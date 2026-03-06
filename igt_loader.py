import os
import torch
import numpy as np
from PIL import Image, ImageOps

class IGT_LoadImageBatch:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "directory": ("STRING", {"default": "/path/to/images"}),
                "index": ("INT", {"default": 0, "min": 0, "max": 999999}),
            },
        }

    # Добавляем третий выход для метаданных (кастомный тип IGT_META)
    RETURN_TYPES = ("IMAGE", "STRING", "IGT_META")
    RETURN_NAMES = ("image", "filename", "source_meta")
    FUNCTION = "load_image"
    CATEGORY = "image/igt Tools"

    def load_image(self, directory, index):
        if not os.path.isdir(directory):
            print(f"[IGT] Error: Directory not found: {directory}")
            return (torch.zeros((1, 64, 64, 3)), "error_path", {})

        valid_extensions = {'.jpg', '.jpeg', '.png', '.webp', '.bmp', '.tiff'}
        files = [f for f in os.listdir(directory) if os.path.splitext(f)[1].lower() in valid_extensions]
        files.sort()

        if not files:
            print(f"[IGT] Error: No images found in {directory}")
            return (torch.zeros((1, 64, 64, 3)), "empty_folder", {})

        target_index = index
        if target_index >= len(files):
            print(f"[IGT] Warning: Index {index} out of range (max {len(files)-1}). Using last file.")
            target_index = len(files) - 1
        
        filename = files[target_index]
        image_path = os.path.join(directory, filename)
        
        # Загрузка изображения и извлечение сырых метаданных
        i = Image.open(image_path)
        
        # Сохраняем EXIF, ICC и блок Photoshop (именно в нем PIL хранит IPTC)
        source_meta = {
            "exif": i.info.get("exif"),
            "photoshop": i.info.get("photoshop"),
            "icc_profile": i.info.get("icc_profile")
        }

        i = ImageOps.exif_transpose(i)
        image = i.convert("RGB")
        image = np.array(image).astype(np.float32) / 255.0
        image = torch.from_numpy(image)[None,]

        filename_text = os.path.splitext(filename)[0]
        
        print(f"[IGT] Loaded batch {target_index}/{len(files)-1}: {filename}")
        
        return (image, filename_text, source_meta)