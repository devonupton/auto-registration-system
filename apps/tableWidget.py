# creates a table based on your needs.

from tkinter import *
import tkinter.messagebox as tm
import cx_Oracle

class tableWidget( Frame ):
    # When calling the widget enter the number of rows NOT including the header row
    def __init__( self, numRows = 4, numCols = 4, t="Search Result" ):
        self.rows = numRows + 1
        self.cols = numCols
        self.root = Tk()
        self.root.title( t )
        self.root.configure( background="black" )
        
        self.table = []
        
        for row in range( self.rows ):
            for col in range( self.cols ):
                if row == 0:
                    thisLabel = Label( self.root, text="", bg="grey")
                else:
                    thisLabel = Label( self.root, text="" )
                thisLabel.grid( row=row, column=col, padx=1, pady=1, sticky=NSEW )
                self.table.append( thisLabel )
       
    # Ensures data is not too long for the table
    def validColLength( self, entryList=[] ):
        if len( entryList ) > self.cols:
            errorMsg = "Input is too large for row.\nErr 0xTW-03"
            tm.showerror( "tableWidget Input Error", errorMsg )
            return False
        return True
       
    # Changes the specified column header to the specified text
    def changeHeaderCol( self, col=0, Header="" ):
        self.table[ col ].configure( text=Header )
        
    # Changes the header row to the given entry list.
    def changeHeaderRow( self, entryList=[] ):
        if not self.validColLength( entryList ):
            return
            
        for x in range( len( entryList ) ):
            self.changeHeaderCol( x, entryList[x] )
    
    # Ensures that the row and column are in the tableSpace (not headerSpace)
    # Assume entry is row+0 and col+0
    # if None input, does not check
    def validEntryRange( self, row=0, col=0 ):
        row = row + 1
        if row != None:
            if ( row <= 0 ) or ( row > self.rows ):
                return False
        if col != None:
            if ( col < 0 ) or ( col > self.cols ):
                return False
        return True
            
    # changes a entry a (row, col) in the entrySpace (not headerSpace)
    def changeEntry( self, row=0, col=0, Text="" ):            
        if not self.validEntryRange( row, col ):
            errorMsg = "Row or col index out of range ( " + str(row) + ", " + str(col) + " )\nErr 0xTW-02"
            tm.showerror( "tableWidget Error", errorMsg )
            return
        row = row + 1
        self.table[ (row * self.cols) + col ].configure( text=Text )
       
    # Changes a selected row in the tableSpace with the entryList
    def changeRow( self, row=0, entryList=[] ):
        if not self.validColLength( entryList ):
            return
               
        for x in range( len( entryList ) ):
            self.changeEntry( row, x, entryList[x] )
      
    # displays the table after all entries have been added
    def showTable( self ):
        mainloop()

# builds a tableSpace into tkinter (a list of all the things)
def buildCxTable( tableSpace, title ):
    numRow = len( tableSpace ) - 1
    numCol = len( tableSpace[0] )
        
    userTable = tableWidget( numRow, numCol, title )
    
    userTable.changeHeaderRow( tableSpace[0] )
    for y in range( numRow ):
        userTable.changeRow( y, tableSpace[y + 1] )
          
    userTable.showTable()
                