import threading
import time
import random
import math
from Tkinter import Tk, Canvas, Frame, BOTH

class DirectPi(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.n_trials = 10000
        self.n_hits = 0
        self.width = 400
        self.height = 400
        self.y = 0
        self.x = self.width
        self.delta = self.width/10
        self.parent = parent
        self.pebbleRadius = 10
        self.timeout = 1.0/3
        self.initUI(self.width, self.height)
        thread = threading.Thread(target=self.startSimulation, args=())
        thread.start()

    def startSimulation(self):
        repeatCounter = 0
        pebbleColorRed = "#f00"
        pebbleColorGreen = "#0f0"
        pebbleColor = pebbleColorRed
        pebble_in = 0
        pebble_out = 0
        for iter in range(self.n_trials):
            del_x, del_y = random.uniform(-self.delta, self.delta), random.uniform(-self.delta, self.delta)
#            if False:
            if ((self.x + del_x) < self.width) and ((self.y + del_y) < self.height) and (self.x + del_x >=0) and (self.y + del_y >=0):
                # pebble inside the square
                repeatCounter = 0
                pebble_in +=1
                self.x += del_x
                self.y += del_y
                print "Pebble IN: (%d, %d) " % (self.x + del_x, self.y + del_y)

                distToCenter = math.sqrt( (self.x - self.width/2)**2 + (self.y -self.height/2)**2 )
                if distToCenter > self.width/2:
                    pebbleColor = pebbleColorRed
                else:
                    pebbleColor = pebbleColorGreen

                self.canvas.create_oval(self.x - self.pebbleRadius,
                                        self.y - self.pebbleRadius, 
                                        self.x + self.pebbleRadius, 
                                        self.y + self.pebbleRadius, 
                                        fill=pebbleColor)

            else:
                repeatCounter += 1
                pebble_out +=1
                print "Pebble out: (%d, %d) " % (self.x + del_x, self.y + del_y)
                self.canvas.create_oval(self.x - self.pebbleRadius,
                                        self.y - self.pebbleRadius - repeatCounter*2, 
                                        self.x + self.pebbleRadius, 
                                        self.y + self.pebbleRadius, 
                                        fill=pebbleColor)

                # pebble outside the square
            time.sleep(self.timeout)

        print "IN: %d    OUT: %d" % (pebble_in, pebble_out)

            # if abs(x + del_x) < 1.0 and abs(y + del_y) < 1.0:
            #     x, y = x + del_x, y + del_y
            # if x**2 + y**2 < 1.0: 
            #     n_hits += 1


        print 4.0 * self.n_hits / float(self.n_trials)
        

    def initUI(self, width, height):      
        self.parent.title("Colors")        
        self.pack(fill=BOTH, expand=1)
        self.canvas = Canvas(self)
        self.canvas.create_oval(0,0, width,height,fill="#fb0", outline="#fb0")
        self.canvas.pack(fill=BOTH, expand=1)



def main():  
    root = Tk()
    directPi = DirectPi(root)
    root.geometry("400x400+200+100")
    root.mainloop()  


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print "exiting.."
        exitapp = True
        raise


