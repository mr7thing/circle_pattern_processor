import numpy as np
import cv2
import torch
from PIL import Image, ImageDraw
import time

class ImageBinarizer:
    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "binarize_image"
    CATEGORY = "image/pattern"
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "threshold": ("FLOAT", {
                    "default": 127,
                    "min": 0,
                    "max": 255,
                    "step": 1,
                    "display": "slider"
                })
            }
        }
    
    def binarize_image(self, image, threshold):
        if isinstance(image, torch.Tensor):
            img = (image[0] * 255).cpu().numpy().astype(np.uint8)
        else:
            img = (image[0] * 255).astype(np.uint8)

        if len(img.shape) != 3:
            raise ValueError("输入图像必须是3通道RGB图像")
        height, width, channels = img.shape
        if channels != 3:
            raise ValueError(f"输入图像必须是3通道RGB图像，当前通道数：{channels}")

        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        _, binary = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)
        result_img = Image.fromarray(binary).convert('RGB')
        
        result_array = np.array(result_img) / 255.0
        result_tensor = torch.from_numpy(result_array).float()
        result_tensor = result_tensor.unsqueeze(0)
        return (result_tensor,)

class CirclePatternProcessor:
    RETURN_TYPES = ("IMAGE", "TUPLE")
    RETURN_NAMES = ("IMAGE", "CIRCLES")
    FUNCTION = "process_circles"
    CATEGORY = "image/pattern"
    
    def __init__(self):
        pass
        
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "min_radius": ("FLOAT", {
                    "default": 5,
                    "min": 1,
                    "max": 100,
                    "step": 1,
                    "display": "slider"
                }),
                "max_radius": ("FLOAT", {
                    "default": 20,
                    "min": 1,
                    "max": 100,
                    "step": 1,
                    "display": "slider"
                }),
                "output_circle_size": ("FLOAT", {
                    "default": 10,
                    "min": 1,
                    "max": 50,
                    "step": 1,
                    "display": "slider"
                }),
                "edge_detection_sensitivity": ("FLOAT", {
                    "default": 50,
                    "min": 1,
                    "max": 100,
                    "step": 1,
                    "display": "slider"
                }),
                "circle_accumulator_threshold": ("FLOAT", {
                    "default": 30,
                    "min": 1,
                    "max": 100,
                    "step": 1,
                    "display": "slider"
                }),
                "min_center_dist": ("FLOAT", {
                    "default": 10,
                    "min": 1,
                    "max": 100,
                    "step": 1,
                    "display": "slider"
                }),
                "merge_mode": (["keep_first", "use_average"], {
                    "default": "keep_first"
                })
            }
        }
    def process_circles(self, image, min_radius, max_radius, output_circle_size, edge_detection_sensitivity, circle_accumulator_threshold, min_center_dist, merge_mode):
        try:
            # 转换图像格式：从Tensor转为NumPy数组
            if isinstance(image, torch.Tensor):
                img = (image[0] * 255).cpu().numpy().astype(np.uint8)
            else:
                img = (image[0] * 255).astype(np.uint8)

            # 检查图像维度
            if len(img.shape) != 3:
                raise ValueError("输入图像必须是3通道RGB图像")
            height, width, channels = img.shape
            if channels != 3:
                raise ValueError(f"输入图像必须是3通道RGB图像，当前通道数：{channels}")

            # 参数类型检查和转换
            min_radius_int = max(1, int(min_radius))
            max_radius_int = max(min_radius_int, int(max_radius))
            output_circle_size = max(1, int(output_circle_size))
            edge_detection_sensitivity = float(edge_detection_sensitivity)
            circle_accumulator_threshold = float(circle_accumulator_threshold)
            min_center_dist = max(1, float(min_center_dist))

            # 转换为灰度图像
            gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
            
            circles = cv2.HoughCircles(
                gray,
                cv2.HOUGH_GRADIENT,
                dp=1,
                minDist=min_radius_int,
                param1=edge_detection_sensitivity,
                param2=circle_accumulator_threshold,
                minRadius=min_radius_int,
                maxRadius=max_radius_int
            )
            
            # 创建新图像用于绘制标准化的圆
            result_img = Image.new('RGB', (width, height), 'black')
            draw = ImageDraw.Draw(result_img)
            
            # 存储检测到的圆形数据
            circle_data = []
            
            if circles is not None:
                circles = np.round(circles[0, :]).astype(int)
                # 合并距离较近的圆心
                merged_circles = []
                used_indices = set()
                
                for i in range(len(circles)):
                    if i in used_indices:
                        continue
                        
                    current_circle = circles[i]
                    close_circles = [current_circle]
                    
                    # 查找距离当前圆心较近的其他圆心
                    for j in range(i + 1, len(circles)):
                        if j in used_indices:
                            continue
                        
                        other_circle = circles[j]
                        dist = np.sqrt((current_circle[0] - other_circle[0])**2 + 
                                     (current_circle[1] - other_circle[1])**2)
                        
                        if dist <= min_center_dist:
                            close_circles.append(other_circle)
                            used_indices.add(j)
                    
                    # 根据合并模式处理圆心
                    if merge_mode == "keep_first":
                        merged_circles.append(close_circles[0])
                    else:  # use_average
                        avg_x = int(np.mean([c[0] for c in close_circles]))
                        avg_y = int(np.mean([c[1] for c in close_circles]))
                        avg_r = int(np.mean([c[2] for c in close_circles]))
                        merged_circles.append([avg_x, avg_y, avg_r])
                    
                    used_indices.add(i)
                
                # 绘制合并后的圆并存储圆形数据
                for (x, y, r) in merged_circles:
                    # 确保圆的坐标在图像范围内
                    if 0 <= x < width and 0 <= y < height:
                        # 绘制标准大小的白色圆
                        draw.ellipse(
                            [(x - output_circle_size, y - output_circle_size),
                             (x + output_circle_size, y + output_circle_size)],
                            fill='white'
                        )
                        # 存储圆形数据
                        circle_data.append((x, y, r))
            
            # 转换回 ComfyUI 格式
            result_array = np.array(result_img) / 255.0
            result_tensor = torch.from_numpy(result_array).float()
            result_tensor = result_tensor.unsqueeze(0)
            return (result_tensor, circle_data)
            
        except Exception as e:
            raise ValueError(f"处理圆形图案时出错：{str(e)}")

        # 转换回 ComfyUI 格式
        result_array = np.array(result_img) / 255.0
        result_tensor = torch.from_numpy(result_array).float()
        result_tensor = result_tensor.unsqueeze(0)
        return (result_tensor, circle_data)
