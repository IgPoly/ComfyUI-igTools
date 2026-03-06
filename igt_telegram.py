import requests
import numpy as np
from PIL import Image
from PIL.PngImagePlugin import PngInfo
import io
import json
import datetime

class IGT_TelegramSender:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE",),
                "bot_token": ("STRING", {"default": "", "multiline": False}),
                "chat_id": ("STRING", {"default": "", "multiline": False}),
                "send_mode": (["Document (PNG + Metadata)", "Photo (Compressed JPG)"],),
                "filename_prefix": ("STRING", {"default": "ComfyImage"}),
                "use_input_data": ("BOOLEAN", {"default": False}), 
            },
            "optional": {
                "filename_override": ("STRING", {"forceInput": True}),
                "source_meta": ("IGT_META",),
                "caption": ("STRING", {"default": "", "multiline": True}),
            },
            "hidden": {"prompt": "PROMPT", "extra_pnginfo": "EXTRA_PNGINFO"},
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "send_image"
    CATEGORY = "image/igt Tools"
    OUTPUT_NODE = True

    def send_image(self, image, bot_token, chat_id, send_mode, filename_prefix, use_input_data, filename_override=None, source_meta=None, caption="", prompt=None, extra_pnginfo=None):
        
        if not bot_token or not chat_id:
            print("[IGT_Telegram] Error: Bot Token or Chat ID missing.")
            return (image,)

        for i, img_tensor in enumerate(image):
            i_np = 255. * img_tensor.cpu().numpy()
            img = Image.fromarray(np.clip(i_np, 0, 255).astype(np.uint8))

            metadata = None
            save_kwargs = {}

            if "Document" in send_mode:
                metadata = PngInfo()
                
                # Вшиваем схему (Workflow) ComfyUI
                if prompt is not None:
                    metadata.add_text("prompt", json.dumps(prompt))
                if extra_pnginfo is not None:
                    for x in extra_pnginfo:
                        metadata.add_text(x, json.dumps(extra_pnginfo[x]))

                # Внедряем ВСЕ найденные метаданные из исходника
                if use_input_data and source_meta:
                    for k, v in source_meta.items():
                        if k == "exif":
                            save_kwargs["exif"] = v
                            print("[IGT_Telegram] -> Injected EXIF")
                        elif k == "photoshop" and isinstance(v, bytes):
                            # Если исходник был JPEG, конвертируем блок Adobe IRB в PNG IPTC (формат Apple/ImageMagick)
                            length_str = f"{len(v):8d}"
                            hex_str = v.hex()
                            hex_lines = "\n".join(hex_str[j:j+72] for j in range(0, len(hex_str), 72))
                            profile_text = f"\n{length_str}\n{hex_lines}\n"
                            metadata.add_text("Raw profile type iptc", profile_text)
                            print("[IGT_Telegram] -> Converted JPEG 'photoshop' block to PNG IPTC")
                        elif isinstance(v, str):
                            # Если это XMP, авторские права или уже готовый текстовый чанк PNG
                            metadata.add_text(k, v)
                            print(f"[IGT_Telegram] -> Injected Text Chunk: {k}")

            img_buffer = io.BytesIO()
            
            if "Document" in send_mode:
                # Сохраняем в честный PNG!
                img.save(img_buffer, format="PNG", pnginfo=metadata, compress_level=4, **save_kwargs)
                target_ext = "png"
                method = "sendDocument"
                file_key = 'document'
            else:
                img.save(img_buffer, format="JPEG", quality=85)
                target_ext = "jpg"
                method = "sendPhoto"
                file_key = 'photo'
            
            img_buffer.seek(0)

            # Определение имени файла
            if use_input_data and filename_override:
                batch_suf = f"_{i}" if len(image) > 1 else ""
                filename = f"{filename_override}{batch_suf}.{target_ext}"
            else:
                timestamp = datetime.datetime.now().strftime("%H%M%S")
                batch_suf = f"_{i}" if len(image) > 1 else ""
                filename = f"{filename_prefix}_{timestamp}{batch_suf}.{target_ext}"

            url = f"https://api.telegram.org/bot{bot_token}/{method}"
            data = {'chat_id': chat_id, 'caption': caption}
            files = {file_key: (filename, img_buffer, f'image/{target_ext}')}

            # Отправка
            try:
                response = requests.post(url, data=data, files=files, timeout=30)
                if response.status_code != 200:
                    print(f"[IGT_Telegram] Failed to send: {response.text}")
                else:
                    print(f"[IGT_Telegram] Sent {filename} to Telegram.")
            except Exception as e:
                print(f"[IGT_Telegram] Connection Error: {e}")

        return (image,)