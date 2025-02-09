import os

utils_dir = os.path.split(os.path.abspath(__file__))[0]
main_dir = os.path.abspath(os.path.join(utils_dir, os.pardir))
data_dir = os.path.join(main_dir, "../assets")
img_dir = os.path.join(data_dir, "img")
font_dir = os.path.join(data_dir, "font")
dogica_path = os.path.join(font_dir, "Dogica_Pixel.ttf")

dark_green = (1, 50, 32)
