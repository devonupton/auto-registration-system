''' New Vehicle Registration Application '''

from tkinter import *
import tkinter.messagebox as tm
import cx_Oracle

class App1( Toplevel ):
    def __init__( self, userCx ):
        Toplevel.__init__( self )
        self.title( "app1: New Vehicle Registration Application" )
        self.userCx = userCx

        #Create all the widgets for vehicle info
        msg1 = Message( self, text="Vehicle Information", padx=5, pady=5, width=200 )

        serial_no_label = Label( self, text="serial_no" )
        self.serial_no_entry = Entry( self )

        maker_label = Label( self, text="maker" )
        self.maker_entry = Entry( self )

        model_label = Label( self, text="model" )
        self.model_entry = Entry( self )

        year_label = Label( self, text="year" )
        self.year_entry = Entry( self )

        color_label = Label( self, text="color" )
        self.color_entry = Entry( self )

        type_id_label = Label( self, text="type_id" )
        self.type_id_entry = Entry( self )

        #Add widgets to frame
        msg1.grid( row=0, sticky=N, columnspan=2 )
        serial_no_label.grid( row=1, sticky=E )
        self.serial_no_entry.grid( row=1, column=1 )

        maker_label.grid( row=2, sticky=E )
        self.maker_entry.grid( row=2, column=1 )
        
        model_label.grid( row=3, sticky=E )
        self.model_entry.grid( row=3, column=1 )

        year_label.grid( row=4, sticky=E )
        self.year_entry.grid( row=4, column=1 )

        color_label.grid( row=5, sticky=E )
        self.color_entry.grid( row=5, column=1 )

        type_id_label.grid( row=6, sticky=E )
        self.type_id_entry.grid( row=6, column=1 )

        #Create all the widgets for personal info
        msg2 = Message( self, text="Personal Information", padx=5, pady=5, width=200 )

        sin_label = Label( self, text="sin" )
        self.sin_entry = Entry( self )
        new_person_button = Button( self, text="Add new Person",  command=lambda: NewPerson( self ) )

        #Add widgets to frame
        msg2.grid( row=0, column=2, sticky=N, columnspan=2 )

        sin_label.grid( row=1, column=2, sticky=E )
        self.sin_entry.grid( row=1, column=3 )

        new_person_button.grid( row=2, column=3, sticky=W )

        #Last few widgets
        self.primary_owner = IntVar()
        self.is_primary_owner_check = Checkbutton( self, text="Primary Owner", variable = self.primary_owner )
        self.is_primary_owner_check.grid( row=4, column=3 , sticky=W )

        submit_button = Button( self, text="Submit", command=lambda: self.submit_form() )
        submit_button.grid( row=5, column=3, sticky=W )

    def submit_form( self ):

        #####################
        # Incomplete
        ####################

        tm.showerror( "Construction Zone", "Feature incomplete" )


class NewPerson( Toplevel ):
    def __init__( self, main_app):
        Toplevel.__init__( self )
        self.title( "New Persons Application" )
        self.userCx = main_app.userCx
        self.main_app = main_app

        #Create widgets
        msg1 = Message( self, text="Personal Information", padx=5, pady=5, width=200 )

        sin_label = Label( self, text="sin" )
        self.sin_entry = Entry( self )

        name_label = Label( self, text="name" )
        self.name_entry = Entry( self )

        height_label = Label( self, text="height" )
        self.height_entry = Entry( self )

        weight_label = Label( self, text="weight" )
        self.weight_entry = Entry( self )

        eyecolor_label = Label( self, text="eyecolor" )
        self.eyecolor_entry = Entry( self )

        haircolor_label = Label( self, text="haircolor" )
        self.haircolor_entry = Entry( self )

        address_label = Label( self, text="address" )
        self.address_entry = Entry( self )

        gender_label = Label( self, text="gender" )
        self.gender_entry = Entry( self )

        birthday_label = Label( self, text="birthday (DD-MMM-YYYY)" )
        self.birthday_entry = Entry( self )

        #Add widgets to frame
        msg1.grid( row=0, sticky=N, columnspan=4 )

        sin_label.grid( row=1, sticky=E )
        self.sin_entry.grid( row=1, column=1 )

        name_label.grid( row=1, column=2, sticky=E )
        self.name_entry.grid( row=1, column=3 )

        height_label.grid( row=2, sticky=E )
        self.height_entry.grid( row=2, column=1 )

        weight_label.grid( row=2, column=2, sticky=E )
        self.weight_entry.grid( row=2, column=3 )

        eyecolor_label.grid( row=3, sticky=E )
        self.eyecolor_entry.grid( row=3, column=1 )

        haircolor_label.grid( row=3, column=2, sticky=E )
        self.haircolor_entry.grid( row=3, column=3 )

        address_label.grid( row=4, sticky=E )
        self.address_entry.grid( row=4, column=1 )
        
        gender_label.grid( row=4, column=2, sticky=E)
        self.gender_entry.grid( row=4, column=3 )

        birthday_label.grid( row=9, sticky=E, columnspan=3 )
        self.birthday_entry.grid( row=9, column=3 )

        #Add submit button
        submit_button = Button( self, text="Submit", command=lambda: self.submit_form() )
        submit_button.grid( row=9, sticky=W )

    def submit_form( self ):

        #####################
        # Incomplete
        ####################

        self.main_app.sin_entry.delete( 0, END )
        self.main_app.sin_entry.insert( 0, self.sin_entry.get() )
        successInfo = self.name_entry.get() + " has been added to the database"
        tm.showinfo( "Success!", successInfo )  
        self.destroy()

def run( userCx ):
    # prevents use of app if user hasn't logged in.
    if userCx == None:
        tm.showerror( "Error", "You need to login before using this app.\nErr 0xa1-1" )
        return
    App1( userCx )
    return




