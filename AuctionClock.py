from Tkinter import *
from PIL import Image, ImageTk
import math
import time
import random


class Player:
	
	def __init__(self, name):
		self.name = name
		self.flowers = []
		self.money = [0, 0, 10, 10, 10, 10, 50]
		self.finished = False
		self.computer = True
		self.apparance = None
		self.colour = None

	def add_flower(self, flower):
		self.flowers.append(flower)

	def del_flower(self, flower):
		self.flowers.remove(flower)

	def add_money(self, money):
		self.money.append(money)
	
	def del_money(self, money):
		self.money.remove(money)


class RunAC():
  def __init__(self, root, amount, auctioneer, bidders, imageFile):
    self.master = root
    self.canvas = Canvas(self.master, width = 1000, height = 500)
    self.auctioneer = auctioneer
    self.bid = False
    self.angle = 0.5 * math.pi
    self.amount = amount
    self.startValue = amount
    self.bidders = bidders
    self.bidder = random.choice([bidder for bidder in bidders if bidder.computer and sum(bidder.money) > 0])
    self.image = Image.open(imageFile)
    self.maxBid = sum(self.bidder.money)
    self.opponentAmount = random.randrange(0, self.maxBid, 10)
    self.bidAmount = 0 
    self.canvas.pack()
    self.constructClock(True)
    self.createMarkingPoint()

    if self.auctioneer.computer:
    	self.createButton()

    self.showAmount()	

    root.after(250, self.next_tick)
    root.wait_window(self.canvas)

  def setBid(self):
    self.bid = True

  def createButton(self):
    button = Button(self.canvas, text = "Bid!", command = self.setBid)

    self.canvas.create_window(500, 350, window = button)
    return


  def showImage(self):
    image = self.image.resize((100, 100), Image.ANTIALIAS)	
    photo = ImageTk.PhotoImage(image)
		
    self.master.one = photo
    self.canvas.create_image(500, 250, image = photo)


  def showAmount(self):
    self.canvas.create_text(500, 150, text = str(self.amount))
    return


  def calculateCoordinatesCircle(self, r):
	x = 500 + r * math.cos(self.angle)
	y = 250 - r * math.sin(self.angle)

	return x, y


  def createMarkingPoint(self):
    x, y = self.calculateCoordinatesCircle(182)

    self.canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill="yellow")   
    return


  def createNumbers(self):
    val = self.startValue
    numberOfNumbers = val / 50
    diff = 2.0 / numberOfNumbers * math.pi
    angle = 0.51 * math.pi #The calculations are made with the angle from the positive x-axis is the beginpoint first put on a half-pi, because the pointer from above is running. Subsequently, here is 0:01 pi added, because the 100 must be above the first compartment, and not above the separation line.

    for i in range(numberOfNumbers):
        x1 = 500 + 225 * math.cos(angle)
        x2 = 250 - 225 * math.sin(angle)

        self.canvas.create_text(x1, x2, text = str(val))
        angle += diff
        val -= 50

    return


  def createLines(self):
    #print "creating lines"
    numberOfLines = self.startValue / 10
    diff = 2.0 / numberOfLines * math.pi

    for i in range(numberOfLines):
      x1, y1 = self.calculateCoordinatesCircle(200) 
      x2, y2 = self.calculateCoordinatesCircle(175)

      self.canvas.create_line(x1, y1, x2, y2)
      self.angle += diff

    return


  def constructClock(self, first_time):
    self.canvas.create_oval(300, 50, 700, 450, fill="lightblue")
    self.canvas.create_oval(310, 60, 690, 440, fill="red")
    self.canvas.create_oval(325, 75, 675, 425, fill="white") 	   
    self.createLines()

    if first_time:#    self.opponents = opponents

      self.createNumbers()

    return


  def next_tick(self):
     update_wait = 250 # millisecondsb
     numberOfMarkingPoints = self.startValue / 10
     self.angle += 2.0 / numberOfMarkingPoints * math.pi

     if self.amount == 0:
       self.canvas.create_text(700, 50, text = "Nobody even wants it for free !!!!")
       self.canvas.after(5000, self.canvas.destroy)

     elif self.amount == self.opponentAmount:      
       self.bidAmount = self.opponentAmount

       self.canvas.create_text(700, 50, text = "Once again sold for " + str(self.amount) + " to " + self.bidder.name  + "!")
       self.canvas.after(5000, self.canvas.destroy)
	 
     elif self.bid:
       self.bidAmount = self.amount

       for bidder in self.bidders:
		if bidder.computer == False:
			self.bidder = bidder			

       self.canvas.create_text(700, 50, text = "Once again sold for " + str(self.amount) + " to " + self.bidder.name  + "!")
       self.canvas.after(5000, self.canvas.destroy)

     else:
       self.amount = max(0, self.amount - 10)

       self.constructClock(False)
       self.createMarkingPoint()
       self.showAmount()
       self.showImage()
       self.master.after(update_wait, self.next_tick)


########################################################

def choosePlayer(bidders, name):
	for bidder in bidders:
		if bidder.name == name:
			bidder.computer = False
			return

	print "Bidder not in list!"
	return


def giveHighestBidder(auctionClock, bidders):
	if auctionClock.bidAmount == 0:
		return None

	if auctionClock.bid:
		for bidder in bidders:
			if bidder.computer == False:
				return bidder

	return auctionClock.bidder

if __name__ == '__main__':
	root = Tk()
	auctioneer = Player("Machteld")
	bidders = [Player("Johannes"), Player("Pieter"), Player("Maria")]

	choosePlayer(bidders, "Johannes")
	RunAC(root, 100, auctioneer, bidders, "fleur.jpg")
	root.destroy()
	root.mainloop()



