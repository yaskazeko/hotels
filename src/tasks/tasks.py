import os
from time import sleep

from PIL import Image

from src.tasks.celery_app import celery_app


@celery_app.task
# ... existing code ...
def task_test():
    sleep(5)
    print("The test task was executed successfully ")


@celery_app.task
def resize_image(image_path):
    """
    Задача для ресайза изображения в Full HD и SD.
    Сохраняет пропорции изображения (thumbnail).
    """
    if not os.path.exists(image_path):
        return f"File not found: {image_path}"

    # Размеры для ресайза
    sizes = {"full_hd": (1920, 1080), "sd": (640, 480)}

    filename, ext = os.path.splitext(image_path)
    output_paths = []

    try:
        with Image.open(image_path) as img:
            for size_name, size in sizes.items():
                # Работаем с копией, чтобы не менять объект для следующей итерации
                img_copy = img.copy()

                # thumbnail изменяет размер, сохраняя пропорции, чтобы картинка вписалась в заданные рамки
                img_copy.thumbnail(size)

                output_path = f"{filename}_{size_name}{ext}"
                img_copy.save(output_path)
                output_paths.append(output_path)

        return output_paths
    except Exception as e:
        return f"Error processing image: {e}"
