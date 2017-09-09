from scipy.misc.pilutil import imread, imshow

from PIL import Image
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from numba.decorators import jit
from skimage.draw.draw import circle_perimeter

import numpy as np


@jit(nopython=True, nogil=True, parallel=False)
def process_pixel(full_image, img_mx, img_my, reference_img):
    ref_xx, ref_yy = reference_img.shape[0:2]
    ii_b = int(img_mx - ref_xx // 2)
    ii_e = int(img_mx + ref_xx // 2 + 1)
    jj_b = int(img_my - ref_yy // 2)
    jj_e = int(img_my + ref_yy // 2)
    return np.sum(np.equal(full_image[ii_b:ii_e, jj_b:jj_e], reference_img))


@jit(nopython=True, nogil=True, parallel=True)
def search_reference_on_image(input_image, reference_image, result):
    xx, yy = input_image.shape[0:2]
    ref_xx, ref_yy = reference_image.shape[0:2]

    for i in xrange(ref_xx // 2, xx - ref_xx // 2):
        for j in xrange(ref_yy // 2, yy - ref_yy // 2):
            result[i, j] = process_pixel(input_image, i, j, reference_image)

BINARY_THRESHOLD = 100
last_image = None
def get_mario_position(ref_img):
    global last_image

    try:
        image = Image.open('/tmp/snapshot.ppm')
        image = np.array(image.resize((256, 256)))
        last_image = image
    except IOError:
        image = last_image

    if image is None:
        return np.zeros(shape=(256, 256))

    gray_image = np.dot(image[..., :3], [0.299, 0.587, 0.114])
    binary_image = np.zeros(shape=gray_image.shape, dtype=bool)
    binary_image[gray_image < BINARY_THRESHOLD] = False
    binary_image[gray_image >= BINARY_THRESHOLD] = True

    result = np.zeros(dtype=int, shape=binary_image.shape)
    search_reference_on_image(binary_image, ref_img, result)
    pike_image = result

    position = np.where(pike_image == np.max(pike_image))
    position = position[0][0], position[1][0]
    image[circle_perimeter(position[0], position[1], 10)] = [255, 0, 0]

    return image

app = QApplication([])
window = QMainWindow()
window.setGeometry(0, 0, 256, 256)

pic = QLabel(window)
pic.setGeometry(0, 0, 256, 256)

class UpdateImageThread(QtCore.QThread):

    def run(self):
        ref_img = np.array(imread('reference.ppm')[:, :, 0], dtype=np.bool)
        while True:
            image = get_mario_position(ref_img)
            image = QtGui.QImage(image, image.shape[1], image.shape[0], 3 * image.shape[1], QtGui.QImage.Format_RGB888)
            pix = QtGui.QPixmap(image)
            pic.setPixmap(pix)
            self.msleep(100)

t = UpdateImageThread()
t.start()

window.show()
app.exec_()
