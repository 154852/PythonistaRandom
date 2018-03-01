import random
from scene import *
import threading, time, math

r = 10
loops = 15000
refresh = 1

def getData():
	results = [0 for i in range(r)]
	
	for i in range(loops):
		results[random.randint(0,r)-1] += 1
		
	percent = loops / 100
	percentages = []
	for i in range(len(results)):
		percentages.append(results[i] / percent)
		
	return percentages
	
class Visual(Scene):
	def setup(self):
		self.background_color = '#0000a3'
		
		self.updates = 0
		self.gap = self.size.w / r
		self.width = 20
		self.start = self.gap / 2
		self.biggest = 0
		
		self.bigDot = ShapeNode(ui.Path.rounded_rect(0, 0, ((self.gap - self.width) / 3) * 2, 6, 5), '#00af00')
		self.add_child(self.bigDot)
		self.smallDot = ShapeNode(ui.Path.rounded_rect(0, 0, ((self.gap - self.width) / 3) * 2,6,5), '#ff4300')
		self.smallDot.position = 0, math.inf
		self.add_child(self.smallDot)
		self.avgDot = ShapeNode(ui.Path.rounded_rect(0, 0, ((self.gap - self.width) / 3) * 2, 6, 5), 'white')
		self.add_child(self.avgDot)
		
		self.info = LabelNode('', ('futura', 25))
		self.info.position = self.size.w/2, (self.size.h/2) + 150
		self.add_child(self.info)
		self.highLowData = {'highest': 0, 'lowest': math.inf, 'average': 0}
		self.infoShown = 0
		
		label = LabelNode('\'Random\' results by Python ' + sys.version.split(' ')[0])
		label.font = ('futura', 30)
		label.position = (self.size.w/2, self.size.h - 50)
		self.add_child(label)
		
		self.create()
		
	def update(self):
		if self.updates > -1:
			self.updates+=1
			if self.updates % refresh == 0:
				self.reset()
				self.create()
		if time.time() - self.infoShown > 3:
			self.info.text = ''
			
	def reset(self):
		for item in self.items:
			item.remove_from_parent()
			
	def touch_began(self, touch):
		r = 25
		touchRect = Rect(touch.location.x - r, touch.location.y - r, r*2, r*2)
		if touchRect.intersects(self.avgDot.frame):
			self.info.text = 'Average Data: ' + str(self.highLowData['average']) + '%'
			self.infoShown = time.time()
		elif touchRect.intersects(self.bigDot.frame):
			self.info.text = 'Highest Recorded Point: ' + str(self.highLowData['highest']) + '%'
			self.infoShown = time.time()
		elif touchRect.intersects(self.smallDot.frame):
			self.info.text = 'Lowest Recorded Point: ' + str(self.highLowData['lowest']) + '%'
			self.infoShown = time.time()
		else:
			self.updates = -1
			self.reset()
			self.create()
		
	def create(self):
		self.items = []
		percentages = getData()
		font = ('futura', 15)
		
		max = 0
		min = math.inf
		avg = 0
		for item in percentages:
			if item > max:
				max = item
			if item < min:
				min = item
			avg += item
		avg /= len(percentages)
		avg = (avg + self.highLowData['average']) / 2
		self.highLowData['average'] = round(avg, 2)
		
		self.avgDot.position = 0, ((avg / 100) * (self.size.h * 0.8)) + 50
		
		for i in range(len(percentages)):
			x = (self.gap * i) + self.start
			y = (percentages[i] / 100) * (self.size.h * 0.8)
			
			if percentages[i] == max:
				col = '#00af00'
			elif percentages[i] == min:
				col = '#ff4300'
			else:
				col = 'white'
			
			if y + 50 > self.bigDot.position.y:
				self.bigDot.position = 0, y + 50
				self.highLowData['highest'] = round(percentages[i], 2)
			if y + 50 < self.smallDot.position.y:
				self.smallDot.position = 0, y + 50
				self.highLowData['lowest'] = round(percentages[i], 2)
				
			line = ShapeNode(ui.Path.rounded_rect(0, 0, self.width, y, 5))
			line.position = (x, (y / 2) + 50)
			line.color = col
			self.add_child(line)
			self.items.append(line)
			label = LabelNode(str(round(i, 2)))
			label.font = font
			label.position = (x, 25)
			label.color = col
			self.add_child(label)
			self.items.append(label)
			label = LabelNode(str(round(percentages[i], 2)) + '%')
			label.font = font
			label.position = (x, y + 75)
			label.color = col
			self.add_child(label)
			self.items.append(label)
			
run(Visual(), show_fps=True)
