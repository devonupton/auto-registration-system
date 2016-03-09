''' Violation Records Application '''

#Violation Record: 
    # This component is used by a police officer to issue a traffic ticket and record 
    # the violation. You may assume that all the information about ticket_type has been 
    # loaded in the initial database.

#CREATE TABLE ticket (
#  ticket_no     int,
#  violator_no   CHAR(15),  
#  vehicle_id    CHAR(15),
#  office_no     CHAR(15),
#  vtype        char(10),
#  vdate        date,
#  place        varchar(20),
#  descriptions varchar(1024),
#  PRIMARY KEY (ticket_no),
#  FOREIGN KEY (vtype) REFERENCES ticket_type,
#  FOREIGN KEY (violator_no) REFERENCES people ON DELETE CASCADE,
#  FOREIGN KEY (vehicle_id)  REFERENCES vehicle,
#  FOREIGN KEY (office_no) REFERENCES people ON DELETE CASCADE
    
from tkinter import *
import tkinter.messagebox as tm
import cx_Oracle
import apps.tableWidget as tW
    
class app4( Toplevel ):
    def __init__( self, userCx ):
        Toplevel.__init__( self ) # might need to consider parent?
        self.title( "App5: Violation Insertion" )
        
        self.userCx = userCx
        
        # building the app window =======================================================
        # [col0 col1 - ticket info] [col2 - extra] [col3, col4 - violator info] [col5 - extra]
        # Information headers
        ticketHeader = Label( self, text="Ticket Info" )
        ticketHeader.grid( column=0, row=0, columnspan=2 )
        violatorHeader = Label( self, text="Violator Info" )
        violatorHeader.grid( column=3, row=0, columnspan=2 )
        
        # ticketNo label/entry
        ticketNo_label = Label( self, text="Ticket No:" )
        ticketNo_label.grid( column=0, row=1, sticky=E )
        self.ticketNo_entry = Entry( self )
        self.ticketNo_entry.grid( row=1, column=1 )
        
        # officerNo label/entry
        officerNo_label = Label( self, text="Officer No:" )
        officerNo_label.grid( column=0, row=2, sticky=E )
        self.officerNo_entry = Entry( self )
        self.officerNo_entry.grid( column=1, row=2 )
        
        # v_type label/entry, and search button
        vType_label = Label( self, text="vType No:" )
        vType_label.grid( column=0, row=3, sticky=E )
        self.vType_entry = Entry( self )
        self.vType_entry.grid( column=1, row=3 )
        
        vTypeHelp_button = Button( self, text="?", command=lambda: findViolationTypes( self.userCx ), padx=0, pady=0 )
        vTypeHelp_button.grid( column=2, row=3 )
        
        # v_date label/entry
        vDate_label = Label( self, text="Date Issued:" )
        vDate_label.grid( column=0, row=4, sticky=E )
        self.vDate_entry = Entry( self )
        self.vDate_entry.grid( column=1, row=4 )
        
        # location label/entry
        loc_label = Label( self, text="Location:" )
        loc_label.grid( column=0, row=5, sticky=E )
        self.loc_entry = Entry( self )
        self.loc_entry.grid( column=1, row=5 )
        
        # Add Description Button ( extends window to add text? )
        self.descOpen = False
        self.descButton = Button( self, text="Open Description >>>", command=lambda: self.addTextWidget() )
        self.descButton.grid( column=0, row=6, columnspan=2, sticky=EW )
        
        # violator_id label/entry
        violator_label = Label( self, text="Violator SIN:" )
        violator_label.grid( column=3, row=1, sticky=E )
        self.violator_entry = Entry( self )
        self.violator_entry.grid( column=4, row=1 )
        
        # vehicle_id label/entry
        vin_label = Label( self, text="VIN:" )
        vin_label.grid( column=3, row=2, sticky=E )
        self.vin_entry = Entry( self )
        self.vin_entry.grid( column=4, row=2 )
        
        # submit violation button
        
        # add new person button (?)
        
        #mainloop()
    
    def addTextWidget( self ):
        if self.descOpen:
            print( "close extendWindow" )
            self.descButton.configure( text="Open Description >>>" )
            self.descOpen = False
            
            self.descBox.destroy()
            
        else:
            print( "open extendWindow" )
            self.descButton.configure( text="<<< Close Description" )
            self.descOpen = True
            
            self.descBox = Text( self, relief=SUNKEN )
            self.descBox.grid( column=0, row=7, columnspan=6, sticky=EW )
            
        return
        
def findViolationTypes( userCx ):
    askMsg = "Do you wish to bring up a table of the possible violation types and their type_ids?"
    if not tm.askyesno( "vType Help", askMsg ):
        return
    print( "search!" )
    
def run( connection ):
    app4( connection )
    pass