''' Auto Transaction Application '''

from tkinter import *
import tkinter.messagebox as tm
import cx_Oracle
import datetime
from apps.new_persons_application import NewPerson

class App2( Toplevel ):
    def __init__( self, userCx ):
        Toplevel.__init__( self )
        self.title( "Auto Transaction Application" )
        self.userCx = userCx

        #Create and add widgets for Sale Info
        msg1 = Message( self, text="Sale Information", padx=5, pady=5, width=200 )
        msg1.grid( row=0, sticky=N, columnspan=2 )

        seller_id_label= Label( self, text="Seller_id" )
        self.seller_id_entry = Entry( self )
        seller_id_label.grid( row=1, sticky=E )
        self.seller_id_entry.grid( row=1, column=1 )

        transaction_id_label = Label( self, text="Transaction_id" )
        self.transaction_id_entry = Entry( self )
        transaction_id_label.grid( row=2, sticky=E )
        self.transaction_id_entry.grid( row=2, column=1 )

        vehicle_id_label = Label( self, text="Vehicle_id" )
        self.vehicle_id_entry = Entry( self )
        vehicle_id_label.grid( row=3, sticky=E )
        self.vehicle_id_entry.grid( row=3, column=1 )

        sale_date_label = Label( self, text="Sale Date" )
        self.sale_date_entry = Entry( self )
        sale_date_label.grid( row=4, sticky=E )
        self.sale_date_entry.grid( row=4, column=1 )
        self.sale_date_entry.insert( 0, datetime.datetime.now().strftime( "%d-%b-%Y" ) )

        sale_price_label = Label( self, text="Sale Price" )
        self.sale_price_entry = Entry( self )
        sale_price_label.grid( row=5, sticky=E )
        self.sale_price_entry.grid( row=5, column=1 )

        row_expander = Label( self, text="" ) #Create an extra blank row
        row_expander.grid( row=6 )

        #Create and add widgets for Buyer info
        msg2 = Message( self, text="Buyer Information", padx=5, pady=5, width=200 )
        msg2.grid( row=0, column=2, sticky=N, columnspan=2 )

        buyer_id_label = Label( self, text="Buyer_id" )
        self.buyer_id_entry = Entry( self )
        buyer_id_label.grid( row=1, column=2, sticky=E )
        self.buyer_id_entry.grid( row=1, column=3 )

        owner_list_label = Label( self, text="Other Owner_id's" )
        self.owner_list_entry = Entry( self )
        owner_list_label.grid( row=2, column=2, sticky=E )
        self.owner_list_entry.grid( row=2, column=3 )

        owner_list_label2 = Label( self, text="(comma separated list of sin #'s)" )
        owner_list_label2.grid( row=3, column=2, columnspan=2, )

        #Buttons
        new_person_button = Button( self, text="Add new Person", \
                                    command=lambda: NewPerson( self, self.autofill ) )
        new_person_button.grid( row=3, column=2, rowspan=3, columnspan=2, )

        submit_button = Button( self, text="Submit", command=lambda: self.submit_form() )
        submit_button.grid( row=5, column=2, rowspan=2, columnspan=2, )

    #Used to fill the sin # upon returning from NewPerson app
    def autofill( self, value ):
        if self.buyer_id_entry.get() == "":
            self.buyer_id_entry.insert( 0, value )
        elif self.owner_list_entry.get() == "":
            self.owner_list_entry.insert( 0, value )
        else:
            self.owner_list_entry.insert( END, ", " + value )

    #Attempt to submit data to the database
    def submit_form( self ):

        #Get each input value
        self.seller_id = self.seller_id_entry.get()
        self.transaction_id = self.transaction_id_entry.get()
        self.vehicle_id = self.vehicle_id_entry.get()
        self.sale_date = self.sale_date_entry.get()
        self.sale_price = self.sale_price_entry.get()
        self.buyer_id = self.buyer_id_entry.get()
        self.owner_id_list = self.owner_list_entry.get().replace( " ", "" ).split( "," )

        if not self.validate_input():
            return

        if not tm.askyesno( "Submit Confirmation", "Are you sure you want to submit?" ):
            return

        #############################
        # INCOMPLETE
        ############################
        tm.showerror( "CONSTRUCTION ZONE" , "Incomplete Feature, come back later" )
        return
            
    #Type checking
    def validate_input( self ):
        error_type = "Input Error"

        if self.seller_id == '' or len( self.seller_id ) > 15:
            tm.showerror( error_type, "Invalid Seller_id: Length must be between 1 and 15\nErr 0xa2-2" )
            return
        try:
            self.transaction_id = int( self.transaction_id )
            if not ( -2147483648 <= self.transaction_id < 2147483648 ):
                raise
        except:
            tm.showerror( error_type, "Invalid Transaction_id: Must be an integer between -(2^31)-1 and (2^31)-1\nErr 0xa2-3" )
            return
        if self.vehicle_id == '' or len( self.vehicle_id ) > 15:
            tm.showerror( error_type, "Invalid Vehicle_id: Length must be between 1 and 15\nErr 0xa2-4" )
            return
        try:
            datetime.datetime.strptime( self.sale_date, "%d-%b-%Y" )
        except:
            tm.showerror( error_type, "Invalid Sale Date: Format must be DD-MMM-YYYY\nEx: 04-OCT-2015\nErr 0xa2-5" )
            return
        try:
            self.sale_price = float( self.sale_price )
            if not ( 0 <= self.sale_price < 10000000 ):
                raise
        except:
            tm.showerror( error_type, "Invalid Sale Price: Must be a number between 0 and 9999999\nErr 0xa2-6" )
            return
        if self.buyer_id == '' or len( self.buyer_id ) > 15:
            tm.showerror( error_type, "Invalid Buyer_id: Length must be between 1 and 15\nErr 0xa2-7" )
            return
        if self.owner_id_list == ['']:
            self.owner_id_list = []
        for owner_id in self.owner_id_list:
            if len( owner_id ) > 15:
                tm.showerror( error_type, "Invalid Owner_id '" + owner_id + "': Length must be between 1 and 15\nErr 0xa2-8" )
                return

        #No errors encountered
        return True

def run( userCx ):
    #Prevents use of app if user hasn't logged in.
    if userCx == None:
        tm.showerror( "Error", "You need to login before using this app.\nErr 0xa2-1" )
        return
    App2( userCx )
    return
