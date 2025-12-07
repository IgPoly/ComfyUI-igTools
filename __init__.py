from .igt_tilescalc import IGT_SimpleTilesCalc, IGT_ImageTilesCalc
from .igt_resizer import IGT_ImageResizer # Импортируем новый файл

NODE_CLASS_MAPPINGS = {
    "IGT_SimpleTilesCalc": IGT_SimpleTilesCalc,
    "IGT_ImageTilesCalc": IGT_ImageTilesCalc,
    "IGT_ImageResizer": IGT_ImageResizer # Регистрируем
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "IGT_SimpleTilesCalc": "IGT Simple Tiles Calc (WxH)",
    "IGT_ImageTilesCalc": "IGT Image Tiles Calc (Image)",
    "IGT_ImageResizer": "IGT Smart Resizer (Mpix)" # Красивое имя
}

WEB_DIRECTORY = "./js" 

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS', 'WEB_DIRECTORY']