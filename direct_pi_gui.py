import threading
import time
import random
import math
from Tkinter import Tk, Canvas, Frame, BOTH

exitapp=False

class DirectPi(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.exiting = False
        self.n_trials = 10000
        self.n_hits = 0
        self.width = 400
        self.height = 400
        self.parent = parent
        self.pebbleRadius = 3
        self.initUI(self.width, self.height)
        self.thread = threading.Thread(target=self.startSimulation, args=())
        self.thread.start()

    def exit(self):
        self.exiting = True
        self.thread.stop()
        print "Exiting from DirectPi"

    def startSimulation(self):
        for iter in range(self.n_trials):
            if self.exiting: break


            # calculate coords for the pebble (origin is the center of the circle)
            x, y = random.uniform(-self.width/2, +self.width/2), random.uniform(-self.height/2, +self.height/2)

            if x**2 + y**2 < (self.width/2)**2:
                pebbleColor = "#0f0"
                self.n_hits += 1
            else:
                pebbleColor = "#f00"

            self.canvas.create_oval(self.width/2 + x - self.pebbleRadius,
                                    self.width/2 + y - self.pebbleRadius, 
                                    self.height/2 + x + self.pebbleRadius, 
                                    self.height/2 + y + self.pebbleRadius, 
                                    fill=pebbleColor)

        print 4.0 * self.n_hits / float(self.n_trials)
        

    def initUI(self, width, height):
        self.parent.title("Colors")
        self.pack(fill=BOTH, expand=1)
        self.canvas = Canvas(self)
        self.canvas.create_oval(0,0, width, height, fill="#fb0", outline="#fb0")
        self.canvas.pack(fill=BOTH, expand=1)


def main():
    root = Tk()
    try:
        directPi = DirectPi(root)
        root.geometry("400x400+200+100")
        root.mainloop()
    except KeyboardInterrupt:
        directPi.exit()
        print "exiting.."
        exitapp = True


if __name__ == '__main__':
    main()


