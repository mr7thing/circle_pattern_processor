import os
import re
import torch
import numpy as np

class CirclePatternSVGExporter:
    RETURN_TYPES = ("STRING",)
    FUNCTION = "export_to_svg"
    CATEGORY = "image/pattern"
    
    @staticmethod
    def get_next_sequence_number(base_path):
        # 获取目录中现有的文件
        if not os.path.exists(base_path):
            os.makedirs(base_path)
            return 0
        
        files = os.listdir(base_path)
        max_sequence = -1
        
        # 查找当前最大序号
        pattern = re.compile(r'\d{4}\.[^.]+$')
        for file in files:
            if pattern.search(file):
                try:
                    sequence = int(file[-8:-4])
                    max_sequence = max(max_sequence, sequence)
                except ValueError:
                    continue
        
        return max_sequence + 1
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "circles": ("TUPLE",),
                "image": ("IMAGE",),
                "filename": ("STRING", {
                    "default": "pattern.svg"
                }),
                "output_circle_size": ("FLOAT", {
                    "default": 10,
                    "min": 1,
                    "max": 50,
                    "step": 1,
                    "display": "slider"
                })
            }
        }
    
    def export_to_svg(self, circles, image, filename, output_circle_size):
        try:
            print("开始保存SVG文件...")
            # 确保circles是有效的元组
            if not circles or not isinstance(circles, (tuple, list)):
                raise ValueError("无效的圆形数据")
                
            # 从图像获取尺寸
            if not isinstance(image, torch.Tensor):
                raise ValueError("无效的图像数据")
                
            height, width = image.shape[1:3]
            
            # 构建输出路径，使用绝对路径
            current_dir = os.path.dirname(os.path.abspath(__file__))
            base_dir = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(current_dir)), "output", "svg"))
            
            # 处理子目录
            if "/" in filename or "\\" in filename:
                subdir = os.path.dirname(filename)
                filename = os.path.basename(filename)
                base_dir = os.path.join(base_dir, subdir)
            
            # 确保目录存在
            os.makedirs(base_dir, exist_ok=True)
            
            # 获取序列号并构建完整文件名
            sequence = self.get_next_sequence_number(base_dir)
            name, ext = os.path.splitext(filename)
            if not ext:
                ext = ".svg"
            final_filename = f"{name}{sequence:04d}{ext}"
            output_path = os.path.join(base_dir, final_filename)
            print(f"准备保存SVG文件到: {output_path}")
            
            # 生成SVG内容
            svg_content = f'<?xml version="1.0" encoding="UTF-8"?>\n'
            svg_content += f'<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">\n'
            
            # 将圆形添加到SVG中
            circle_count = 0
            for (x, y, _) in circles:  # 忽略原始半径，使用传入的大小
                if 0 <= x < width and 0 <= y < height:
                    svg_content += f'  <circle cx="{x}" cy="{y}" r="{output_circle_size}" '
                    svg_content += 'fill="white" stroke="none" opacity="1" />'
                    circle_count += 1
            
            svg_content += '</svg>'
            print(f"已生成SVG内容，包含 {circle_count} 个圆形")
            
            # 保存SVG文件
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(svg_content)
            
            print(f"SVG文件保存成功: {output_path}")
            return (f"SVG文件已保存至: {output_path}",)
            
        except Exception as e:
            error_msg = f"保存SVG文件时出错: {str(e)}"
            print(error_msg)
            return (error_msg,)