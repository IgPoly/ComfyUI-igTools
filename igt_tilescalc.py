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
        tile_resolution_px = math.floor(tile_resolution * 1048576)
        
        # Инициализируем "худшими" значениями
        best_tile_w = 640
        best_tile_h = 640
        best_overlap = min_overlap
        min_tiles = float('inf') # Бесконечность
        max_area = 0 # Для выбора самого жирного тайла при равном количестве

        # Максимальная сторона (с запасом +64 для корректной работы range)
        # Ограничим разумным пределом, например 2048, чтобы не уйти в космос
        limit_dim = 2048 
        
        # Пробегаем по ширине и высоте
        # +1 в range не нужен, если мы делаем запас в limit_dim, но для точности добавим шаг
        for tile_w in range(640, limit_dim, 64):
            for tile_h in range(640, limit_dim, 64):
                
                # 1. Проверка площади (не превышаем лимит мегапикселей)
                current_area = tile_w * tile_h
                if current_area > tile_resolution_px:
                    break # Прерываем внутренний цикл, так как дальше h будет только расти

                # 2. Безопасность: нахлест не может быть больше тайла
                if min_overlap >= tile_w or min_overlap >= tile_h:
                    continue

                # 3. Правильный расчет количества плиток по оси W
                if image_width <= tile_w:
                    tiles_w = 1
                else:
                    # Формула: 1 + ceil((W - Tile) / (Tile - Overlap))
                    stride_w = tile_w - min_overlap
                    tiles_w = 1 + math.ceil((image_width - tile_w) / stride_w)

                # 4. Правильный расчет количества плиток по оси H
                if image_height <= tile_h:
                    tiles_h = 1
                else:
                    stride_h = tile_h - min_overlap
                    tiles_h = 1 + math.ceil((image_height - tile_h) / stride_h)

                total_tiles = tiles_w * tiles_h

                # 5. Логика выбора лучшего
                # Если нашли меньше плиток - берем сразу
                if total_tiles < min_tiles:
                    min_tiles = total_tiles
                    best_tile_w = tile_w
                    best_tile_h = tile_h
                    best_overlap = min_overlap
                    max_area = current_area
                
                # Если плиток столько же, но этот тайл БОЛЬШЕ (больше контекста) - берем его
                elif total_tiles == min_tiles:
                    if current_area > max_area:
                        best_tile_w = tile_w
                        best_tile_h = tile_h
                        best_overlap = min_overlap
                        max_area = current_area

        # Возвращаем результат
        # Важно: overlap возвращаем тот же, что и входной (min_overlap), 
        # так как Tiled Diffusion сам расширит его при необходимости, 
        # чтобы равномерно распределить плитки.
        return (int(best_tile_w), int(best_tile_h), int(best_overlap), int(min_tiles))
    
