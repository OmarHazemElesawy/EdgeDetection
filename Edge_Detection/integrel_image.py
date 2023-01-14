import matplotlib.pyplot as plt
from PIL import Image
import time


def toArrayAndSquare(im):
    img = [[0 for _ in range(im.size[0])] for _ in range(im.size[1])]
    sqr = [[0 for _ in range(im.size[0])] for _ in range(im.size[1])]
    for i in range(0, im.size[0]):
        for j in range(0, im.size[1]):
            img[j][i] = im.getpixel((i, j))
            sqr[j][i] = img[j][i]**2
    return img, sqr


def applyThreshold(im, th):
    res = [[0 for _ in range(len(im[0]))] for _ in range(len(im))]
    for i in range(0, len(im)):
        for j in range(0, len(im[0])):
            if im[i][j] < th:
                res[i][j] = 0
            else:
                res[i][j] = 255
    return res


def integralArray(img):
    # 𝑠(𝑖,𝑗) = 𝑠(𝑖,𝑗−1) + 𝑓(𝑖,𝑗)
    # 𝑖𝑖(𝑖,𝑗) = 𝑖𝑖(𝑖−1,𝑗) + 𝑠(𝑖,𝑗)
    s = [[0 for _ in range(len(img[0]))] for _ in range(len(img))]
    ii = [[0 for _ in range(len(img[0]))] for _ in range(len(img))]
    for x in range(len(img)):
        for y in range(len(img[0])):
            if y == 0:
                s[x][y] = img[x][y]
            else:
                s[x][y] = s[x][y - 1] + img[x][y]
    for x in range(len(img)):
        for y in range(len(img[0])):
            if x == 0:
                ii[x][y] = s[x][y]
            else:
                ii[x][y] = ii[x - 1][y] + s[x][y]
    return ii


def localSum(img, top_left, bottom_right):
    total = 0
    window_size_x = bottom_right[0] - top_left[0] + 1
    window_size_y = bottom_right[1] - top_left[1] + 1
    total += img[bottom_right[0]][bottom_right[1]] + img[top_left[0] - 1][top_left[1] - 1] - \
        img[bottom_right[0]][bottom_right[1] - window_size_y] - img[bottom_right[0] - window_size_x][bottom_right[1]]
    return total


def imgWithIntegral(img, window_size):
    original_img, squared_img = toArrayAndSquare(img)
    integral_img = integralArray(original_img)
    integral_sqr = integralArray(squared_img)
    # window size is passed as a tuple --> (3,3)
    n = window_size[0] * window_size[1]
    starting_x = window_size[0]//2
    starting_y = window_size[1]//2
    res_img = [[0 for _ in range(img.size[0])] for _ in range(img.size[1])]
    for i in range(starting_x, img.size[0] - starting_x):
        for j in range(starting_y, img.size[1] - starting_y):
            sum_integral = localSum(integral_img, (j - starting_y, i - starting_x), (j + starting_y, i + starting_x))
            sum_squared = localSum(integral_sqr, (j - starting_y, i - starting_x), (j + starting_y, i + starting_x))
            variance = ((1/n) * sum_squared) - ((1/n) * sum_integral)**2
            if variance < 0:
                variance = 0
            res_img[j][i] = variance
    return res_img


def main():
    st = time.time()

    image = (Image.open("sample_image.jpg")).convert("L")
    et_image = time.time()
    print(f"Done with sample image, took {et_image - st} secs")

    img_array, squared_img_array = toArrayAndSquare(image)
    et_arr_conv = time.time()
    print(f"Done with array conversions, took {et_arr_conv - et_image} secs")

    integral_img = integralArray(img_array)
    et_integral = time.time()
    print(f"Done with image integral image, took {et_integral - et_arr_conv} secs")

    integral_img_squared = integralArray(squared_img_array)
    et_squared = time.time()
    print(f"Done with image integral image squared, took {et_squared - et_integral} secs")

    result_img = imgWithIntegral(image, (3, 3))
    et_result_img = time.time()
    print(f"Done with resulting image without thresholding, took {et_result_img - et_squared} secs")

    result_img_threshold = applyThreshold(result_img, 750)
    et_res_thr = time.time()
    print(f"Done with resulting image with thresholding, took {et_res_thr - et_result_img} secs")
    print(f"The process took  {et_res_thr - st} secs in total")

    plt.subplots(nrows=3, ncols=2, figsize=(25, 25))
    plt.subplot(3, 2, 1)
    plt.imshow(img_array, cmap='gray')

    plt.subplot(3, 2, 2)
    plt.imshow(integral_img, cmap='gray')

    plt.subplot(3, 2, 3)
    plt.imshow(squared_img_array, cmap='gray')

    plt.subplot(3, 2, 4)
    plt.imshow(integral_img_squared, cmap='gray')

    plt.subplot(3, 2, 5)
    plt.imshow(result_img, cmap='gray')

    plt.subplot(3, 2, 6)
    plt.imshow(result_img_threshold, cmap='gray')
    plt.show()

# The next bit of code is for testing another image,
# just uncomment the next part  and comment the previous part of the main.

    # st = time.time()
    #
    # image = (Image.open("sample_image_2.jpg")).convert("L")
    # et_image = time.time()
    # print(f"Done with sample image, took {et_image - st} secs")
    #
    # img_array, squared_img_array = toArrayAndSquare(image)
    # et_arr_conv = time.time()
    # print(f"Done with array conversions, took {et_arr_conv - et_image} secs")
    #
    # integral_img = integralArray(img_array)
    # et_integral = time.time()
    # print(f"Done with image integral image, took {et_integral - et_arr_conv} secs")
    #
    # integral_img_squared = integralArray(squared_img_array)
    # et_squared = time.time()
    # print(f"Done with image integral image squared, took {et_squared - et_integral} secs")
    #
    # result_img = imgWithIntegral(image, (3, 3))
    # et_result_img = time.time()
    # print(f"Done with resulting image without thresholding, took {et_result_img - et_squared} secs")
    #
    # result_img_threshold = applyThreshold(result_img, 750)
    # et_res_thr = time.time()
    # print(f"Done with resulting image with thresholding, took {et_res_thr - et_result_img} secs")
    # print(f"The process took  {et_res_thr - st} secs in total")
    #
    # plt.subplots(nrows=3, ncols=2, figsize=(25, 25))
    # plt.subplot(3, 2, 1)
    # plt.imshow(img_array, cmap='gray')
    #
    # plt.subplot(3, 2, 2)
    # plt.imshow(integral_img, cmap='gray')
    #
    # plt.subplot(3, 2, 3)
    # plt.imshow(squared_img_array, cmap='gray')
    #
    # plt.subplot(3, 2, 4)
    # plt.imshow(integral_img_squared, cmap='gray')
    #
    # plt.subplot(3, 2, 5)
    # plt.imshow(result_img, cmap='gray')
    #
    # plt.subplot(3, 2, 6)
    # plt.imshow(result_img_threshold, cmap='gray')
    # plt.show()


main()
