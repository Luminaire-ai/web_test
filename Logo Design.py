import numpy as np
import random 
from PIL import Image, ImageDraw, ImageFont
import os.path
import sys
import importlib

moduleName = "transparency_tool"
transparency_tool = importlib.import_module(moduleName)

def get_img_dir() -> str:
    pkg_dir = os.path.dirname(__file__)
    return pkg_dir

def circle():
	image = Image.new('RGBA', (800, 800))
	draw = ImageDraw.Draw(image)
	draw.ellipse((20, 20, 780, 780),  outline ='blue')
	return image
def square():
	image = Image.new('RGBA', (800, 800))
	draw = ImageDraw.Draw(image)
	draw.rectangle(((10, 10), (790, 790)), fill="black")
	return image
def oval():
	image = Image.new('RGBA', (800, 400))
	draw = ImageDraw.Draw(image)
	x, y =  image.size
	eX, eY = 790, 390 
	bbox =  (x/2 - eX/2, y/2 - eY/2, x/2 + eX/2, y/2 + eY/2)
	draw.ellipse(bbox,  outline ='blue')
	return image
def rectangle():
	image = Image.new('RGBA', (800, 400))
	draw = ImageDraw.Draw(image)
	draw.rectangle((10,10,790,390),  outline ='blue')
	return image



class Logo:
	def __init__(self, shape, colour, position, font_size, font_style): #Create a logo object
		self.shape = shape
		self.colour = colour
		self.position = position
		self.font_size = font_size
		self.font_style = font_style
	def __str__(self):
		return str([self.shape, self.colour, self.position, self.font_size, self.font_style])
	def __eq__(self, other):
		return self.__dict__ == other.__dict__
	def return_val(self):
		return str([self.shape, self.colour, self.position, self.font_size, self.font_style])
	def logo_maker():
		shape_arr = (random.randint(0,len(shapes)-1))
		colour_arr = (random.randint(0,len(colours)-1))
		position_arr = (random.randint(0,len(positions)-1))
		font_size_arr = (random.randint(0,len(description_font_size)-1))
		font_style_arr = (random.randint(0,len(description_font_style)-1))
		combination = Logo(shapes[shape_arr], colours[colour_arr], positions[position_arr], description_font_size[font_size_arr], description_font_style[font_style_arr])
		return combination

class Combinations: 
	def __init__(self, samples): #Declare the number of Logo objects you want to create
		self.combinations = []
		self.samples = samples
		for item in range(samples):
			combination = Logo.logo_maker()
			print(self.duplicate_checker(combination))
			while self.duplicate_checker(combination) == False:
				combination = Logo.logo_maker()
			self.combinations.append(combination)
	def __str__(self): #Print all items inside combinations object
		disp_list = []
		for item in self.combinations:
			disp_list.append(item.return_val())
		return str(disp_list)
	def duplicate_checker(self, combination):
		for combo in self.combinations:
			if combo == combination:
				return False
			else:
				return True
	def render_images(self): #Render images stored inside combinations object
		transparency_tool.sigma()
		 #Create masked logos
		for index, item in enumerate(self.combinations):			
			if item.shape == 'Rectangle':
				loc = Rectangle_position[item.position]
				image = rectangle()
			elif item.shape == 'Square':
				loc = Square_position[item.position]
				image = square()
			elif item.shape == 'Circle':
				loc = Circle_position[item.position]
				image = circle()
			elif item.shape == 'Oval':
				loc = Oval_position[item.position]
				image = oval()
			width, height = image.size
			center = (int(0.5 * width), int(0.5 * height))
			fill_colour = colors_dict[item.colour]
			ImageDraw.floodfill(image, xy=center, value=fill_colour)
			colour_array = colors_dict[item.colour][0:3]
			colour_array = [x / 255 for x in colour_array]
			transparency_tool.color_mask(colour_array)
			logo_pic = Image.open('final.png')
			width1, height1 = logo_pic.size
			ratio = height1/width1
			height1 = image.height - 30
			if item.shape=='Circle':
				height1 = image.height-150
			width1 = height1/ratio
			logo_pic = logo_pic.resize((int(width1), int(height1)))
			image.paste(logo_pic, (int(image.width/2-(logo_pic.width/2)), int(image.height/2-(logo_pic.height/2))))
			draw = ImageDraw.Draw(image)	
			input_logo = os.path.join(get_img_dir(), "Premier Logo.png")
			logo = Image.open(input_logo)
			image.paste(logo, loc, logo)
			font_address = str(os.path.join("Fonts", item.font_style + ".ttf"))
			font = ImageFont.truetype(font_address, item.font_size)
			x, y = loc
			y+=95
			loc_draw = (x,y)
			draw.text(loc_draw, "Special Face Tissue", fill = (255,255,255,255), font=font)
			file_name = str(index + 1).zfill(4)
			output_img = os.path.join(get_img_dir(),'static','img', 'Premier Logos',file_name + ".png")
			image.save(output_img)
			print(str(index + 1))
			print(item)


#List of available descriptions
shapes = ['Rectangle', 'Square', 'Circle', 'Oval']
colours = ['red', 'orange', 'green', 'blue', 'pink', 'purple']
positions = ['top-left', 'top-right', 'bottom-left', 'bottom-right', 'center']
description_font_style = ['Times New Roman', 'Arial', 'Comic Sans MS']
description_font_size = [15,17,19,21,23,25,27,29,31,33,35]
colors_dict = {'red': (255,0,0,255), 'orange': (255,119,0,255) ,'green': (0,255,0,255), 'blue': (0,0,255,255), 'pink': (255,0,230,255), 'purple': (162,0,255,255)}

#Text Positions Relative to Shape
Oval_position = {'top-left': (120,60), 'top-right': (225,60), 'bottom-left': (120, 195), 'bottom-right': (225,195), 'center': (173,128)}
Rectangle_position = {'top-left': (30,30), 'top-right': (350,30), 'bottom-left': (30,260), 'bottom-right': (350,260), 'center': (190, 145)}
Circle_position = {'top-left': (140, 110), 'top-right': (225,110), 'bottom-left': (220, 550), 'bottom-right': (250, 550), 'center': (190,330)}
Square_position = {'top-left': (50, 50), 'top-right': (330,50), 'bottom-left': (50,600), 'bottom-right': (330,600), 'center': (190,325)}

combo = Combinations(500)
combo.render_images()
