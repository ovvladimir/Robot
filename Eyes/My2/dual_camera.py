# https://docs.python.org/3/library/concurrent.futures.html
from concurrent.futures import ThreadPoolExecutor
import cv2

width = 640  # заданная ширина окна
w, h = (width, int(480 * width / float(640)))


def show(ret, frame, name):
    if ret:
        frame = cv2.resize(frame, (w, h))
        cv2.imshow(name, frame)


def main():
    with ThreadPoolExecutor(max_workers=2) as executor:
        cap1 = cv2.VideoCapture(0)
        cap2 = cv2.VideoCapture(1)

        while True:
            executor.submit(show(*cap1.read(), 'cam1'))
            executor.submit(show(*cap2.read(), 'cam2'))

            if cv2.waitKey(1) == 27:
                break


if __name__ == '__main__':
    main()

'''
cam1 = executor.submit(cap1.read)
cam2 = executor.submit(cap2.read)
c1 = cam1.result()
c2 = cam2.result()
show(*c1, '1')
show(*c2, '2')
'''
