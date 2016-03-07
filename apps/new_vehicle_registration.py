''' New Vehicle Registration Application '''

from tkinter import *
import tkinter.messagebox as tm
import cx_Oracle
from apps.new_persons_application import NewPerson

class App1( Toplevel ):
    def __init__( self, userCx ):
        Toplevel.__init__( self )
        self.title( "app1: New Vehicle Registration Application" )
        self.userCx = userCx

        #Create all the widgets for vehicle info
        msg1 = Message( self, text="Vehicle Information", padx=5, pady=5, width=200 )

        serial_no_label = Label( self, text="Serial_no" )
        self.serial_no_entry = Entry( self )

        maker_label = Label( self, text="Maker" )
        self.maker_entry = Entry( self )

        model_label = Label( self, text="Model" )
        self.model_entry = Entry( self )

        year_label = Label( self, text="Year" )
        self.year_entry = Entry( self )

        color_label = Label( self, text="Color" )
        self.color_entry = Entry( self )

        type_id_label = Label( self, text="Type_id" )
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

        primary_owner_id_label = Label( self, text="Primary Owner_id" )
        self.primary_owner_id_entry = Entry( self )

        owner_id_label = Label( self, text="Other Owner_id's" )
        owner_id_label2 = Label( self, text="(comma separated list of sin #'s)" )
        self.owner_id_entry = Entry( self )

        new_person_button = Button( self, text="Add new Person", \
                                    command=lambda: NewPerson( self, self.autofill ) )

        #Add widgets to frame
        msg2.grid( row=0, column=2, sticky=N, columnspan=2 )

        primary_owner_id_label.grid( row=1, column=2, sticky=E )
        self.primary_owner_id_entry.grid( row=1, column=3 )

        owner_id_label.grid( row=2, column=2, sticky=E )
        self.owner_id_entry.grid( row=2, column=3 )

        owner_id_label2.grid( row=3, column=2, columnspan=2, )

        new_person_button.grid( row=3, column=2, rowspan=3, columnspan=2, )

        #Submit button
        submit_button = Button( self, text="Submit", command=lambda: self.submit_form() )
        submit_button.grid( row=5, column=2, rowspan=2, columnspan=2, )

    def autofill( self, value ):
        if self.primary_owner_id_entry.get() == "":
            self.primary_owner_id_entry.insert( 0, value )
        elif self.owner_id_entry.get() == "":
            self.owner_id_entry.insert( 0, value )
        else:
            self.owner_id_entry.insert( END, ", " + value )

    def submit_form( self ):

        #####################
        # Incomplete
        ####################

        tm.showerror( "Construction Zone", "Feature incomplete" )

def run( userCx ):
    # prevents use of app if user hasn't logged in.

    ####Testing!!!!
    #userCx = True
    ####Testing!!!!

    if userCx == None:
        tm.showerror( "Error", "You need to login before using this app.\nErr 0xa1-1" )
        return
    App1( userCx )
    return




