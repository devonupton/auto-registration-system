''' Driver Licence Registration Application '''

from tkinter import *
import tkinter.messagebox as tm
import cx_Oracle
from datetime import datetime
from apps.new_persons_application import NewPerson

class App3( Toplevel ):
    def __init__( self, userCx ):
        Toplevel.__init__( self )
        self.title( "Driver Licence Registration Application" )
        self.userCx = userCx
        self.resizable( width=FALSE, height=FALSE )

        #Create and add widgets for licence info
        msg1 = Message( self, text="License Information" , padx=5, pady=5, width=200 )
        msg1.grid( row=0, sticky=N, columnspan=2 )

        licence_no_label= Label( self, text="Licence_no" )
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

        expiring_date_label = Label( self, text="Expiring Date" )
        self.expiring_date_entry = Entry( self )
        expiring_date_label.grid( row=4, sticky=E )
        self.expiring_date_entry.grid( row=4, column=1 )

        row_expander = Label( self, text="" ) #Create an extra blank row
        row_expander.grid( row=5 )

        #Create and add widgets for personal info
        msg2 = Message( self, text="Personal Information" , padx=5, pady=5, width=200 )
        msg2.grid( row=0, column=2, sticky=N, columnspan=2 )

        sin_label = Label( self, text="Sin" )
        self.sin_entry = Entry( self )
        sin_label.grid( row=1, column=2, sticky=E )
        self.sin_entry.grid( row=1, column=3 )

        photo_label = Label( self, text="Photo File" )
        self.photo_entry = Entry( self )
        photo_label.grid( row=2, column=2, sticky=E )
        self.photo_entry.grid( row=2, column=3 )

        #Buttons
        new_person_button = Button( self, text="Add new Person", \
                                    command=lambda: NewPerson( self, self.autofill ) )
        new_person_button.grid( row=3, column=2, rowspan=2, columnspan=2, sticky=W+N )

        open_image_button = Button( self, text="Open Image", \
                                    command=lambda: self.openimage() )
        open_image_button.grid( row=3, column=3, rowspan=2, sticky=E+N )

        submit_button = Button( self, text="Submit", command=lambda: self.submit_form() )
        submit_button.grid( row=4, column=2, rowspan=2, columnspan=2, sticky=S )

    #Used to fill the sin # upon returning from NewPerson app
    def autofill( self, value ):
        self.sin_entry.delete( 0, END )
        self.sin_entry.insert( 0, value )

    def openimage( self ):
        tm.showerror( "CONSTRUCTION ZONE", "INCOMPLETE" )
        return

    #Attempt to submit data to the database
    def submit_form( self ):

        #Get each input value
        self.entries = { "licence_no":      self.licence_no_entry.get().lower(),
                         "class":           self.class_entry.get().lower(),
                         "issuing_date":    self.issuing_date_entry.get(),
                         "expiring_date":   self.expiring_date_entry.get(),
                         "sin":             self.sin_entry.get().lower(),
                         "photo":           self.photo_entry.get().lower() }

        if not self.validate_input():
            return

        if not tm.askyesno( "Submit Confirmation", "Are you sure you want to submit?" ):
            return

        cursor = self.userCx.cursor()

        #Create query statments

        error_type = "Submit Failure"

        #Create savepoint here
        cursor.execute( "SAVEPOINT App3Save" )


        #SQL statements executed successfully
        cursor.close()
        self.userCx.commit()

        #Success message
        successInfo = "incomplete message"
        tm.showinfo( "Success!", successInfo )  
        self.destroy()
            

    #Type checking
    def validate_input( self ):
        error_type = "Input Error"

        #licence_no validation
        if self.entries["licence_no"] == '' or len( self.entries["licence_no"] ) > 15:
            msg = "Invalid Licence_no: Must not be blank and no longer than 15 characters\nErr 0xa3-2" 
            tm.showerror( error_type, msg )
            return

        #class validation
        if self.entries["class"] == '' or len( self.entries["class"] ) > 10:
            msg = "Invalid Class: Must not be blank and no longer than 10 characters\nErr 0xa3-3" 
            tm.showerror( error_type, msg )
            return
            
        #issuing_date validation
        try:
            date1 = datetime.strptime( self.entries["issuing_date"], "%d-%b-%Y" )
        except:
            msg = "Invalid Issuing Date: Format must be DD-MMM-YYYY\nEx: 04-OCT-2015\nErr 0xa3-4"
            tm.showerror( error_type, msg )
            return

        #expiring_date validation
        try:
            date2 = datetime.strptime( self.entries["expiring_date"], "%d-%b-%Y" )
        except:
            msg = "Invalid Expiring Date: Format must be DD-MMM-YYYY\nEx: 04-OCT-2015\nErr 0xa3-5"
            tm.showerror( error_type, msg )
            return

        #Make sure issuing date and expiring date make sense together
        if date1 > date2:
            msg = "Invalid Expiring Date: Must be later than Issuing Date\nErr 0xa3-6"
            tm.showerror( error_type, msg )
            return

        #sin validation
        if self.entries["sin"] == '' or len( self.entries["sin"] ) > 15:
            msg = "Invalid Sin: Must not be blank and no longer than 15 characters\nErr 0xa3-6" 
            tm.showerror( error_type, msg )
            return

        #photo validation

        #No errors encountered
        return True

def run( userCx ):
    #Prevents use of app if user hasn't logged in.
    if userCx == None:
        tm.showerror( "Error", "You need to login before using this app.\nErr 0xa3-1" )
        return
    App3( userCx )
    return
