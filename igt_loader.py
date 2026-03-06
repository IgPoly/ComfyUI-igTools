import os
import hashlib
import torch
import numpy as np
from PIL import Image, ImageOps
import folder_paths

# --- КЛАСС 1: Загрузчик одиночного файла (Полный аналог системного LoadImage) ---
class IGT_LoadSingleImage:
    @classmethod
    def INPUT_TYPES(s):
        input_dir = folder_paths.get_input_directory()
        files = [f for f in os.listdir(input_dir) if os.path.isfile(os.path.join(input_dir, f))]
        return {"required":
                    {"image": (sorted(files), {"image_upload": True})},
                }

    CATEGORY = "image/igt Tools"
    # Добавили MASK (как в оригинале), STRING (имя) и IGT_META (метаданные)
    RETURN_TYPES = ("IMAGE", "MASK", "STRING", "IGT_META")
    RETURN_NAMES = ("image", "mask", "filename", "source_meta")
    FUNCTION = "load_image"

    def load_image(self, image):
        image_path = folder_paths.get_annotated_filepath(image)
        
        # Загрузка изображения
        i = Image.open(image_path)
        
        # Извлекаем метаданные: EXIF, ICC и блок Photoshop (где лежит IPTC)
        source_meta = {
            "exif": i.info.get("exif"),
            "photoshop": i.info.get("photoshop"),
            "icc_profile": i.info.get("icc_profile")
        }

        i = ImageOps.exif_transpose(i)
        
        # Конвертация в формат ComfyUI (RGB Tensor)
        if i.mode == 'I':
            i = i.point(lambda i: i * (1 / 255))
        image_rgb = i.convert("RGB")
        image_tensor = np.array(image_rgb).astype(np.float32) / 255.0
        image_tensor = torch.from_numpy(image_tensor)[None,]
        
        # Создание альфа-маски (как в оригинальном лоадере)
        if 'A' in i.getbands():
            mask = np.array(i.getchannel('A')).astype(np.float32) / 255.0
            mask = 1. - mask
        else:
            mask = np.zeros((64, 64), dtype=np.float32)
        mask = torch.from_numpy(mask)[None,]

        # Имя файла без расширения
        filename_text = os.path.splitext(image)[0]
        
        return (image_tensor, mask, filename_text, source_meta)

    # Системные функции ComfyUI для кэширования файлов при drag-and-drop
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


# --- КЛАСС 2: Загрузчик папки (Batch) ---
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
        
        source_meta = {
            "exif": i.info.get("exif"),
            "photoshop": i.info.get("photoshop"),
            "icc_profile": i.info.get("icc_profile")
        }

        i = ImageOps.exif_transpose(i)
        image_rgb = i.convert("RGB")
        image_np = np.array(image_rgb).astype(np.float32) / 255.0
        image_tensor = torch.from_numpy(image_np)[None,]

        filename_text = os.path.splitext(filename)[0]
        return (image_tensor, filename_text, source_meta)