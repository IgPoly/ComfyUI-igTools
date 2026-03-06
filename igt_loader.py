import os
import hashlib
import torch
import numpy as np
from PIL import Image, ImageOps
import folder_paths

class IGT_LoadSingleImage:
    @classmethod
    def INPUT_TYPES(s):
        input_dir = folder_paths.get_input_directory()
        files = [f for f in os.listdir(input_dir) if os.path.isfile(os.path.join(input_dir, f))]
        return {"required":
                    {"image": (sorted(files), {"image_upload": True})},
                }

    CATEGORY = "image/igt Tools"
    RETURN_TYPES = ("IMAGE", "MASK", "STRING", "IGT_META")
    RETURN_NAMES = ("image", "mask", "filename", "source_meta")
    FUNCTION = "load_image"

    def load_image(self, image):
        image_path = folder_paths.get_annotated_filepath(image)
        
        if not os.path.exists(image_path):
             print(f"[IGT] Error: File not found: {image_path}")
             return (torch.zeros((1, 64, 64, 3)), torch.zeros((1, 64, 64)), "error_file", {})

        i = Image.open(image_path)
        filename_text = os.path.splitext(image)[0]
        
        # ЗАБИРАЕМ ВСЕ МЕТАДАННЫЕ ИЗ ФАЙЛА
        source_meta = {}
        for k, v in i.info.items():
            # Берем только безопасные типы данных, чтобы не сломать линки ComfyUI
            if isinstance(v, (str, bytes, dict, int, float)):
                source_meta[k] = v
                
        # ПЕЧАТАЕМ В КОНСОЛЬ, ЧТОБЫ УВИДЕТЬ ИСТИНУ
        print(f"\n[IGT] --- METADATA FOUND IN {filename_text} ---")
        print(f"[IGT] Keys: {list(source_meta.keys())}\n")

        i = ImageOps.exif_transpose(i)
        
        if i.mode == 'I':
            i = i.point(lambda i: i * (1 / 255))
        image_rgb = i.convert("RGB")
        image_tensor = np.array(image_rgb).astype(np.float32) / 255.0
        image_tensor = torch.from_numpy(image_tensor)[None,]
        
        if 'A' in i.getbands():
            mask = np.array(i.getchannel('A')).astype(np.float32) / 255.0
            mask = 1. - mask
        else:
            mask = np.zeros((64, 64), dtype=np.float32)
        mask = torch.from_numpy(mask)[None,]
        
        return (image_tensor, mask, filename_text, source_meta)

    @classmethod
    def IS_CHANGED(s, image):
        image_path = folder_paths.get_annotated_filepath(image)
        m = hashlib.sha256()
        with open(image_path, 'rb') as f:
            m.update(f.read())
        return m.digest().hex()

    @classmethod
    def VALIDATE_INPUTS(s, image):
        if not folder_paths.exists_annotated_filepath(image):
            return "Invalid image file: {}".format(image)
        return True


class IGT_LoadImageBatch:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "directory": ("STRING", {"default": "/path/to/images"}),
                "index": ("INT", {"default": 0, "min": 0, "max": 999999}),
            },
        }

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
        
        i = Image.open(image_path)
        filename_text = os.path.splitext(filename)[0]
        
        # ЗАБИРАЕМ ВСЕ МЕТАДАННЫЕ ИЗ ФАЙЛА
        source_meta = {}
        for k, v in i.info.items():
            if isinstance(v, (str, bytes, dict, int, float)):
                source_meta[k] = v
                
        # ПЕЧАТАЕМ В КОНСОЛЬ, ЧТОБЫ УВИДЕТЬ ИСТИНУ
        print(f"\n[IGT] --- METADATA FOUND IN {filename_text} ---")
        print(f"[IGT] Keys: {list(source_meta.keys())}\n")

        i = ImageOps.exif_transpose(i)
        image_rgb = i.convert("RGB")
        image_np = np.array(image_rgb).astype(np.float32) / 255.0
        image_tensor = torch.from_numpy(image_np)[None,]

        return (image_tensor, filename_text, source_meta)