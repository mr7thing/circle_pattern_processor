# Circle Pattern Processor for ComfyUI

这是一个用于ComfyUI的自定义节点，可以检测图像中的圆形图案并生成标准化的圆形输出。

## 功能特点

- 使用霍夫圆变换检测图像中的圆形
- 可调节的预处理阈值
- 可配置的圆形检测参数（最小/最大半径）
- 输出标准大小的圆形图案
- 支持将检测到的圆形导出为SVG格式

## 安装方法

1. 将此仓库克隆到ComfyUI的`custom_nodes`目录下：
   ```bash
   cd custom_nodes
   git clone [repository_url] circle_pattern_processor
   ```

2. 安装依赖：
   ```bash
   cd circle_pattern_processor
   pip install -r requirements.txt
   ```

## 使用方法

1. 启动ComfyUI
2. 在节点选择菜单中找到"Circle Pattern Processor"和"Circle Pattern SVG Exporter"
3. 将节点添加到工作流中
4. 连接输入图像
5. 调整参数：
   - preprocessing_threshold：图像预处理的阈值（0-255）
   - min_radius：检测圆形的最小半径
   - max_radius：检测圆形的最大半径
   - output_circle_size：输出圆形的大小

## 参数说明

### CirclePatternProcessor节点

- preprocessing_threshold (默认: 127)
  - 范围: 0-255
  - 用于图像二值化的阈值

- min_radius (默认: 5)
  - 范围: 1-100
  - 检测圆形的最小半径

- max_radius (默认: 20)
  - 范围: 1-100
  - 检测圆形的最大半径

- output_circle_size (默认: 10)
  - 范围: 1-50
  - 输出图像中圆形的标准大小

### CirclePatternSVGExporter节点

- output_size (默认: 512)
  - 范围: 64-2048
  - 输出SVG画布的大小

- circle_radius (默认: 10)
  - 范围: 1-100
  - SVG中圆形的半径

- stroke_width (默认: 2)
  - 范围: 0-10
  - SVG中圆形边框的宽度

- stroke_color (默认: "#000000")
  - SVG中圆形边框的颜色

- fill_color (默认: "none")
  - SVG中圆形的填充颜色

## 许可证

MIT License