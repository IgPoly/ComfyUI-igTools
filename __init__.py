from .igt_tilescalc import IGT_SimpleTilesCalc, IGT_ImageTilesCalc
from .igt_resizer import IGT_ImageResizer, IGT_AspectRatioResizer

NODE_CLASS_MAPPINGS = {
    "IGT_SimpleTilesCalc": IGT_SimpleTilesCalc,
    "IGT_ImageTilesCalc": IGT_ImageTilesCalc,
    "IGT_ImageResizer": IGT_ImageResizer,
    "IGT_AspectRatioResizer": IGT_AspectRatioResizer
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "IGT_SimpleTilesCalc": "IGT Simple Tiles Calc (WxH)",
    "IGT_ImageTilesCalc": "IGT Image Tiles Calc (Image)",
    "IGT_ImageResizer": "IGT Smart Resizer (Image)",
    "IGT_AspectRatioResizer": "IGT Smart Resizer (Ratio)"
}

WEB_DIRECTORY = "./js" 

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS', 'WEB_DIRECTORY']