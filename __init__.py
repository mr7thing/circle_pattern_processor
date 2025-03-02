from .circle_detector import CirclePatternProcessor, ImageBinarizer
from .svg_exporter import CirclePatternSVGExporter

NODE_CLASS_MAPPINGS = {
    "CirclePatternProcessor": CirclePatternProcessor,
    "ImageBinarizer": ImageBinarizer,
    "CirclePatternSVGExporter": CirclePatternSVGExporter
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "CirclePatternProcessor": "Circle Pattern Processor",
    "ImageBinarizer": "Image Binarizer",
    "CirclePatternSVGExporter": "Circle Pattern SVG Exporter"
}

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']