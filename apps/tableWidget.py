# creates a table based on your needs.

from tkinter import *
import tkinter.messagebox as tm

class tableWidget( Frame ):
    def __init__( self, numRows = 4, numCols = 4 ):
        self.rows = numRows + 1
        self.cols = numCols
        self.root = Tk()
        self.root.configure( background="black" )
        
        self.table = []
        
        for row in range( self.rows ):
            for col in range( self.cols ):
                thisLabel = Label( self.root, text="" )
                thisLabel.grid( row=row, column=col, padx=1, pady=1, sticky=EW )
                self.table.append( thisLabel )
        
    def changeColHeader( self, col, Header ):
        self.table[ col ].configure( text=Header )
    
    def changeEntry( self, row, col, Text ):
        row = row + 1
        self.table[ (row * self.cols) + col ].configure( text=Text )
        
    def showTable( self ):
        mainloop()
        
test = tableWidget()
test.changeColHeader( 1, "Random Things" )
test.changeEntry( 1, 1, "double" )
test.showTable()