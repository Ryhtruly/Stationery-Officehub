import cloudinary
import cloudinary.uploader

cloudinary.config(
    cloud_name='dpbfb6hai',
    api_key='536479469775784',
    api_secret='LXFgaRYj07-SAWCAcCzu9OcbgSo',
    secure=True
)

def upload_image(file):
    try:
        result = cloudinary.uploader.upload(file)
        return result.get('secure_url')
    except Exception as e:
        print(f"Upload error: {e}")
        return None
