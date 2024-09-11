import math

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
        tile_resolution_px = math.floor(tile_resolution * 1048576) # Convert MPix to Pixels
        best_tile_w = 640
        best_tile_h = 640
        best_overlap = min_overlap
        min_tiles = 10000  # Initialize with infinity
        max_tile_length = math.floor((tile_resolution_px / 640) / 64) * 64

        # Итерация для нахождения лучших размеров плиток
        for tile_w in range(640, max_tile_length, 64):  # Ширина плитки в диапазоне от 640 до 1536
            for tile_h in range(640, max_tile_length, 64):  # Высота плитки в диапазоне от 640 до 1536
                if tile_w * tile_h <= tile_resolution_px:  # Проверка условия разрешения
                    # Подсчет необходимого количества плиток
                    if (image_width / tile_w) > 1:
                        num_tiles_w = math.ceil(image_width / (tile_w - min_overlap))
                    else:
                        num_tiles_w = 1;
                    if (image_height / tile_h) > 1:
                        num_tiles_h = math.ceil(image_height / (tile_h - min_overlap)) 
                    else:
                        num_tiles_h = 1;
                    total_tiles = num_tiles_w * num_tiles_h
                    # Обновление лучших размеров, если текущие лучше
                    if total_tiles < min_tiles:
                        min_tiles = total_tiles
                        best_tile_w = tile_w
                        best_tile_h = tile_h
                        best_overlap = min_overlap



        return (int(best_tile_w), int(best_tile_h), int(best_overlap), int(min_tiles))
