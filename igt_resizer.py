import math

# --- Вспомогательная функция (ядро логики) ---
def calculate_smart_resolution(target_ar, resolution, round_to):
    # Целевая площадь в пикселях (1 MP = 1048576 px)
    target_pixels = resolution * 1048576
    
    # 1. Считаем идеальные размеры
    ideal_height = math.sqrt(target_pixels / target_ar)
    ideal_width = ideal_height * target_ar
    
    # 2. Кандидаты на округление
    def get_candidates(val, div):
        floored = (int(val) // div) * div
        ceiled = floored + div
        return [floored, ceiled]
    
    w_candidates = get_candidates(ideal_width, round_to)
    h_candidates = get_candidates(ideal_height, round_to)
    
    best_w = w_candidates[0]
    best_h = h_candidates[0]
    min_ar_error = float('inf')
    
    # 3. Перебор комбинаций для минимизации ошибки пропорций
    for wc in w_candidates:
        for hc in h_candidates:
            if wc == 0 or hc == 0: continue
            current_ar = wc / hc
            # Log error делает сжатие и растяжение равнозначными
            ar_error = abs(math.log(current_ar / target_ar))
            
            if ar_error < min_ar_error:
                min_ar_error = ar_error
                best_w = wc
                best_h = hc
            elif ar_error == min_ar_error:
                # При равной ошибке пропорций, выбираем то, что ближе по площади к цели
                current_pixels = wc * hc
                if abs(current_pixels - target_pixels) < abs((best_w * best_h) - target_pixels):
                    best_w = wc
                    best_h = hc
                    
    # Инфо строка
    real_mp = round((best_w * best_h) / 1048576, 2)
    info_str = f"{best_w}x{best_h} ({real_mp} MP)"
    
    return best_w, best_h, info_str


# --- Нода 1: Ресайз на основе картинки ---
class IGT_ImageResizer:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE",),
                "resolution": ("FLOAT", {"default": 1.0, "min": 0.1, "max": 32.0, "step": 0.1}),
                "round_to": ("INT", {"default": 64, "min": 8, "max": 512, "step": 8}),
            },
        }

    RETURN_TYPES = ("INT", "INT", "STRING")
    RETURN_NAMES = ("width", "height", "info")
    FUNCTION = "execute"
    CATEGORY = "image/igt Tools"
    
    def execute(self, image, resolution, round_to):
        _, h, w, _ = image.shape
        target_ar = w / h
        
        best_w, best_h, info_str = calculate_smart_resolution(target_ar, resolution, round_to)

        return {
            "ui": { "res_w": [best_w], "res_h": [best_h], "info": [info_str] },
            "result": (best_w, best_h, info_str)
        }


# --- Нода 2: Ресайз на основе списка соотношений ---
class IGT_AspectRatioResizer:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "aspect_ratio": ([
                    "1:1", 
                    "4:3", "3:4", 
                    "3:2", "2:3", 
                    "5:4", "4:5", 
                    "16:9", "9:16", 
                    "21:9", "9:21"
                ],),
                "resolution": ("FLOAT", {"default": 1.0, "min": 0.1, "max": 32.0, "step": 0.1}),
                "round_to": ("INT", {"default": 64, "min": 8, "max": 512, "step": 8}),
            },
        }

    RETURN_TYPES = ("INT", "INT", "STRING")
    RETURN_NAMES = ("width", "height", "info")
    FUNCTION = "execute"
    CATEGORY = "image/igt Tools"
    
    def execute(self, aspect_ratio, resolution, round_to):
        # Парсим строку вида "16:9"
        w_str, h_str = aspect_ratio.split(":")
        target_ar = float(w_str) / float(h_str)
        
        best_w, best_h, info_str = calculate_smart_resolution(target_ar, resolution, round_to)

        return {
            "ui": { "res_w": [best_w], "res_h": [best_h], "info": [info_str] },
            "result": (best_w, best_h, info_str)
        }