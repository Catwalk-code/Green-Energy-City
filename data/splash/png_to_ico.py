import os
from PIL import Image

# Получаем путь к папке, где лежит этот скрипт (data/splash/)
script_dir = os.path.dirname(os.path.abspath(__file__))
icon_path = os.path.join(script_dir, "icon.png")
output_path = os.path.join(script_dir, "icon.ico")

# Конвертация
img = Image.open(icon_path)
img.save(
    output_path,
    format="ICO",
    sizes=[(256, 256)]
)
print(f"✅ icon.ico успешно создан: {output_path}")