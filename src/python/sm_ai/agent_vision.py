from scipy.misc.pilutil import imread, imshow

from PIL import Image
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from numba.decorators import jit
from skimage.draw.draw import circle_perimeter
import numba

import numpy as np


@jit(nopython=True, nogil=True, parallel=False)
def process_pixel(full_image, reference_img, img_mx, img_my, ref_xx, ref_yy):
    ii_b = img_mx - ref_xx // 2
    ii_e = img_mx + ref_xx // 2 + 1
    jj_b = img_my - ref_yy // 2
    jj_e = img_my + ref_yy // 2
    return np.sum(np.equal(full_image[ii_b:ii_e, jj_b:jj_e], reference_img))


@jit(nopython=True, nogil=True, parallel=True)
def search_reference_on_image(input_image, reference_image):
    xx, yy = input_image.shape
    ref_xx, ref_yy = reference_image.shape

    i_begin = ref_xx // 2
    i_end = xx - i_begin
    j_begin = ref_yy // 2
    j_end = yy - j_begin
    result = np.zeros(shape=input_image.shape, dtype=np.int32)
    for i in numba.prange(i_begin, i_end):
        for j in range(j_begin, j_end):
            result[i, j] = process_pixel(input_image, reference_image, i, j, ref_xx, ref_yy)
    return result

BINARY_THRESHOLD = 100
last_image = None
def get_environment_snapshot():
    global last_image
    try:
        image = Image.open('/tmp/snapshot.ppm')
        image = np.array(image.resize((256, 256)))
        last_image = image
    except IOError:
        image = last_image

    if image is None:
        return np.zeros(shape=(256, 256))

    return image


def get_binary_image(image):
    gray_image = np.dot(image[..., :3], [0.299, 0.587, 0.114])
    binary_image = np.zeros(shape=gray_image.shape, dtype=bool)
    binary_image[gray_image < BINARY_THRESHOLD] = False
    binary_image[gray_image >= BINARY_THRESHOLD] = True
    return binary_image


def get_artifact_position(binary_image, ref_img, n_artifacts=1):
    pike_image = search_reference_on_image(binary_image, ref_img)
    position = np.where(pike_image == np.max(pike_image))
    position = position[0][0], position[1][0]
    return position

app = QApplication([])
window = QMainWindow()
window.setGeometry(0, 0, 256, 256)

pic = QLabel(window)
pic.setGeometry(0, 0, 256, 256)

class UpdateImageThread(QtCore.QThread):

    def run(self):
        mario_head_ref_img = np.array(imread('mario_head.ppm')[:, :, 0], dtype=np.bool)
        block_ref_img = np.array(imread('block.ppm')[:, :, 0], dtype=np.bool)

        while True:
            env_snap = get_environment_snapshot()
            binary_image = get_binary_image(env_snap)
            mario_position = get_artifact_position(binary_image, mario_head_ref_img)
            block_positions = get_artifact_position(binary_image, block_ref_img)

            env_snap[circle_perimeter(mario_position[0], mario_position[1], 10)] = [255, 0, 0]
            env_snap[circle_perimeter(block_positions[0], block_positions[1], 5)] = [0, 0, 255]

            with open('/tmp/vision.txt', 'w') as f:
                f.write('%s,%s\n' % (mario_position[0], mario_position[1]))
                f.write('%s,%s' % (block_positions[0], block_positions[1]))

            image = QtGui.QImage(env_snap, env_snap.shape[1], env_snap.shape[0], 3 * env_snap.shape[1], QtGui.QImage.Format_RGB888)
            pix = QtGui.QPixmap(image)
            pic.setPixmap(pix)
            self.msleep(100)

t = UpdateImageThread()
t.start()

window.show()
app.exec_()
