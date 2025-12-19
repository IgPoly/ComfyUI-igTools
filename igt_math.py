class IGT_IntMinMax:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "a": ("INT", {"default": 0, "min": -sys.maxsize, "max": sys.maxsize}),
                "b": ("INT", {"default": 0, "min": -sys.maxsize, "max": sys.maxsize}),
            },
        }

    RETURN_TYPES = ("INT", "INT")
    RETURN_NAMES = ("min", "max")
    FUNCTION = "execute"
    CATEGORY = "image/igt Tools"
    
    def execute(self, a, b):
        min_val = min(a, b)
        max_val = max(a, b)
        
        # Возвращаем данные для JS (ui) и для Comfy (result)
        return {
            "ui": { "min_val": [min_val], "max_val": [max_val] },
            "result": (min_val, max_val)
        }

class IGT_FloatMinMax:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "a": ("FLOAT", {"default": 0.0, "min": -sys.float_info.max, "max": sys.float_info.max, "step": 0.01}),
                "b": ("FLOAT", {"default": 0.0, "min": -sys.float_info.max, "max": sys.float_info.max, "step": 0.01}),
            },
        }

    RETURN_TYPES = ("FLOAT", "FLOAT")
    RETURN_NAMES = ("min", "max")
    FUNCTION = "execute"
    CATEGORY = "image/igt Tools"
    
    def execute(self, a, b):
        min_val = min(a, b)
        max_val = max(a, b)
        
        # Округлим для красивого отображения в UI, но в result отдадим точные данные
        ui_min = round(min_val, 4)
        ui_max = round(max_val, 4)

        return {
            "ui": { "min_val": [ui_min], "max_val": [ui_max] },
            "result": (min_val, max_val)
        }

# Нужно для получения максимальных значений системы
import sys