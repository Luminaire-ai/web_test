from PIL import Image, ImageDraw, ImageFont
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from scipy import misc
import scipy.ndimage
from skimage import data, color, io, img_as_float

def grayscale(rgb):
	return np.dot(rgb[...,:3], [0.299, 0.587, 0.114])
def dodge(front, back):
		result=front*255/(255-back) 
		result[result>255]=255
		result[back==255]=255
		return result.astype('uint8')
def sigma():
	img = mpimg.imread("input.jpg")
	arr = np.array(img)
	gray = grayscale(img)
	inverted_img = 255-gray
	blur_img = scipy.ndimage.filters.gaussian_filter(inverted_img,sigma=1000)
	final_img = dodge(blur_img, gray)

	plt.imsave('inter.png', final_img, cmap = plt.get_cmap('gray'))

def color_mask(colour_array):
	alpha = 1
	img_temp = Image.open('inter.png')
	img_temp = img_temp.convert('L')
	print(img_temp.mode)

	img = img_as_float(img_temp) 

	rows, cols = img.shape

	color_mask = np.zeros((rows, cols, 3))
	color_mask[0:rows, 0:cols] = colour_array

	img_color = np.dstack((img, img, img))

	img_hsv = color.rgb2hsv(img_color)
	color_mask_hsv = color.rgb2hsv(color_mask)

	img_hsv[..., 0] = color_mask_hsv[..., 0]
	img_hsv[..., 1] = color_mask_hsv[..., 1] * alpha

	img_masked = color.hsv2rgb(img_hsv)
	f, (ax0, ax1, ax2) = plt.subplots(1, 3, subplot_kw={'xticks': [], 'yticks': []})
	plt.imsave('final.png', img_masked)
	plt.close()
