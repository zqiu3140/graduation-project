from PIL import Image
from datetime import datetime
def get_date_from_image(image_path):
    try:
        image = Image.open(image_path)
        exif_data = image._getexif()
        if exif_data:
            for tag, value in exif_data.items():
                if tag == 36867:  # 'DateTimeOriginal'
                    date_str = value.split(' ')[0].replace(':', '-')
                    return datetime.strptime(date_str, '%Y-%m-%d').date()
        return None
    except Exception as e:
        print(f"Error processing {image_path}: {e}")
        return None