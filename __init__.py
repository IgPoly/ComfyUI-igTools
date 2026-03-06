from .igt_tilescalc import IGT_SimpleTilesCalc, IGT_ImageTilesCalc
from .igt_resizer import IGT_ImageResizer, IGT_AspectRatioResizer
from .igt_math import IGT_IntMinMax, IGT_FloatMinMax
from .igt_telegram import IGT_TelegramSender
# Импортируем оба лоадера
from .igt_loader import IGT_LoadImageBatch, IGT_LoadSingleImage 

NODE_CLASS_MAPPINGS = {
    "IGT_SimpleTilesCalc": IGT_SimpleTilesCalc,
    "IGT_ImageTilesCalc": IGT_ImageTilesCalc,
    "IGT_ImageResizer": IGT_ImageResizer,
    "IGT_AspectRatioResizer": IGT_AspectRatioResizer,
    "IGT_IntMinMax": IGT_IntMinMax,
    "IGT_FloatMinMax": IGT_FloatMinMax,
    "IGT_TelegramSender": IGT_TelegramSender,
    "IGT_LoadImageBatch": IGT_LoadImageBatch,
    "IGT_LoadSingleImage": IGT_LoadSingleImage # <-- Новая нода
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "IGT_SimpleTilesCalc": "IGT Simple Tiles Calc (WxH)",
    "IGT_ImageTilesCalc": "IGT Image Tiles Calc (Image)",
    "IGT_ImageResizer": "IGT Smart Resizer (Image)",
    "IGT_AspectRatioResizer": "IGT Smart Resizer (Ratio)",
    "IGT_IntMinMax": "IGT Min/Max (INT)",
    "IGT_FloatMinMax": "IGT Min/Max (FLOAT)",
    "IGT_TelegramSender": "IGT Save to Telegram",
    "IGT_LoadImageBatch": "IGT Load Image Batch (Dir)",
    "IGT_LoadSingleImage": "IGT Load Image (Single)" # <-- Имя в поиске
}

WEB_DIRECTORY = "./js" 

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS', 'WEB_DIRECTORY']