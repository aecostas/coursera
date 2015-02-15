import threading
import time
import random
import math
from Tkinter import Tk, Canvas, Frame, BOTH

class PebbleGame(Frame):
    UP=0
    RIGHT=1
    DOWN=2
    LEFT=3

    MOVEMENTS_STR = ["UP", "RIGHT", "DOWN", "LEFT"]
    MOVEMENTS_ROW_STEPS = [-1, 0, 1, 0]
    MOVEMENTS_COL_STEPS = [0, 1, 0, -1]

    def __init__(self, parent):
        Frame.__init__(self, parent)
        dimensionality = 4
        self.margin = 10
        self.width = 400
        self.height = 400
        self.tk_counter = {}
        self.currentRow = 0
        self.currentCol = dimensionality-1
        self.parent = parent
        self.timeout = 1.0/6
        self.initMatrix(dimensionality)
        self.initUI(self.width, self.height,dimensionality)
        thread = threading.Thread(target=self.startSimulation, args=([dimensionality]))
        thread.start()


    def initMatrix(self, dim):
        self.matrix = {}
        for row in range(dim):
            self.matrix[row] = {}
            for col in range(dim):
                self.matrix[row][col] = {}
                self.matrix[row][col]["probability"] = 1
                self.matrix[row][col]["counter"] = 0



    def startSimulation(self, dimensionality):
        repeatCounter = 0
        pebbleColorRed = "#f00"
        pebbleColorGreen = "#0f0"
        pebbleColor = pebbleColorRed
        pebble_in = 0
        pebble_out = 0
        time.sleep(self.timeout)

        self.ball = self.canvas.create_oval((dimensionality-1) *self.width/dimensionality + self.margin, 
                                            0 + self.margin, 
                                            self.width - self.margin,
                                            self.height/dimensionality - self.margin, 
                                            fill="#f00",
                                            outline="#f00")

        while True:
            # 1-> up; 2-> right; 3->down; 4->left
            movementDirection = random.randint(0,3)
            if ((self.currentRow == 0 and movementDirection==PebbleGame.UP) or
                ((self.currentRow == dimensionality-1) and movementDirection==PebbleGame.DOWN) or
                (self.currentCol == 0 and movementDirection==PebbleGame.LEFT) or
                ((self.currentCol == dimensionality-1) and movementDirection==PebbleGame.RIGHT)):
                print "Discarting movement from (%d, %d) to the %s" % (self.currentRow, self.currentCol, PebbleGame.MOVEMENTS_STR[movementDirection])
            else:
                print "Moving: ROW: %d      COL: %d" % (PebbleGame.MOVEMENTS_ROW_STEPS[movementDirection], PebbleGame.MOVEMENTS_COL_STEPS[movementDirection])
                self.canvas.move(self.ball, 
                                 PebbleGame.MOVEMENTS_COL_STEPS[movementDirection] * self.height/dimensionality, 
                                 PebbleGame.MOVEMENTS_ROW_STEPS[movementDirection] * self.width/dimensionality)

                self.currentRow += PebbleGame.MOVEMENTS_ROW_STEPS[movementDirection]
                self.currentCol += PebbleGame.MOVEMENTS_COL_STEPS[movementDirection]
                self.matrix[self.currentRow][self.currentCol]["probability"] += 1
                
                self.canvas.itemconfig(
                    self.tk_counter[self.currentRow][self.currentCol],
                    text="%d"%(self.matrix[self.currentRow][self.currentCol]["probability"])
                )
                    

                print "Current: (%d, %d) " % (self.currentRow, self.currentCol)

            time.sleep(self.timeout )
                
    def initUI(self, width, height, dimensionality):
        margin = 10
        self.parent.title("Pebble Game")
        self.pack(fill=BOTH, expand=1)
        self.canvas = Canvas(self)

        for line in range(dimensionality-1):
            self.canvas.create_line(self.width/dimensionality + line*self.width/dimensionality,
                                    0, 
                                    self.width/dimensionality + line*self.width/dimensionality,
                                    self.height)

            self.canvas.create_line(0,
                                    self.height/dimensionality + line*self.height/dimensionality , 
                                    self.height, 
                                    self.height/dimensionality + line*self.height/dimensionality )

        for row in range(dimensionality):
            self.tk_counter[row] = {}
            for col in range(dimensionality):
                self.tk_counter[row][col] = self.canvas.create_text((col+1)*self.width/dimensionality - 10, 
                                                               (row+1)*self.height/dimensionality - 10, 
                                                               text="0")

        self.canvas.pack(fill=BOTH, expand=1)


def main():  
    root = Tk()
    directPi = PebbleGame(root)
    root.geometry("400x400+200+100")
    root.mainloop()  


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print "exiting.."
        exitapp = True
        raise
