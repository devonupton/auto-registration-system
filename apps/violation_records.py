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
import apps.new_persons_application as newPA
    
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
        vType_label = Label( self, text="vType:" )
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
        self.descButton = Button( self, text="Add Description >>", command=lambda: self.addTextWidget() )
        self.descButton.grid( column=1, row=6, sticky=EW )
        
        # violator_id label/entry
        violator_label = Label( self, text="Violator SIN:" )
        violator_label.grid( column=3, row=1, sticky=E )
        self.violator_entry = Entry( self )
        self.violator_entry.grid( column=4, row=1 )
        
        # add new person button (?)
        newPerson_button = Button( self, padx=0, pady=0, text="?", command=lambda: self.handleNewPerson() )
        newPerson_button.grid( column=5, row=1, sticky=EW )
        
        # vehicle_id label/entry
        vin_label = Label( self, text="VIN:" )
        vin_label.grid( column=3, row=2, sticky=E )
        self.vin_entry = Entry( self )
        self.vin_entry.grid( column=4, row=2 )
        
        # submit violation button
        submit_button = Button( self, text="Submit Record", command=lambda: self.submitViolation() )
        submit_button.grid( column=4, row=6, sticky=EW )
        

        #mainloop()
    
    # Opens an editable text window for the ticket description
    def addTextWidget( self ):
        if self.descOpen:
            # Ask user to confirm data loss for closing description
            if len( self.descBox.get( 1.0, END ).strip() ) > 0:
                askMsg = "If you close the description you will lose what has been written. " +\
                         "Are you sure you want to close?"
                if not tm.askyesno( "Data Loss Confirmation", askMsg ):
                    return
            
            self.descButton.configure( text="Add Description >>" )
            self.descOpen = False
            
            self.descBox.destroy()
            
        else:
            #print( "open extendWindow" )
            self.descButton.configure( text="<< Close Description" )
            self.descOpen = True
         
            self.descBox = Text( self, relief=SUNKEN, width=70, height=20 )
            self.descBox.grid( column=0, row=7, columnspan=5, sticky=NSEW )
            
        return
        
    def autofill( self, value ):
        if self.violator_entry.get() == "":
            self.violator_entry.insert( 0, value )
            infoMsg = "The new SIN was inserted into the violator SIN section." 
            tm.showinfo( "SIN saved", infoMsg )
        else:
            self.violator_entry.insert( END, " <<" + value + ">>" )
            errMsg = "There was information in the entry already. The new SIN was placed in the entry with '<<' and '>>' surrounding it\nErr 0xA5-02"
            tm.showerror( "SIN saved", errMsg )
  
    def handleNewPerson( self ):
        askMsg = "Would you like to register a person that is not in the system for use here?"
        if not tm.askyesno( "Add New Person?", askMsg ):
            return
        
        newPA.NewPerson( self, self.autofill )
        
    def submitViolation( self ):
        askMsg = "Please check all your entries and make sure they are correct before continuing."
        if not tm.askokcancel( "Are You Sure?", askMsg ):
            return
        
        askMsg = "Are you sure you want to submit the violation with no description?"
        if not self.descOpen:
            if not tm.askokcancel( "No Description?", askMsg ):
                self.addTextWidget()
                return
        elif len( self.descBox.get( 1.0, END ).strip() ) == 0:
            if not tm.askokcancel( "No Description?", askMsg ):
                return
        
def findViolationTypes( userCx ):
    askMsg = "Do you wish to bring up a table of the possible violation types and their fines?"
    if not tm.askyesno( "vType Help", askMsg ):
        return
    
    cursor = userCx.cursor()
    
    statement = "SELECT UNIQUE * FROM ticket_type"
    cursor.execute( statement )
    
    rows = cursor.fetchall()
    if len( rows ) == 0:
        tm.showerror( "No Violation Types!", "There are no violation types in the database.\nErr 0xA5-01" )
        
    tW.buildSuperTable( cursor.description, rows, "Violation Types" )
    
    cursor.close()
    
def run( connection ):
    app4( connection )
