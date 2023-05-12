import os
import multiprocessing
from PIL import Image

def is_corrupted(path):
    try:
        with Image.open(path) as img:
            img.verify()
        return False
    except:
        return True

def check_images(path):
    corrupted = []
    for dirpath, _, filenames in os.walk(path):
        for filename in filenames:
            if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.jp2', '.tif', '.tiff')):
                img_path = os.path.join(dirpath, filename)
                if is_corrupted(img_path):
                    corrupted.append(img_path)
    return corrupted

if __name__ == '__main__':
    path = input("Enter the path where the images are located: ")
    num_processes = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(processes=num_processes)
    results = []

    for root, dirs, files in os.walk(path):
        for directory in dirs:
            dir_path = os.path.join(root, directory)
            result = pool.apply_async(check_images, [dir_path])
            results.append(result)

    pool.close()
    pool.join()

    corrupted_images = []
    for result in results:
        corrupted_images.extend(result.get())

    if len(corrupted_images) == 0:
        print("No corrupted images found.")
    else:
        print("Corrupted images num: " + (str(len(corrupted_images))))
        print("Corrupted images found:")
        for img_path in corrupted_images:
            print(img_path)