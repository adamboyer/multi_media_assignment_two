from PIL import Image
import os

img = Image.open("Lena.jpg")
width, height = img.size

print("The dimensions of the image are: " + str(width) + " x " + str(height))

# Getting the image size in bytes

with open("Lena.jpg", "rb") as file:
    file_size = os.fstat(file.fileno()).st_size

print("The size of the file is " + str(file_size) + " bytes")

# calculate the original file size
original_file_size = width * height * 3

print("Given that the image is " + str(width) + " x " + str(height) + " where each pixel is 24 bits or 3 bytes,\nThe image should be " + str(original_file_size) + " bytes")

# calculate compression rate
compression_rate = (1 - (file_size / original_file_size)) * 100
print("Now we use this formula (1 -( compressed size / original size)) 100% to get a compresion rate of: " + str(round(compression_rate, 2)))

# create a copy of the image and convert it to YCbCr
ycbcr_img = img.convert("YCbCr")

# get the Y Cb and Cr channels from the converted image
y, cb, cr = ycbcr_img.split()

# scale the Y or brightness by 2
new_y = y.point(lambda x: x * 2)

# merge the new y channel with the old cb and cr channels to create a new image
modified_ycbcr_img = Image.merge("YCbCr", (new_y, cb, cr))

# convert back to RGB and save the image
new_img = modified_ycbcr_img.convert("RGB")
new_img.save("modified_Lena.jpg")

print("The original image has now been converted to YCbCr format, increased the Y channel by a factor of two, converted back to RGB, and finally saved as modified_Lena.jpg")

print("If you open eximine both images, you will notice the modified image is much brighter than the original image")

print("Now we will reduce the Cr to zero and display the new image")

new_cr = cr.point(lambda x: x - x)

no_red_img = Image.merge("YCbCr", (y, cb, new_cr))

new_no_red_img = no_red_img.convert("RGB")

new_no_red_img.save("no_red_Lena.jpg")

new_no_red_img.show()

# now down-sample Cb and Cr channels and then up-sample to see if there is any change
down_sampled_cr = cr.resize((cr.width // 2, cr.height // 2), resample=Image.BICUBIC)
down_sampled_cb = cb.resize((cb.width // 2, cb.height // 2), resample=Image.BICUBIC)

up_sampled_cr = down_sampled_cr.resize((down_sampled_cr.width * 2, down_sampled_cr.height * 2), resample=Image.BICUBIC)
up_sampled_cb = down_sampled_cb.resize((down_sampled_cb.width * 2, down_sampled_cb.height * 2), resample=Image.BICUBIC)

up_sampled_img = Image.merge("YCbCr", (y.resize((up_sampled_cr.width, up_sampled_cr.height), resample=Image.BICUBIC), up_sampled_cb, up_sampled_cr))

up_sampled_img_rgb = up_sampled_img.convert("RGB")

up_sampled_img_rgb.save("cb_cr_down_then_up_sampled_Lena.jpg")

print("Performed down-sampling and then upsampling on Lena.jpb Cr and Cb channels and saved image as cb_cr_down_then_up_sampled_Lena.jpg")

# now also down-sample then up-sample Y channel and see if there is any changes

down_sampled_y = cb.resize((y.width // 2, y.height // 2), resample=Image.BICUBIC)
up_sampled_y = down_sampled_y.resize((down_sampled_y.width * 2, down_sampled_y.height * 2), resample=Image.BICUBIC)

final_img = Image.merge("YCbCr", (up_sampled_y, up_sampled_cb, up_sampled_cr))

final_img_rgb = final_img.convert("RGB")

final_img_rgb.save("all_downsampled_then_upsampled_Lena.jpg")

print('Down-sampled and up-sampled Y, Cr, and Cb channels for Lena.jpg. New image saved as all_downsampled_then_upsampled_Lena.jpg')