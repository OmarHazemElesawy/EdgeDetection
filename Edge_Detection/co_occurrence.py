import matplotlib.pyplot as plt
from PIL import Image
import time

image = (Image.open("sample_image.jpg")).convert("L")

# The next line of code is for testing another image.
# image = (Image.open("sample_image_2.jpg")).convert("L")


def toArrayAndSquare(im):
    img = [[0 for _ in range(im.size[0])] for _ in range(im.size[1])]
    sqr = [[0 for _ in range(im.size[0])] for _ in range(im.size[1])]
    for i in range(0, im.size[0]):
        for j in range(0, im.size[1]):
            img[j][i] = im.getpixel((i, j))
            sqr[j][i] = img[j][i]**2
    return img, sqr


def calculateCooccurrence():
    img, sqr = toArrayAndSquare(image)
    horizontal = [[0] * 256 for _ in range(256)]
    vertical = [[0] * 256 for _ in range(256)]
    for x in range(len(img) - 1):
        for y in range(len(img[0]) - 1):
            i = img[x][y]
            j = img[x][y+1]
            z = img[x+1][y]
            horizontal[i][z] += 1
            vertical[i][j] += 1
    return vertical, horizontal


def nullifyPixels(matrix):
    res = [[0 for _ in range(len(matrix[0]))] for _ in range(len(matrix))]
    for x in range(len(matrix)):
        for y in range(len(matrix[0])):
            if abs(x - y) < 30:
                res[x][y] = 0
            else:
                res[x][y] = matrix[x][y]
    return res


def imgWithCooccurrence(v_matrix_null, h_matrix_null):
    result = Image.new('L', (image.size[0], image.size[1]))
    for x in range(image.size[0] - 1):
        for y in range(image.size[1] - 1):
            i = image.getpixel((x, y))
            j = image.getpixel((x, y + 1))
            z = image.getpixel((x + 1, y))
            if v_matrix_null[i][z] != 0 or h_matrix_null[i][j] != 0:
                result.putpixel((x, y), 255)
    return result


def main():
    st = time.time()

    v_matrix, h_matrix = calculateCooccurrence()
    v_matrix_null = nullifyPixels(v_matrix)
    h_matrix_null = nullifyPixels(h_matrix)
    res_image = imgWithCooccurrence(v_matrix_null, h_matrix_null)

    et = time.time()
    print(f"The process took  {et - st} secs in total")
    plt.subplots(nrows=3, ncols=2, figsize=(25, 25))
    plt.subplot(3, 2, 1)
    plt.imshow(image, cmap='gray')

    plt.subplot(3, 2, 2)
    plt.imshow(res_image, cmap='gray')

    plt.subplot(3, 2, 3)
    plt.imshow(v_matrix, cmap='gray')

    plt.subplot(3, 2, 4)
    plt.imshow(v_matrix_null, cmap='gray')

    plt.subplot(3, 2, 5)
    plt.imshow(h_matrix, cmap='gray')

    plt.subplot(3, 2, 6)
    plt.imshow(h_matrix_null, cmap='gray')
    plt.show()


main()
