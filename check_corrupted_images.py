import glob
from multiprocessing import Pool
from PIL import Image
from pprint import pprint

def check_one(f):
    try:
        im = Image.open(f)
        im.verify()
        im.close()
        #  Debug:print(f"OK: {f}")
        return
    except (IOError, OSError, Image.DecompressionBombError):
        #  Debug:print(f"Fail: {f}")
        return f

if __name__ == "__main__":
    p = Pool()
    files = [f for f in glob.glob('**/*.jpg',recursive=True)]
    num_files = len(files)
    result = p.map(check_one, files)
    result = list(filter(None, result))
    print(f'Num files total: {len(files)}')
    print(f'Num files corrupted: {len(result)}')
    pprint(f'Corrupted files:\n {str(sorted(result))}')