import base64
import os
from datetime import datetime, timezone

BASE62 = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.join(__file__, os.pardir), os.pardir))
png_prefix = 'data:image/jpeg;base64,'
URN_UUID_PREFIX = 'urn:uuid:'

def encode_image(filename):
    with open(filename, "rb") as image_file:
        encoded = base64.b64encode(image_file.read())
        png_str = png_prefix + encoded.decode('utf-8')
        return png_str

def create_iso8601_tz():
    ret = datetime.now(timezone.utc)
    return ret.isoformat()