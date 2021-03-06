''' New Persons Application '''

# This is a sub-application

from tkinter import *
import tkinter.messagebox as tm
import cx_Oracle
from datetime import datetime

#Run this app by calling NewPerson( parent_window, return_entry )
#parent_window: the window that owns the button that calls this app
#return_entry: An function from parent window that will be automatically
#              called with "sin" once this application finishes

class NewPerson( Toplevel ):
    def __init__( self, parent, return_entry=None ):
        Toplevel.__init__( self, parent )
        self.title( "New Persons Application" )
        self.resizable( width=FALSE, height=FALSE )

        self.parent = parent
        self.userCx = parent.userCx
        #Used to return the sin back to the previous window
        self.return_entry = return_entry 

        #Create and add widgets for Personal Information
        msgtext = "Personal Information"
        msg1 = Message( self, text=msgtext, padx=5, pady=5, width=200 )
        msg1.grid( row=0, sticky=N, columnspan=4 )

        sin_label = Label( self, text="SIN" )
        self.sin_entry = Entry( self )
        sin_label.grid( row=1, sticky=E )
        self.sin_entry.grid( row=1, column=1 )

        name_label = Label( self, text="Name" )
        self.name_entry = Entry( self )
        name_label.grid( row=1, column=2, sticky=E )
        self.name_entry.grid( row=1, column=3 )

        height_label = Label( self, text="Height" )
        self.height_entry = Entry( self )
        height_label.grid( row=2, sticky=E )
        self.height_entry.grid( row=2, column=1 )

        weight_label = Label( self, text="Weight" )
        self.weight_entry = Entry( self )
        weight_label.grid( row=2, column=2, sticky=E )
        self.weight_entry.grid( row=2, column=3 )

        eyecolor_label = Label( self, text="Eyecolor" )
        self.eyecolor_entry = Entry( self )
        eyecolor_label.grid( row=3, sticky=E )
        self.eyecolor_entry.grid( row=3, column=1 )

        haircolor_label = Label( self, text="Haircolor" )
        self.haircolor_entry = Entry( self )
        haircolor_label.grid( row=3, column=2, sticky=E )
        self.haircolor_entry.grid( row=3, column=3 )

        address_label = Label( self, text="Address" )
        self.address_entry = Entry( self )
        address_label.grid( row=4, sticky=E )
        self.address_entry.grid( row=4, column=1 )

        gender_label = Label( self, text="Gender" )
        self.gender_entry = Entry( self )
        gender_label.grid( row=4, column=2, sticky=E )
        self.gender_entry.grid( row=4, column=3 )

        birthday_label = Label( self, text="Birthday" )
        self.birthday_entry = Entry( self )
        birthday_label.grid( row=5, sticky=N+E )
        self.birthday_entry.grid( row=5, column=1, sticky=N )

        #Add submit button
        submit_button = Button( self, text="Submit", \
                                command=lambda: self.submit_form() )
        submit_button.grid( row=5, column=3, sticky=W )

    #Attempt to submit data to the database
    def submit_form( self ):

        self.entries = { "sin":       self.sin_entry.get().strip(),
                         "name":      self.name_entry.get().strip(),
                         "height":    self.height_entry.get(),
                         "weight":    self.weight_entry.get(),
                         "eyecolor":  self.eyecolor_entry.get().strip(),
                         "haircolor": self.haircolor_entry.get().strip(),
                         "address":   self.address_entry.get().strip(),
                         "gender":    self.gender_entry.get().strip(),
                         "birthday":  self.birthday_entry.get().strip() }

        #Check if input is valid
        if not self.validate_input():
            return

        msg = "Are you sure you want to submit?"
        if not tm.askyesno( "Submit Confirmation", msg ):
            return

        cursor = self.userCx.cursor()
        #Try to insert new person
        statement = "INSERT INTO people \
                     VALUES ( :sin, :name, :height, :weight, :eyecolor, \
                              :haircolor, :address, :gender, :birthday )"
        try:
            cursor.execute( statement, self.entries )
        #Source of this code: cx-oracle.readthedocs.org/en/latest/module/html
        except cx_Oracle.DatabaseError as exc:
            error, = exc.args
            if error.code == 1: #SIN must already exist
                tm.showerror("Submit Failure", "SIN '" + self.entries["sin"] + \
                              "' is already in the database\nErr 0xs1-11")
            else: #Unexpected Error
                tm.showerror("Submit Failure", error.message + "\nErr 0xs1-12")
            return
        finally:
            cursor.close()
        self.userCx.commit()

        #Success message
        successInfo = self.name_entry.get() + " has been added to the database"
        tm.showinfo( "Success!", successInfo )  
                
        #Return sin back to previous window
        if self.return_entry:
            return_entry = self.return_entry
            return_entry( self.entries["sin"] )

        self.destroy()

    #Type checking
    def validate_input( self ):
        error_type = "Input Error"

        #sin validation
        if self.entries["sin"] == '' or len( self.entries["sin"] ) > 15:
            msg = "Invalid SIN: Must not be blank or longer than 15 " + \
                  "characters\nErr 0xs1-1"
            tm.showerror( error_type, msg )
            return

        #name validation
        if self.entries["name"] == '' or len( self.entries["name"] ) > 40:
            msg = "Invalid Name: Must not be blank or longer than 40 " + \
                  "characters\nErr 0xs1-2"
            tm.showerror( error_type, msg )
            return

        #height validation
        try:
            self.entries["height"] = float( self.entries["height"] )
            if not ( 0 <= self.entries["height"] <= 999.99 ):
                raise
        except:
            msg = "Invalid Height: Must be a number between 0 and 999.99" + \
                  "\nErr 0xs1-3"
            tm.showerror( error_type, msg )
            return

        #weight validation
        try:
            self.entries["weight"] = float( self.entries["weight"] )
            if not ( 0 <= self.entries["weight"] <= 999.99 ):
                raise
        except:
            msg = "Invalid Weight: Must be a number between 0 and 999.99" + \
                  "\nErr 0xs1-4"
            tm.showerror( error_type, msg )
            return

        #eyecolor validation
        if self.entries["eyecolor"] == '' \
            or len( self.entries["eyecolor"] ) > 10:
            msg = "Invalid Eyecolor: Must not be blank or longer than 10 " + \
                  "characters\nErr 0xs1-5"
            tm.showerror( error_type, msg )
            return

        #haircolor validation
        if self.entries["haircolor"] == '' \
            or len( self.entries["haircolor"] ) > 10:
            msg = "Invalid Haircolor: Must not be blank or longer than 10 " + \
                  "characters\nErr 0xs1-6"
            tm.showerror( error_type, msg )
            return

        #address validation
        if self.entries["address"] == '' or len( self.entries["address"] ) > 50:
            msg = "Invalid Address: Must not be blank or longer than 50 " + \
                  "characters\nErr 0xs1-7"
            tm.showerror( error_type, msg )
            return

        #gender validation
        if self.entries["gender"] == '' \
            or self.entries["gender"][0].lower() not in ('m', 'f'):
            msg = "Invalid Gender: Enter either 'm' or 'f'\nErr 0xs1-8"
            tm.showerror( error_type, msg )
            return
        self.entries["gender"] = self.entries["gender"][0].lower()

        #birthday validation
        try:
            date = datetime.strptime( self.entries["birthday"], "%d-%b-%Y" )
        except:
            msg = "Invalid Birthday: Format must be DD-MMM-YYYY" + \
                  "\nEx: 04-OCT-2015\nErr 0xs1-9"
            tm.showerror( error_type, msg )
            return

        #Make sure birthday is in the past
        if date >= datetime.now():
            msg = "Invalid Birthday: Time travellers are not allowed" + \
                  "\nErr 0xs1-10"
            tm.showerror( error_type, msg )
            return

        #No errors detected!
        return True
