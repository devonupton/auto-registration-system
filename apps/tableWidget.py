# creates a table based on your needs.

from tkinter import *
import tkinter.messagebox as tm

class tableWidget( Frame ):
    # When calling the widget enter the number of rows NOT including the header row
    def __init__( self, numRows = 4, numCols = 4 ):
        self.rows = numRows + 1
        self.cols = numCols
        self.root = Tk()
        self.root.configure( background="black" )
        
        self.table = []
        
        for row in range( self.rows ):
            for col in range( self.cols ):
                # add somthing to change the colour of the header?
                thisLabel = Label( self.root, text="" )
                thisLabel.grid( row=row, column=col, padx=1, pady=1, sticky=EW )
                self.table.append( thisLabel )
        
    def changeColHeader( self, col, Header ):
        self.table[ col ].configure( text=Header )
        
    def changeHeaderRow( self, entryList ):
        return
    
    # Ensures that the row and column are in the tableSpace (not header space)
    # Assume entry is row+0 and col+0
    # if None input, does not check
    def validEntryRange( self, row, col ):
        row = row + 1
        if row != None:
            if ( row < 0 ) or ( row > self.rows ):
                return False
        if col != None:
            if ( col < 0 ) or ( col > self.cols )
                return False
        return True
            
    #
    def changeEntry( self, row, col, Text ):
        if not validEntryRange( row, col ):
            errorMsg = "Row or col index out of range ( " + str(row) + ", " + str(col) + " )\nErr 0xTW-02"
            tm.showerror( "tableWidget Error", errorMsg )
        row = row + 1
        self.table[ (row * self.cols) + col ].configure( text=Text )
       
    #
    def changeRow( self, row, entryList ):
        if len( entryList ) > self.cols:
            errorMsg = "Input is incorrect size for row.\nErr 0xTW-03"
            tm.showerror( "tableWidget Input Error", errorMsg )
            
        for x in range( len( entryList ) ):
            self.changeEntry( row, x, entryList[x] )
            
    def showTable( self ):
        mainloop()
        
test = tableWidget( 5, 10 )
test.changeRow( 1, [] )
test.changeRow( 0, [] )
#test.changeRow( -1, [] )
test.changeRow( 6, [])
test.showTable()