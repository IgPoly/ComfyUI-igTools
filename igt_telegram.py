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
                "send_mode": (["Document (Best Quality)", "Photo (Preview)"],),
                "filename_prefix": ("STRING", {"default": "ComfyImage"}),
                # Новый чекбокс
                "use_input_data": ("BOOLEAN", {"default": False}), 
            },
            "optional": {
                # Новые входы для линков от Лоадера
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
            save_kwargs = {} # Словарь для инъекции IPTC/EXIF

            if "Document" in send_mode:
                metadata = PngInfo()
                if prompt is not None:
                    metadata.add_text("prompt", json.dumps(prompt))
                if extra_pnginfo is not None:
                    for x in extra_pnginfo:
                        metadata.add_text(x, json.dumps(extra_pnginfo[x]))

                # Если включен чекбокс и есть линк на метаданные, внедряем их
                if use_input_data and source_meta:
                    if source_meta.get("exif"):
                        save_kwargs["exif"] = source_meta["exif"]
                    if source_meta.get("photoshop"):
                        # В блоке photoshop лежат данные IPTC
                        save_kwargs["photoshop"] = source_meta["photoshop"]
                    if source_meta.get("icc_profile"):
                        save_kwargs["icc_profile"] = source_meta["icc_profile"]

            img_buffer = io.BytesIO()
            
            if "Document" in send_mode:
                # Внедряем save_kwargs (IPTC/EXIF) при сохранении документа
                img.save(img_buffer, format="PNG", pnginfo=metadata, compress_level=4, **save_kwargs)
                target_ext = "png"
                method = "sendDocument"
                file_key = 'document'
            else:
                img.save(img_buffer, format="JPEG", quality=90)
                target_ext = "jpg"
                method = "sendPhoto"
                file_key = 'photo'
            
            img_buffer.seek(0)

            # Формирование имени файла
            if use_input_data and filename_override:
                # Используем имя из лоадера
                batch_suf = f"_{i}" if len(image) > 1 else ""
                filename = f"{filename_override}{batch_suf}.{target_ext}"
            else:
                # Используем стандартный префикс
                timestamp = datetime.datetime.now().strftime("%H%M%S")
                batch_suf = f"_{i}" if len(image) > 1 else ""
                filename = f"{filename_prefix}_{timestamp}{batch_suf}.{target_ext}"

            # Отправка
            url = f"https://api.telegram.org/bot{bot_token}/{method}"
            data = {'chat_id': chat_id, 'caption': caption}
            files = {file_key: (filename, img_buffer, f'image/{target_ext}')}

            try:
                response = requests.post(url, data=data, files=files, timeout=30)
                if response.status_code != 200:
                    print(f"[IGT_Telegram] Failed to send: {response.text}")
                else:
                    print(f"[IGT_Telegram] Sent {filename} to Telegram.")
            except Exception as e:
                print(f"[IGT_Telegram] Connection Error: {e}")

        return (image,)