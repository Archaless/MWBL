import numpy as np
import cv2
import sys

def main():
    args  = sys.argv[1:] # argv[0] is the script name
    if len(args) < 1:
        files = ['imgRAW.bin']
    else:
        files = args
    print(files)
    for filename in files:
        print('Converting file: ' + filename)
        w, h = 640, 512   # change to your size
        img = np.fromfile(filename, dtype=np.uint16)
        img = img.reshape((h, w))

        # Normalize to 8-bit
        img8 = cv2.normalize(img, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
        filePath = filename[0:-4] + ".jpg"
        print('Saving to:' + filePath)
        cv2.imwrite(filePath, img8)
    return 0

if __name__ == "__main__":
    main()