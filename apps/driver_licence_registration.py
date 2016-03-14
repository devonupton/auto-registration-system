''' Driver Licence Registration Application '''

from tkinter import *
import tkinter.messagebox as tm
import cx_Oracle
from apps.new_persons_application import NewPerson

class App3( Toplevel ):
    def __init__( self, userCx ):
        Toplevel.__init__( self )
        self.title( "Driver Licence Registration Application" )
        self.userCx = userCx
        self.resizable( width=FALSE, height=FALSE )

        #Create and add widgets for licence info
        msg1 = Message( self, text="Licence Information", padx=5, pady=5, width=200 )
        msg1.grid( row=0, sticky=N, columnspan=2 )

        licence_no_label= Label( self, text="Licence_no" )
        self.licence_no_entry = Entry( self )
        licence_no_label.grid( row=1, sticky=E )
        self.licence_no_entry.grid( row=1, column=1 )

        sin_label = Label( self, text="Sin" )
        self.sin_entry = Entry( self )
        sin_label.grid( row=2, sticky=E )
        self.sin_entry.grid( row=2, column=1 )

        class_label = Label( self, text="Class" )
        self.class_entry = Entry( self )
        class_label.grid( row=3, sticky=E )
        self.class_entry.grid( row=3, column=1 )

        photo_label = Label( self, text="Photo Filepath" )
        self.photo_entry = Entry( self )
        photo_label.grid( row=4, sticky=E )
        self.photo_entry.grid( row=4, column=1 )

        issuing_date_label = Label( self, text="Issuing Date" )
        self.issuing_date_entry = Entry( self )
        issuing_date_label.grid( row=5, sticky=E )
        self.issuing_date_entry.grid( row=5, column=1 )

        expiring_date_label = Label( self, text="Expiring Date" )
        self.expiring_date_entry = Entry( self )
        expiring_date_label.grid( row=6, sticky=E )
        self.expiring_date_entry.grid( row=6, column=1 )

        #Buttons
        new_person_button = Button( self, text="Add new Person", \
                                    command=lambda: NewPerson( self, self.autofill ) )
        new_person_button.grid( row=3, column=2, rowspan=3, columnspan=2, )

        submit_button = Button( self, text="Submit", command=lambda: self.submit_form() )
        submit_button.grid( row=5, column=2, rowspan=2, columnspan=2, )

    #Used to fill the sin # upon returning from NewPerson app
    def autofill( self, value ):
        self.sin_entry.delete( 0, END )
        self.sin_entry.insert( 0, value )

    #Attempt to submit data to the database
    def submit_form( self ):

        #Get each input value
        self.entries = { "licence_no":      self.licence_no_entry.get().lower(),
                         "sin":             self.sin_entry.get().lower(),
                         "class":           self.class_entry.get().lower(),
                         "photo":           self.photo_entry.get().lower(),
                         "issuing_date":    self.issuing_date_entry.get(),
                         "expiring_date":   self.expiring_date_entry.get() }

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

        tm.showerror( "CONSTRUCTION ZONE", "INCOMPLETE" )
        return

        #vehicle_id validation
        if self.entries["vehicle_id"] == '' or len( self.entries["vehicle_id"] ) > 15:
            msg = "Invalid Vehicle_id: Must not be blank and no longer than 15 characters\nErr 0xa1-2" 
            tm.showerror( error_type, msg )
            return

        #maker validation
        if self.entries["maker"] == '' or len( self.entries["maker"] ) > 20:
            msg = "Invalid Maker: Must not be blank and no longer than 20 characters\nErr 0xa1-3" 
            tm.showerror( error_type, msg )
            return
            
        #model validation
        if self.entries["model"] == '' or len( self.entries["model"] ) > 20:
            msg = "Invalid Model: Must not be blank and no longer than 20 characters\nErr 0xa1-4" 
            tm.showerror( error_type, msg )
            return

        #year validation
        try:
            self.entries["year"] = int( self.entries["year"] )
            if not ( 0 <= self.entries["year"] < 10000 ):
                raise
        except:
            msg = "Invalid Year: Must be an integer between 0 and 9999\nErr 0xa1-5" 
            tm.showerror( error_type, msg )
            return

        #color validation
        if self.entries["color"] == '' or len( self.entries["color"] ) > 10:
            msg = "Invalid Color: Must not be blank and no longer than 10 characters\nErr 0xa1-6" 
            tm.showerror( error_type, msg )
            return

        #type_id validation
        try:
            self.entries["type_id"] = int( self.entries["type_id"] )
            if not ( -2147483648 <= self.entries["type_id"] < 2147483648 ):
                raise
        except:
            msg = "Invalid Type_id: Must be an integer between -(2^31)-1 and (2^31)-1\nErr 0xa1-7" 
            tm.showerror( error_type, msg )
            return


        #No errors encountered
        return True

def run( userCx ):
    #Prevents use of app if user hasn't logged in.
    if userCx == None:
        tm.showerror( "Error", "You need to login before using this app.\nErr 0xa3-1" )
        return
    App3( userCx )
    return
