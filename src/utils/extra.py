import random
import os

def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def upload_post_image_path(instace, filename):
    new_filename = random.randint(1, 99999999999)
    name, ext = get_filename_ext(filename)
    final_filename = f"{new_filename}{ext}"
    return f"post/{new_filename}/{final_filename}"
