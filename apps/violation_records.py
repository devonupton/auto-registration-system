''' Violation Records Application '''
#Violation Record: 
    # This component is used by a police officer to issue a traffic ticket and record 
    # the violation. You may assume that all the information about ticket_type has been 
    # loaded in the initial database.
    
from tkinter import *
from datetime import datetime
import tkinter.messagebox as tm
import cx_Oracle
import apps.tableWidget as tW
import apps.new_persons_application as newPA
    
class app4( Toplevel ):
    def __init__( self, userCx ):
        Toplevel.__init__( self ) 

        self.title( "Violation Records Application" )
        self.resizable( width=FALSE, height=FALSE )
 
        self.userCx = userCx
        
        # building the app window =======================================================
        # [col0 col1 - ticket info] [col2 - extra] [col3, col4 - violator info] [col5 - extra]
        # Information headers
        ticketHeader = Message( self, text="Ticket Information", padx=5, pady=5, width=200 )
        ticketHeader.grid( column=0, row=0, columnspan=2 )
        violatorHeader = Message( self, text="Violator Information", padx=5, pady=5, width=200 )
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
        
        # v_date label/entry
        vDate_label = Label( self, text="Date Issued:" )
        vDate_label.grid( column=0, row=4, sticky=E )
        self.vDate_entry = Entry( self )
        self.vDate_entry.grid( column=1, row=4 )
        self.vDate_entry.insert( 0, "DD-MMM-YYYY HH:MM:SS" )
        
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
        
        # vehicle_id label/entry
        vin_label = Label( self, text="VIN:" )
        vin_label.grid( column=3, row=2, sticky=E )
        self.vin_entry = Entry( self )
        self.vin_entry.grid( column=4, row=2 )
        
        # submit violation button
        submit_button = Button( self, text="Submit Record", command=lambda: self.submitViolation() )
        submit_button.grid( column=4, row=6, sticky=EW )

        # Help buttons
        vTypeHelp_button = Button( self, text="?", command=lambda: findViolationTypes( self.userCx ), padx=0, pady=0 )
        vTypeHelp_button.grid( column=2, row=3 )

        getDate_button = Button( self, text="?", command=lambda: self.setSystime(), padx=0, pady=0 )
        getDate_button.grid( column=2, row=4 )
        
    # Allows user to set the violation date to the system time when requested
    def setSystime( self ):
        askMsg = "Would you like to fill vDate with the current system time?"
        if not tm.askyesno( "Autofill vDate?", askMsg ):
            return
    
        self.vDate_entry.delete( 0, END )
        self.vDate_entry.insert( 0, datetime.now().strftime( "%d-%b-%Y %H:%M:%S" ) )
    
    # Opens an editable Text window for the ticket description
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
            self.descButton.configure( text="<< Close Description" )
            self.descOpen = True
         
            self.descBox = Text( self, relief=SUNKEN, width=70, height=20 )
            self.descBox.grid( column=0, row=7, columnspan=5, sticky=NSEW )
            
        return
  
    # Asks the user if they would like to add a new person to the database, if yes opens the app for it
    def handleNewPerson( self ):
        askMsg = "Would you like to register a person that is not in the system for use here?"
        if not tm.askyesno( "Add New Person?", askMsg ):
            return
        
        newPA.NewPerson( self, self.autofill )
       
    # Major function for submitting a violation
    def submitViolation( self ):
        # Checks that user wants to submit with or without a description.
        askMsg = "Are you sure you want to submit the violation with no description?"
        if not self.descOpen:
            if not tm.askokcancel( "No Description?", askMsg ):
                self.addTextWidget()
                return
            else:
                getDesc = None
        elif len( self.descBox.get( 1.0, END ).strip() ) == 0:
            if not tm.askokcancel( "No Description?", askMsg ):
                return
            else:
                getDesc = None
        else:
            getDesc = self.descBox.get( 1.0, END ).strip()
    
        # create the entry dictionary for the statement
        self.entries = { "ticketNo":    self.ticketNo_entry.get().strip(),
                         "violatorNo":  self.violator_entry.get().strip(),
                         "vehicle_id":  self.vin_entry.get().strip(),
                         "officerNo":   self.officerNo_entry.get().strip(),
                         "vtype":       self.vType_entry.get().strip(),
                         "vdate":       self.vDate_entry.get().strip(),
                         "place":       self.loc_entry.get().strip(),
                         "descr":       getDesc                             }
    
        if not self.validateEntries():
            return
    
        askMsg = "Please check all your entries and make sure they are correct before continuing."
        if not tm.askokcancel( "Are You Sure?", askMsg ):
            return
                
        cursor = self.userCx.cursor()
       
        statement = "INSERT INTO ticket VALUES ( :ticketNo, :violatorNo, :vehicle_id, :officerNo, :vtype, TO_DATE( :vdate, 'dd-Mon-yyyy hh24:mi:ss' ), :place, :descr )"
    
        cursor.execute( "SAVEPOINT Violation" )
        
        try:
            cursor.execute( statement, self.entries )
            cursor.execute( "COMMIT" )
        except cx_Oracle.DatabaseError as exc:
            cursor.execute( "ROLLBACK to Violation" ) 
            cursor.close()
            error, = exc.args
            self.recoverError( error )
            return
            
        infoMsg = "Ticket Number " + str( self.entries["ticketNo"] ) + " has been recorded."
        tm.showinfo( "Success!", infoMsg )
        cursor.close()
     
    # If an error is encountered, we check the error and print a message
    # basically checks the error code, and searches each table to check
    # where a integrity/foreign key constraint comes from.
    def recoverError( self, error ):
        # Ticket No already in Database
        if error.code == 1:
                errMsg = "There is already the ticketNo " + str( self.entries["ticketNo"] ) + " in the database."
                tm.showerror( "TicketNo Already Used", errMsg )
                return
        
        # If the error is not from a foreign key constraint, it is unknown
        if error.code != 2291:
            errMsg = error.message + "\nErr 0xa4-16"
            tm.showerror( "Unexpected Error", errMsg )
            return
                
        cursor = self.userCx.cursor()
            
        # Check vtype for integrity constraint
        statement = "SELECT * FROM ticket_type WHERE vtype = '" + self.entries["vtype"] + "'"
        try:
            cursor.execute( statement )
        except:
            cursor.close()
            tm.showerror( "Error", "Something unexpected happened!\nErr 0xa4-17")
            return
            
        rows = cursor.fetchall()
        if len( rows ) == 0:
            cursor.close()
            errMsg = "'" + self.entries["vtype"] + "' is not a valid vType. Use the '?' button to the right of the vType entry to check possible vTypes.\nErr 0xa4-23"
            tm.showerror( "Invalid vType", errMsg )
            return
            
        # Check violator_no for integrity constraint
        statement = "SELECT * FROM people WHERE sin = '" + self.entries["violatorNo"] + "'"
        try:
            cursor.execute( statement )
        except:
            cursor.close()
            tm.showerror( "Error", "Something unexpected happened!\nErr 0xa4-18")
            return
            
        rows = cursor.fetchall()
        if len( rows ) == 0:
            cursor.close()
            errMsg = "The violator '" + self.entries["violatorNo"] + "' is not in the database. Please double check the violatorNo and try again.\nErr 0xa4-19"
            tm.showerror( "Invalid violatorNo", errMsg )
            return
            
        # Check office_no for integrity constraint
        statement = "SELECT * FROM people WHERE sin = '" + self.entries["officerNo"] + "'"
        try:
            cursor.execute( statement )
        except:
            cursor.close()
            tm.showerror( "Error", "Something unexpected happened!\nErr 0xa4-19")
            return
            
        rows = cursor.fetchall()
        if len( rows ) == 0:
            cursor.close()
            errMsg = "The officer '" + self.entries["officerNo"] + "' is not in the database. Please double check the officerNo and try again.\nErr 0xa4-20"
            tm.showerror( "Invalid officerNo", errMsg )
            return
        
        # Check vehicle_id for integrity constraint
        statement = "SELECT * FROM vehicle WHERE serial_no = '" + self.entries["vehicle_id"] + "'"
        try:
            cursor.execute( statement )
        except:
            cursor.close()
            tm.showerror( "Error", "Something unexpected happened!\nErr 0xa4-21")
            return
            
        rows = cursor.fetchall()
        if len( rows ) == 0:
            cursor.close()
            errMsg = "The VIN '" + self.entries["vehicle_id"] + "' is not in the database. Please double check the VIN and try again.\nErr 0xa4-22"
            tm.showerror( "Invalid VIN", errMsg )
            return
            
        cursor.close()
        tm.showerror( "UNEXPECTED ERROR", error.message )
        
    # Gets the primary owner on a VIN.
    def getPrimaryOwner( self ):
        cursor = self.userCx.cursor()
        
        askMsg = "Would you like to write this violation to the Primary Owner of '" + self.entries["vehicle_id"] + "'"
        if not tm.askyesno( "Blank Violator Entry", askMsg ):
            return False
        
        # Check vehicle_id for integrity constraint
        statement = "SELECT * FROM vehicle WHERE serial_no = '" + self.entries["vehicle_id"] + "'"
        try:
            cursor.execute( statement )
        except:
            cursor.close()
            tm.showerror( "Error", "Something unexpected happened!\nErr 0xa4-24")
            return False
            
        rows = cursor.fetchall()
        if len( rows ) == 0:
            cursor.close()
            errMsg = "The VIN '" + self.entries["vehicle_id"] + "' is not in the database. Please double check the VIN and try again.\nErr 0xa4-25"
            tm.showerror( "Invalid VIN", errMsg )
            return False
            
        # Grab the primary owner
        statement = "SELECT owner_id FROM owner O " +\
                    "WHERE is_primary_owner = 'y' AND " +\
                    "vehicle_id = '" + self.entries["vehicle_id"] + "'"
                    
        try:
            cursor.execute( statement )
        except:
            cursor.close()
            tm.showerror( "Error", "Something unexpected happened!\nErr 0xa4-26")
            return False
            
        # If there is no primary owner, we have an odd issue...
        rows = cursor.fetchall()
        if len( rows ) == 0:
            cursor.close()
            errMsg = "The VIN '" + self.entries["vehicle_id"] + "' has no primary owner!\nErr 0xa4-27"
            tm.showerror( "No primary owner!", errMsg )
            return False
            
        primaryOwner = rows[0][0]
        
        askMsg = "The primary owner was found to be: '" + primaryOwner.strip() + "' continue?"
        if not tm.askyesno( "Continue?", askMsg ):
            return False
            
        self.violator_entry.insert( 0, primaryOwner.strip() )
        self.entries["violatorNo"] = primaryOwner.strip()
        
        return True
        
        cursor.close()
        
    # Ensures that the entries are valid for submitting to oracle/database
    def validateEntries( self ):
        # ticketNo validation
        if self.entries["ticketNo"] == '':
            errMsg = "The ticket number cannot be blank.\nErr 0xa4-02"
            tm.showerror( "Ticket Number Error", errMsg )
            return False
        try:
            self.entries["ticketNo"] = int( self.entries["ticketNo"] )
            if not ( -2147483648 <= self.entries["ticketNo"] < 2147483648 ):
                raise
        except:
            tm.showerror( "Ticket Number Error", "Invalid ticketNo: Must be an integer between -(2^31)-1 and (2^31)-1\nErr 0xa4-03" )
            return False

        # officerNo validation
        if self.entries["officerNo"] == '' or len( self.entries["officerNo"] ) > 15:
            errMsg = "Officer No must not be blank and no longer than 15 characters.\nErr 0xa4-04"
            tm.showerror( "Officer No Error", errMsg )
            return False
            
        # vType validation
        if self.entries["vtype"] == '' or len( self.entries["vtype"] ) > 10:
            errMsg = "vType must not be blank and no longer than 10 characters.\nErr 0xa4-05"
            tm.showerror( "vType Error", errMsg )
            return False
            
        # vDate validation (allow for two date types)
        temp = self.entries["vdate"].split()
        askMsg = "Your vDate does not include hours and minutes, do you wish to continue?"
        if len( temp ) == 1:
            if not tm.askokcancel( "No HH:MM Specified", askMsg ):
                return False
            
        if len( temp ) == 1:
            try:
                # Strip only DD-MMM-YYYY
                ticketTime = datetime.strptime( self.entries["vdate"], "%d-%b-%Y" )
                self.entries["vdate"] += " 00:00:00"
            except:
                errMsg = "Date must be of the format DD-MMM-YYYY at least.\nEx: 14-OCT-2016\nErr 0xa4-06"
                tm.showerror( "Invalid Date entry", errMsg )
                return False
        elif len( temp ) == 2:
            try:
                # Strip DD-MMM-YYYY and HH:MM:SS
                ticketTime = datetime.strptime( self.entries["vdate"], "%d-%b-%Y %H:%M:%S" )
            except:
                errMsg = "Date must be of the format DD-MMM-YYYY HH:MM:SS\nEx: 14-OCT-2016 14:25:00\nErr 0xa4-07"
                tm.showerror( "Invalid Date entry", errMsg )
                return False
        else:
            errMsg = "Date must be of the format DD-MMM-YYYY HH:MM:SS\nEx: 14-OCT-2016 14:25:00\nErr 0xa4-08"
            tm.showerror( "Invalid Date entry", errMsg )
            return False 
            
        # vDate should not be in the future
        if ticketTime > datetime.now():
            errMsg = "Tickets cannot be issued in advance. Please ensure the correct time.\nErr 0xa4-09"
            tm.showerror( "Ticket Date in Future", errMsg )
            return False
            
        # Place validation
        if self.entries["place"] == '':
            askMsg = "Are you sure you want the location to be NULL?"
            if not tm.askyesno( "No location?", askMsg ):
                return False
        elif len( self.entries["place"] ) > 20:
            errMsg = "The location entry must be less than 20 characters.\nErr 0xa4-10"
            tm.showerror( "Location Length Error", errMsg )
            return False
            
        # Description Validation
        if self.entries["descr"] != None:
            if len( self.entries["descr"] ) > 1024:
                errMsg = "The description cannot be longer than 1024 characters.\nErr 0xa4-11"
                tm.showerror( "Description Too Long", errMsg )
                return False 
                
        # vehicle_id validation
        # THIS MUST BE DONE BEFORE GETTING THE PRIMARY OWNER IF NEEDED
        if self.entries["vehicle_id"] == '' or len( self.entries["vehicle_id"] ) > 15:
            errMsg = "VIN must not be blank and no longer than 15 characters.\nErr 0xa4-13"
            tm.showerror( "VIN Error", errMsg )
            return False
            
        # violator_no validation
        if self.entries["violatorNo"] == '':
            if not self.getPrimaryOwner():
                return False
        if self.entries["violatorNo"] == '' or len( self.entries["violatorNo"] ) > 15:
            errMsg = "Violator No must not be blank and no longer than 15 characters.\nErr 0xa4-12"
            tm.showerror( "Violator SIN Error", errMsg )
            return False

        # Officer should not be Violator
        if self.entries["officerNo"] == self.entries["violatorNo"]:
            errMsg = "The issuer of the ticket cannot be the violator.\nErr 0xa4-14"
            tm.showerror( "Officer/Violator Conflict", errMsg )
            return False
            
        return True
        

        
# Returns a super table to violation types for the user
def findViolationTypes( userCx ):
    askMsg = "Do you wish to bring up a table of the possible violation types and their fines?"
    if not tm.askyesno( "vType Help", askMsg ):
        return
    
    cursor = userCx.cursor()
    
    statement = "SELECT UNIQUE * FROM ticket_type"
    cursor.execute( statement )
    
    rows = cursor.fetchall()
    if len( rows ) == 0:
        tm.showerror( "No Violation Types!", "There are no violation types in the database.\nErr 0xa4-01" )
        
    tW.buildSuperTable( cursor.description, rows, "Violation Types" )
    
    cursor.close()
    
# starts the toplevel for APP4
# makes sure the user is logged in before the app can open
def run( userCx ):
    if userCx == None:
        tm.showerror( "Error", "You need to login before using this app.\nErr 0xa4-99" )
        return

    app4( userCx )
