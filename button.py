from timeit import timeit
import pygame
from utils import *

class Button:
	def __init__(self,text,text_size,event,width,height,pos,screen,colorA=WHITE,colorB=BLUE,text_switch=[],event_args=()):
		"""Creation of a button

		Args:
			text (string): text first displayed
			text_size (int): fond size
			event (func): function called on click
			width (int): width of the button
			height (int): height of the button
			pos (list(int,int)): position of the button on the screen (x,y)
			screen (SCREEN): screen on which the button will be displayed
   
			colorA (tuple(int,int,int), optional): primary color. Defaults to WHITE.
			colorB (tuple(int,int,int), optional): secondary color. Defaults to BLUE.
				when the button is hovered or clicked primary and secondary colors swap place
   
			text_switch (list(string), optional): when the button is clicked the text change s
   				uccessively with those in this list and then go back to the original one etc. Defaults to [].
			event_args (tuple()): args given to event. Default to ()
		"""
		#Core attributes
		self.font = pygame.font.Font("assets/fonts/FredokaOne-Regular.ttf", text_size)
		self.screen=screen
		self.pressed = False
		self.elevation = 5
		self.dynamic_elecation = self.elevation
		self.original_y_pos = pos[1]
		self.color1=colorA
		self.color2=colorB        
		# top rectangle 
		self.top_rect = pygame.Rect(pos,(width,height))
		self.top_color = self.color1
  
		#event triggered
		self.event = event
		self.event_args = event_args
	
		# bottom rectangle 
		self.bottom_rect = pygame.Rect(pos,(width,height))
		self.bottom_color = '#354B5E'
		#text
		self.nb_switch = len(text_switch)+1
		self.switch_counter = min(1,len(text_switch))
		self.all_switch = [text]
		self.all_switch.extend(text_switch)
  
		self.text = text
		self.text_color = self.color2

		self.text_surf = self.font.render(text,True,self.text_color)
		self.text_rect = self.text_surf.get_rect(center = self.top_rect.center)

	def draw(self):
		"""display the button on the screen
		"""
		#elevation logic 
		self.top_rect.y = self.original_y_pos - self.dynamic_elecation
		self.text_rect.center = self.top_rect.center 

		self.bottom_rect.midtop = self.top_rect.midtop
		self.bottom_rect.height = self.top_rect.height + self.dynamic_elecation

		#draw both rectangle
		pygame.draw.rect(self.screen,self.bottom_color, self.bottom_rect,border_radius = 12)
		pygame.draw.rect(self.screen,self.top_color, self.top_rect,border_radius = 12)
		
		#display the text inside
		self.text_surf = self.font.render(self.text,True,self.text_color)
		self.text_rect = self.text_surf.get_rect(center = self.top_rect.center)
		self.screen.blit(self.text_surf, self.text_rect)
		self.check_click()

	def check_click(self):
		"""handle mouse click and cursor collisison with the button
		"""
		#get mouse position
		mouse_pos = pygame.mouse.get_pos()

		#check if the cursor hovers the button
		if self.top_rect.collidepoint(mouse_pos):
			
			#chnage color to show that the cursor is hovering the button
			self.top_color = self.color1
			self.text_color=self.color2

			#if clicked, the button get pressed down with a dynamic animation
			if pygame.mouse.get_pressed()[0]:
				self.dynamic_elecation = 0
				self.pressed = True
			else:
				self.dynamic_elecation = self.elevation
				if self.pressed == True:
					self.pressed = False

					#update text
					self.text = self.all_switch[self.switch_counter]
					self.switch_counter = (self.switch_counter+1)%self.nb_switch 
					
     				#trigger event
					self.event(*self.event_args)
		else:
			#reset the colors and button animation
			self.dynamic_elecation = self.elevation
			self.top_color = self.color2
			self.text_color=self.color1
   
