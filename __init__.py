from .igt_tilescalc import IGT_SimpleTilesCalc, IGT_ImageTilesCalc
from .igt_resizer import IGT_ImageResizer, IGT_AspectRatioResizer
from .igt_math import IGT_IntMinMax, IGT_FloatMinMax # <-- Добавили

NODE_CLASS_MAPPINGS = {
    "IGT_SimpleTilesCalc": IGT_SimpleTilesCalc,
    "IGT_ImageTilesCalc": IGT_ImageTilesCalc,
    "IGT_ImageResizer": IGT_ImageResizer,
    "IGT_AspectRatioResizer": IGT_AspectRatioResizer,
    "IGT_IntMinMax": IGT_IntMinMax,     # <-- Добавили
    "IGT_FloatMinMax": IGT_FloatMinMax  # <-- Добавили
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "IGT_SimpleTilesCalc": "IGT Simple Tiles Calc (WxH)",
    "IGT_ImageTilesCalc": "IGT Image Tiles Calc (Image)",
    "IGT_ImageResizer": "IGT Smart Resizer (Image)",
    "IGT_AspectRatioResizer": "IGT Smart Resizer (Ratio)",
    "IGT_IntMinMax": "IGT Min/Max (INT)",      # <-- Добавили
    "IGT_FloatMinMax": "IGT Min/Max (FLOAT)"   # <-- Добавили
}

WEB_DIRECTORY = "./js" 

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS', 'WEB_DIRECTORY']