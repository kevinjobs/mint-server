import os
import cv2


def compress_image(orgin: str, output: str):
    img = cv2.imread(orgin)
    x, y = img.shape[0:2]
    width = 300
    height = int(y / (x / width))
    img2 = cv2.resize(img, (height, width), interpolation=cv2.INTER_NEAREST)
    cv2.imwrite(output, img2)


if __name__ == '__main__':
    files = os.listdir(r'uploads/img')
    for f in files:
        if not os.path.isdir(f):
            origin = 'uploads/img/' + f
            output = 'uploads/img-thumb/' + 'thumb-' + f
            compress_image(origin, output)
