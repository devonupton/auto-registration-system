''' Driver Licence Registration Application '''

from tkinter import *
import cx_Oracle
from datetime import datetime
import tkinter.messagebox as tm
import apps.tableWidget as tW
from apps.new_persons_application import NewPerson
try:
    #Module for opening the image
    from PIL import Image
    PIL_loaded = True
except:
    PIL_loaded = False

#The application object
class App3( Toplevel ):
    def __init__( self, userCx ):
        Toplevel.__init__( self )
        self.title( "Driver Licence Registration Application" )
        self.userCx = userCx
        self.resizable( width=FALSE, height=FALSE )

        #Create and add widgets for licence info
        msg1 = Message( self, text="License Information" , padx=5, pady=5, width=200 )
        msg1.grid( row=0, sticky=N, columnspan=2 )

        licence_no_label= Label( self, text="Licence #" )
        self.licence_no_entry = Entry( self )
        licence_no_label.grid( row=1, sticky=E )
        self.licence_no_entry.grid( row=1, column=1 )

        class_label = Label( self, text="Class" )
        self.class_entry = Entry( self )
        class_label.grid( row=2, sticky=E )
        self.class_entry.grid( row=2, column=1 )

        issuing_date_label = Label( self, text="Issuing Date" )
        self.issuing_date_entry = Entry( self )
        issuing_date_label.grid( row=3, sticky=E )
        self.issuing_date_entry.grid( row=3, column=1 )
        self.issuing_date_entry.insert( 0, datetime.now().strftime( "%d-%b-%Y" ) )

        expiring_date_label = Label( self, text="Expiring Date" )
        self.expiring_date_entry = Entry( self )
        expiring_date_label.grid( row=4, sticky=E )
        self.expiring_date_entry.grid( row=4, column=1 )

        #Create and add widgets for restriction info
        condition_id_label = Label( self, text="Condition IDs" )
        self.condition_id_list_entry = Entry( self )
        condition_id_label.grid( row=5, sticky=E )
        self.condition_id_list_entry.grid( row=5, column=1 )

        condition_label2 = Label( self, text="(comma separated list of c_id's)" )
        condition_label2.grid( row=6, columnspan=2, sticky=E )

        #Create and add widgets for personal info
        msg2 = Message( self, text="Personal Information" , padx=5, pady=5, width=200 )
        msg2.grid( row=0, column=2, sticky=N, columnspan=2 )

        sin_label = Label( self, text="SIN" )
        self.sin_entry = Entry( self )
        sin_label.grid( row=1, column=2, sticky=E )
        self.sin_entry.grid( row=1, column=3 )

        photo_label = Label( self, text="Photo File" )
        self.photo_entry = Entry( self )
        photo_label.grid( row=2, column=2, sticky=E )
        self.photo_entry.grid( row=2, column=3 )

        #Buttons
        condition_id_help_button = Button( self, text="?", command=lambda: self.findConditionIDs(), padx=0, pady=0 )
        condition_id_help_button.grid( row=5, column=2, sticky=W )

        new_condition_button = Button( self, text="Add new Condition", \
                                    command=lambda: NewCondition( self, self.autofill_c_id ) )
        new_condition_button.grid( row=3, column=2, rowspan=4, columnspan=2 )


        new_person_button = Button( self, text="Add new Person", \
                                    command=lambda: NewPerson( self, self.autofill_SIN ) )
        new_person_button.grid( row=3, column=2, rowspan=2, columnspan=2, sticky=N+W )


        open_image_button = Button( self, text="Open Image", \
                                    command=lambda: self.openimage() )
        open_image_button.grid( row=3, column=3, rowspan=2, sticky=E+N )

        submit_button = Button( self, text="Submit", command=lambda: self.submit_form() )
        submit_button.grid( row=6, column=2, columnspan=2 )

    #Used to fill the C_id upon returning from NewCondition app
    def autofill_c_id( self, value ):
        if self.condition_id_list_entry.get() == "":
            self.condition_id_list_entry.insert( 0, value )
        else:
            self.condition_id_list_entry.insert( END, ", " + value )

    #Used to fill the sin # upon returning from NewPerson app
    def autofill_SIN( self, value ):
        self.sin_entry.delete( 0, END )
        self.sin_entry.insert( 0, value )

    #Attempt to open the image upon pressing "Open Image"
    def openimage( self ):
        if PIL_loaded:
            try:
                Image.open( self.photo_entry.get() ).show()
            except:
                tm.showerror( "Open Image Error", "Image could not be opened\nErr 0xa3-2" )
        else:
            tm.showerror( "Open Image Error", "Module unavailable to open images\nErr 0xa3-3" )

    #Returns a super table of Condition IDs for the user
    def findConditionIDs( self ):
        askMsg = "Do you wish to bring up a table of the possible Driving Conditions and their Condition IDs?"
        if not tm.askyesno( "Condition ID Help", askMsg ):
            return
        
        cursor = self.userCx.cursor()
        
        statement = "SELECT UNIQUE * FROM driving_condition"
        cursor.execute( statement )
        
        rows = cursor.fetchall()
        if len( rows ) == 0:
            tm.showerror( "No Driving Conditions!", "There are no Driving Conditions in the database.\nErr 0xa3-4" )
            
        tW.buildSuperTable( cursor.description, rows, "Driving Conditions" )
        
        cursor.close()

    #Attempt to submit data to the database
    def submit_form( self ):

        #Get each input value
        self.entries = { "licence_no":      self.licence_no_entry.get().strip(),
                         "class":           self.class_entry.get().strip().strip(),
                         "issuing_date":    self.issuing_date_entry.get().strip(),
                         "expiring_date":   self.expiring_date_entry.get().strip(),
                         "sin":             self.sin_entry.get().strip(),
                         "photo":           self.photo_entry.get().strip() }

        #Get the Condition IDs
        self.condition_id_list = self.condition_id_list_entry.get().split( "," )

        #Check if input is valid
        if not self.validate_input():
            return

        if not tm.askyesno( "Submit Confirmation", "Are you sure you want to submit?" ):
            return

        cursor = self.userCx.cursor()
        error_type = "Submit Failure"

        #Create savepoint here and specify size of photo
        cursor.execute( "SAVEPOINT App3Save" )
        cursor.setinputsizes( photo=cx_Oracle.BLOB )

        #Try to insert Licence
        statement = "INSERT INTO drive_licence \
                     VALUES( :licence_no, :sin, :class, :photo, :issuing_date, :expiring_date )"
        try:
            cursor.execute( statement, self.entries )
        except cx_Oracle.DatabaseError as exc:
            cursor.execute( "ROLLBACK to App3Save" ) 
            error, = exc.args
            if error.code == 1: #Licence_no must exist or person already has a licence

                #Test if licence already exists
                statement = "SELECT licence_no FROM drive_licence WHERE licence_no = :a"
                try:
                    cursor.execute( statement, a=self.entries["licence_no"].ljust(15) )
                except: #Unknown error
                    tm.showerror( error_type, "Unexpected Error\nErr 0xa3-14" )
                    cursor.close()
                    return

                if len( cursor.fetchall() ) == 0: #Licence isn't taken, must be sin that is taken
                    tm.showerror( error_type, "SIN '" + \
                        self.entries["sin"] + "' already has a licence\nErr 0xa3-15" )
                else: #Licence was found, therefore it's already taken
                    tm.showerror( error_type, "Licence # '" + \
                        self.entries["licence_no"] + "' is already in the database\nErr 0xa3-16" )

            elif error.code == 2291: #sin does not exist
                tm.showerror( error_type, "SIN '" + \
                    str( self.entries["sin"] ) + "' does not exist\nErr 0xa3-17" )
            else: #Unknown error
                tm.showerror( error_type, error.message + "\nErr 0xa3-18" )
            cursor.close()
            return

        #Try to insert Licence Restrictions
        statement = "INSERT INTO restriction VALUES( :a, :b )"
        for condition_id in self.condition_id_list:
            try:
                cursor.execute( statement, a=self.entries["licence_no"], b=condition_id )
            except cx_Oracle.DatabaseError as exc:
                cursor.execute( "ROLLBACK to App3Save" ) 
                cursor.close()
                error, = exc.args
                if error.code == 1: #Duplicate exists
                    tm.showerror( error_type, "Condition ID '" + str(condition_id) + "' entered more than once\nErr 0x3-19" )
                elif error.code == 2291: #Licence already exists -> Condition ID doesn't exist
                    tm.showerror( error_type, "Condition ID '" + \
                        str( condition_id ) + "' does not exist\nErr 0xa3-20" )
                else: #Unknown error
                    tm.showerror( error_type, error.message + "\nErr 0xa3-21" )
                return
            
        #SQL statements executed successfully
        self.userCx.commit()

        #Success message
        successInfo = "License # '" + self.entries["licence_no"] + \
                      "' has been added to the database\nSIN: " +  self.entries["sin"] + \
                      "\nCondition IDs: " + ", ".join( str(i) for i in self.condition_id_list )

        tm.showinfo( "Success!", successInfo )  
        self.destroy()
            
    #Type checking
    def validate_input( self ):
        error_type = "Input Error"

        #licence_no validation
        if self.entries["licence_no"] == '' or len( self.entries["licence_no"] ) > 15:
            msg = "Invalid Licence #: Must not be blank and no longer than 15 characters\nErr 0xa3-5" 
            tm.showerror( error_type, msg )
            return

        #class validation
        if self.entries["class"] == '' or len( self.entries["class"] ) > 10:
            msg = "Invalid Class: Must not be blank and no longer than 10 characters\nErr 0xa3-6" 
            tm.showerror( error_type, msg )
            return
            
        #issuing_date validation
        try:
            date1 = datetime.strptime( self.entries["issuing_date"], "%d-%b-%Y" )
        except:
            msg = "Invalid Issuing Date: Format must be DD-MMM-YYYY\nEx: 04-OCT-2015\nErr 0xa3-7"
            tm.showerror( error_type, msg )
            return

        #Make sure issuing date isn't in the future
        if date1 > datetime.now():
            msg = "Invalid Issuing Date: Issuing Date cannot be in the future\nErr 0xa3-8"
            tm.showerror( error_type, msg )
            return
        elif date1.date() < datetime.now().date():
            if not tm.askyesno( "Input Confirmation", "The Issuing Date is listed as before today. Is that correct?" ):
                return

        #expiring_date validation
        try:
            date2 = datetime.strptime( self.entries["expiring_date"], "%d-%b-%Y" )
        except:
            msg = "Invalid Expiring Date: Format must be DD-MMM-YYYY\nEx: 04-OCT-2015\nErr 0xa3-9"
            tm.showerror( error_type, msg )
            return

        #Make sure issuing date and expiring date make sense together
        if date1 >= date2:
            msg = "Invalid Expiring Date: Must be later than Issuing Date\nErr 0xa3-10"
            tm.showerror( error_type, msg )
            return

        #sin validation
        if self.entries["sin"] == '' or len( self.entries["sin"] ) > 15:
            msg = "Invalid SIN: Must not be blank and no longer than 15 characters\nErr 0xa3-11" 
            tm.showerror( error_type, msg )
            return

        #photo validation
        try:
            self.entries["photo"] = open( self.entries["photo"], 'rb' ).read()
        except:
            msg = "Invalid Photo File: File not found\nExample filepath: Pictures/MyPicture.jpg\nErr 0xa3-12"
            tm.showerror( error_type, msg )
            return

        if self.condition_id_list[0].strip() == '' and len(self.condition_id_list) == 1:
            self.condition_id_list = []
        #condition_id validation and conversion to integers
        for element in range(len(self.condition_id_list)):
            try:
                self.condition_id_list[element] = int( self.condition_id_list[element] )
                if not ( -2147483648 <= self.condition_id_list[element] < 2147483648 ):
                    raise
            except:
                msg = "Invalid Condition ID '" + self.condition_id_list[element] + \
                      "': Must be an integer between -(2^31)-1 and (2^31)-1\nErr 0xa3-13"
                tm.showerror( error_type, msg )
                return
                        
        #No errors encountered
        return True

################################################################################

#A sub-application used to adding a new Driving Condition
#return_entry: A function from parent window that will be automatically
#              called with "c_id" once this application finishes
class NewCondition( Toplevel ):
    def __init__( self, parent, return_entry=None ):
        Toplevel.__init__( self, parent )
        self.title( "New Driving Condition Application" )
        self.resizable( width=FALSE, height=FALSE )

        self.parent = parent
        self.userCx = parent.userCx
        self.return_entry = return_entry #Used to return the c_id back to the previous window

        #Create and add widgets for Description and C_ID
        descr_label = Message( self, text="Enter the Driving Condition Description below", padx=5, pady=5, width=250 )
        self.descBox = Text( self, relief=SUNKEN, width=70, height=15 )
        descr_label.grid( columnspan=4 )
        self.descBox.grid( row=1, columnspan=4 )

        c_id_label = Label( self, text="Condition ID" )
        self.c_id_entry = Entry( self )
        c_id_label.grid( row=2, sticky=E )
        self.c_id_entry.grid( row=2, column=1, sticky=W )

        #Make some space between the entry box and the submit button
        columnexpander = Label( self, text="          " )
        columnexpander.grid( row=2, column=2 )

        #Submit Button
        submit_button = Button( self, text="Submit", command=lambda: self.submit_form() )
        submit_button.grid( row=2, column=3 )

    def submit_form( self ):
        self.descr = self.descBox.get( 1.0, END).strip()
        self.c_id = self.c_id_entry.get().strip()

        #Check that all entries are valid
        if not self.validate_input():
            return

        if not tm.askyesno( "Submit Confirmation", "Are you sure you want to submit?" ):
            return
        
        #Send information to Oracle Database
        statement = "INSERT INTO driving_condition VALUES( :a, :b )"
        cursor = self.userCx.cursor()
        try:
            cursor.execute( statement, a=self.c_id, b=self.descr )

        except cx_Oracle.DatabaseError as exc:
            error, = exc.args
            if error.code == 1:
                tm.showerror( "Submit Failure", "Condition ID '" + str(self.c_id) + "' is already taken\nErr 0xa3-24" )
            else:
                tm.showerror( "Submit Failure", error.message + "\nErr 0xa3-25" )
            return
        finally:
            cursor.close()

        self.userCx.commit()

        #Success message
        successInfo = "Condition ID '" + str(self.c_id) + "' has been added to the database"
        tm.showinfo( "Success!", successInfo )  
                
        #Return sin back to previous window
        if self.return_entry:
            return_entry = self.return_entry
            return_entry( self.c_id_entry.get() )

        self.destroy()

    #Type checking
    def validate_input( self ):
        error_type = "Input Error"

        if self.descr == '' or len( self.descr ) > 1024:
            msg = "Invalid Description: Must not be blank or longer than 1024 characters\nErr 0xa3-22"
            tm.showerror( error_type, msg )
            return
        try:
            self.c_id = int( self.c_id )
            if not ( -2147483648 <= self.c_id < 2147483648 ):
                raise
        except:
            msg = "Invalid Condition ID: Must be an integer between -(2^31)-1 and (2^31)-1\nErr 0xa3-23"
            tm.showerror( error_type, msg )
            return

        #No errors encountered
        return True

#This function starts App3 if user is logged in
def run( userCx ):
    #Prevents use of app if user hasn't logged in.
    if userCx == None:
        tm.showerror( "Error", "You need to login before using this app.\nErr 0xa3-1" )
        return
    App3( userCx )
    return
