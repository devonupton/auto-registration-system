# creates a tkinter table from SQL rows 

from tkinter import *
import tkinter.messagebox as tm
import cx_Oracle

class tableWidget( Frame ):
    # When calling the widget enter the number of rows 
    # NOT including the header row
    def __init__( self, numRows = 4, numCols = 4, t="Search Result" ):
        self.rows = numRows + 1
        self.cols = numCols
        self.root = Tk()
        self.root.title( t )
        self.root.configure( background="dark grey" )
        self.root.resizable( width=FALSE, height=FALSE )
        
        self.table = []
        
        # Pythonic way of creating a list of tkinter widgets
        for row in range( self.rows ):
            for col in range( self.cols ):
                if row == 0:
                    thisLabel = Label( self.root, text="", bg="grey")
                else:
                    thisLabel = Label( self.root, text="" )
                    
                thisLabel.grid( row=row, column=col,\
                                padx=1, pady=1, sticky=NSEW )
                                
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
            errorMsg = "Row or col index out of range ( " + str(row) +\
                       ", " + str(col) + " )\nErr 0xTW-02"
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

#===============================================================================
# Function: buildCxTable
#===============================================================================
# builds a tableSpace into tkinter (a list of all the things)
# You may want to see the buildSuperTable, a more general function
def buildCxTable( tableSpace, title ):
    numRow = len( tableSpace ) - 1
    numCol = len( tableSpace[0] )
        
    userTable = tableWidget( numRow, numCol, title )
    
    userTable.changeHeaderRow( tableSpace[0] )
    for y in range( numRow ):
        userTable.changeRow( y, tableSpace[y + 1] )
          
    userTable.showTable()
         
#===============================================================================
# Function: getHeaderList
#===============================================================================
# expected use: getHeaderList( cursor.description )
# returns the headerList for use with createTableSpace
# You may just want to use the general buildSuperTable function.
def getHeaderList( objectSet ):
    temp = []
    for column in objectSet:
        temp.append( column[0] )
    return temp
    
#===============================================================================
# Function: createTableSpace
#===============================================================================
# creates a tableSpace for use with buildCxTable
# You may want to see buildSuperTable, instead
def createTableSpace( headerList, rows ):
    if len( rows ) == 0:
        return None
    tableSpace = [headerList]
    for x in range( len(rows) ):
        tempRow = []
        for entry in rows[x]:
            if entry == None:
                tempRow.append( "N/A" )
            else:
                tempRow.append( entry )
        tableSpace.append( tempRow )
    return tableSpace
                
#===============================================================================
# Function: buildSuperTable
#===============================================================================
# builds a table before your eyes
# usage: buildSuperTable( cursor.description, cursor.fetchall(), "title" )
def buildSuperTable( desc, rows, title ):
    if len( rows ) == 0:
        return None
    buildCxTable( createTableSpace(  getHeaderList( desc ), rows ), title )