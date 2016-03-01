# creates a table based on your needs.

from tkinter import *
import tkinter.messagebox as tm

class tableWidget():
    def __init__( self, rows=3, columns=3 ):
        
        self.root = Tk()
        self.rows = rows
        self.columns = columns
        self.table = []
        
        for row in range( rows ):
            for col in range( columns ):
                print( row, col )
                self.table.append( Label( self.root, text="hi" ) )
                
                
        for row in self.table:
            print( row )
                
                
    def addEntry( self, row, col, entry ):
        print( self.table )
        self.table[row][col] = entry
        
    def printTable( self ):
        print( self.table )
        
a = tableWidget( rows = 4, columns = 5)
#a.addEntry( 1, 1, "poop" )
#a.printTable()