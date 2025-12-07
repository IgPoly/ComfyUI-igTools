import math

# --- Твой старый класс (оставляем как есть) ---
class IGT_SimpleTilesCalc:
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image_width": ("INT", {"forceInput": True}),
                "image_height": ("INT", {"forceInput": True}),
                "tile_resolution": ("FLOAT", {"default": 1}),
                "min_overlap": ("INT", {"default": 64}),
            },
        }

    RETURN_TYPES = ("INT","INT", "INT", 'INT')
    RETURN_NAMES = ("best_tile_w", "best_tile_h", "best_overlap", "min_tiles")
    FUNCTION = "calctiles"
    CATEGORY = "image/igt Tools"
    
    def calctiles(self, image_width, image_height, tile_resolution, min_overlap):
        tile_resolution_px = math.floor(tile_resolution * 1048576)
        
        best_tile_w = 640
        best_tile_h = 640
        best_overlap = min_overlap
        min_tiles = float('inf')
        max_area = 0 
        limit_dim = 2048 
        
        for tile_w in range(640, limit_dim, 64):
            for tile_h in range(640, limit_dim, 64):
                current_area = tile_w * tile_h
                if current_area > tile_resolution_px: break
                if min_overlap >= tile_w or min_overlap >= tile_h: continue

                if image_width <= tile_w: tiles_w = 1
                else: tiles_w = 1 + math.ceil((image_width - tile_w) / (tile_w - min_overlap))

                if image_height <= tile_h: tiles_h = 1
                else: tiles_h = 1 + math.ceil((image_height - tile_h) / (tile_h - min_overlap))

                total_tiles = tiles_w * tiles_h

                if total_tiles < min_tiles:
                    min_tiles = total_tiles
                    best_tile_w, best_tile_h, best_overlap, max_area = tile_w, tile_h, min_overlap, current_area
                elif total_tiles == min_tiles:
                    if current_area > max_area:
                        best_tile_w, best_tile_h, best_overlap, max_area = tile_w, tile_h, min_overlap, current_area

        return {
            "ui": {
                "tile_w": [int(best_tile_w)],
                "tile_h": [int(best_tile_h)],
                "overlap": [int(best_overlap)],
                "total": [int(min_tiles)]
            },
            "result": (int(best_tile_w), int(best_tile_h), int(best_overlap), int(min_tiles))
        }

# --- НОВЫЙ КЛАСС ---
class IGT_ImageTilesCalc:
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                # Принимаем IMAGE вместо цифр
                "image": ("IMAGE",), 
                "tile_resolution": ("FLOAT", {"default": 1}),
                "min_overlap": ("INT", {"default": 64}),
            },
        }

    RETURN_TYPES = ("INT","INT", "INT", 'INT')
    RETURN_NAMES = ("best_tile_w", "best_tile_h", "best_overlap", "min_tiles")
    FUNCTION = "execute"
    CATEGORY = "image/igt Tools"
    
    def execute(self, image, tile_resolution, min_overlap):
        # image.shape выдает (Batch_Size, Height, Width, Channels)
        # Нам нужны Height (индекс 1) и Width (индекс 2)
        _, h, w, _ = image.shape
        
        # Просто вызываем метод расчета из соседнего класса, чтобы не дублировать код
        calc_node = IGT_SimpleTilesCalc()
        return calc_node.calctiles(w, h, tile_resolution, min_overlap)