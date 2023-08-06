from PIL import Image

up = Image.open("images/circle.png")
img_bg = Image.open("images/bg.jpg")

upResize = up.resize((100,100))
img_bg.paste(upResize, (100, 100), upResize)

img_bg.save('images/img2.png')

img_1 = Image.open('images/img1.png')
img_2 = Image.open('images/img1.png')

img1 = img_1.convert('RGB')
img2 = img_2.convert('RGB')

image_list=[img2, img1]


img_bg.save('images/test.pdf', 'PDF',save_all=True, append_images=image_list)