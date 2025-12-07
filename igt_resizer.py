import math

class IGT_ImageResizer:
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE",),
                "resolution": ("FLOAT", {"default": 1.0, "min": 0.1, "max": 32.0, "step": 0.1, "display": "number"}), # В мегапикселях (1 = 1024x1024)
                "round_to": ("INT", {"default": 64, "min": 8, "max": 512, "step": 8}),
            },
        }

    RETURN_TYPES = ("INT", "INT", "STRING")
    RETURN_NAMES = ("width", "height", "info")
    FUNCTION = "execute"
    CATEGORY = "image/igt Tools"
    
    def execute(self, image, resolution, round_to):
        _, h, w, _ = image.shape
        original_ar = w / h
        
        # Целевая площадь в пикселях (1 MP = 1048576 px, как в Comfy стандарте 1024*1024)
        target_pixels = resolution * 1048576
        
        # 1. Считаем идеальные размеры, сохраняющие пропорции
        ideal_height = math.sqrt(target_pixels / original_ar)
        ideal_width = ideal_height * original_ar
        
        # 2. Функция для получения кандидатов (округление вниз и вверх)
        def get_candidates(val, div):
            floored = (int(val) // div) * div
            ceiled = floored + div
            return [floored, ceiled]
        
        w_candidates = get_candidates(ideal_width, round_to)
        h_candidates = get_candidates(ideal_height, round_to)
        
        best_w = w_candidates[0]
        best_h = h_candidates[0]
        min_ar_error = float('inf')
        
        # 3. Перебираем 4 комбинации округления, чтобы найти ту, где искажение пропорций минимально
        # Искажение важнее, чем точное попадание в мегапиксели
        for wc in w_candidates:
            for hc in h_candidates:
                if wc == 0 or hc == 0: continue
                current_ar = wc / hc
                # Считаем ошибку пропорции (логарифм отношения, чтобы сжатие и растяжение весили одинаково)
                ar_error = abs(math.log(current_ar / original_ar))
                
                if ar_error < min_ar_error:
                    min_ar_error = ar_error
                    best_w = wc
                    best_h = hc
                elif ar_error == min_ar_error:
                    # Если ошибки равны, берем тот, что ближе к целевому разрешению
                    current_pixels = wc * hc
                    if abs(current_pixels - target_pixels) < abs((best_w * best_h) - target_pixels):
                        best_w = wc
                        best_h = hc

        # Формируем информационную строку
        real_mp = round((best_w * best_h) / 1048576, 2)
        info_str = f"{best_w}x{best_h} ({real_mp} MP)"
        
        # Отправляем данные в JS для обновления интерфейса ноды
        return {
            "ui": {
                "res_w": [best_w],
                "res_h": [best_h],
                "info": [info_str]
            },
            "result": (best_w, best_h, info_str)
        }