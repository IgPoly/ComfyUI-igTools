from .igt_tilescalc import IGT_SimpleTilesCalc, IGT_ImageTilesCalc

NODE_CLASS_MAPPINGS = {
    "IGT_SimpleTilesCalc": IGT_SimpleTilesCalc,
    "IGT_ImageTilesCalc": IGT_ImageTilesCalc
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "IGT_SimpleTilesCalc": "IGT Simple Tiles Calc (WxH)",
    "IGT_ImageTilesCalc": "IGT Image Tiles Calc (Image)"
}

WEB_DIRECTORY = "./js" 

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS', 'WEB_DIRECTORY']
