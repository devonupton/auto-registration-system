''' Auto Transaction Application '''

from tkinter import *
import tkinter.messagebox as tm
import cx_Oracle
from datetime import datetime
from apps.new_persons_application import NewPerson

class App2( Toplevel ):
    def __init__( self, userCx ):
        Toplevel.__init__( self )
        self.title( "Auto Transaction Application" )
        self.userCx = userCx
        self.resizable( width=FALSE, height=FALSE )

        #Create and add widgets for Sale Info
        msg1 = Message( self, text="Sale Information", padx=5, pady=5, width=200 )
        msg1.grid( row=0, sticky=N, columnspan=2 )

        seller_id_label= Label( self, text="Seller ID" )
        self.seller_id_entry = Entry( self )
        seller_id_label.grid( row=1, sticky=E )
        self.seller_id_entry.grid( row=1, column=1 )

        transaction_id_label = Label( self, text="Transaction ID" )
        self.transaction_id_entry = Entry( self )
        transaction_id_label.grid( row=2, sticky=E )
        self.transaction_id_entry.grid( row=2, column=1 )

        vehicle_id_label = Label( self, text="Vehicle ID" )
        self.vehicle_id_entry = Entry( self )
        vehicle_id_label.grid( row=3, sticky=E )
        self.vehicle_id_entry.grid( row=3, column=1 )

        sale_date_label = Label( self, text="Sale Date" )
        self.sale_date_entry = Entry( self )
        sale_date_label.grid( row=4, sticky=E )
        self.sale_date_entry.grid( row=4, column=1 )
        self.sale_date_entry.insert( 0, datetime.now().strftime( "%d-%b-%Y" ) )

        price_label = Label( self, text="Price ($)" )
        self.price_entry = Entry( self )
        price_label.grid( row=5, sticky=E )
        self.price_entry.grid( row=5, column=1 )

        row_expander = Label( self, text="" ) #Create an extra blank row
        row_expander.grid( row=6 )

        #Create and add widgets for Buyer info
        msg2 = Message( self, text="Buyer Information", padx=5, pady=5, width=200 )
        msg2.grid( row=0, column=2, sticky=N, columnspan=2 )

        buyer_id_label = Label( self, text="Buyer ID" )
        self.buyer_id_entry = Entry( self )
        buyer_id_label.grid( row=1, column=2, sticky=E )
        self.buyer_id_entry.grid( row=1, column=3 )

        owner_list_label = Label( self, text="Other Owner ID's" )
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
        self.seller_id = self.seller_id_entry.get().strip()
        self.transaction_id = self.transaction_id_entry.get().strip()
        self.vehicle_id = self.vehicle_id_entry.get().strip()
        self.sale_date = self.sale_date_entry.get().strip()
        self.price = self.price_entry.get()
        self.buyer_id = self.buyer_id_entry.get().strip()
        self.owner_id_list = self.owner_list_entry.get().split( "," )
        for element in range(len(self.owner_id_list)):
            self.owner_id_list[element] = self.owner_id_list[element].strip()

        if not self.validate_input():
            return

        #####################################################

        if not tm.askyesno( "Submit Confirmation", "Are you sure you want to submit?" ):
            return

        cursor = self.userCx.cursor()
        error_type = "Submit Failure"
        cursor.execute( "SAVEPOINT App2Save" )
        
        #####################################################

        #Make sure seller is primary owner of the vehicle
        statement = "SELECT owner_id FROM owner \
                     WHERE owner_id=:a and vehicle_id=:b and is_primary_owner='y'" 
        cursor.execute( statement, a=self.seller_id.ljust(15), b=self.vehicle_id.ljust(15) )
        if len( cursor.fetchall() ) == 0: #Not in system

            #Check if sin exists
            test1 = "SELECT sin FROM people WHERE sin=:a"
            try:
                cursor.execute( test1, a=self.seller_id.ljust(15) )
            except: #Unknown error
                tm.showerror( error_type, "Unexpected Error\nErr 0xa2-11" )
                return

            if len( cursor.fetchall() ) == 0:
                tm.showerror( error_type, "Seller ID '" + self.seller_id + "' does not exist\nErr 0xa2-12" )
                cursor.close()
                return

            #Check if vehicle_id exists
            test2 = "SELECT serial_no FROM vehicle WHERE serial_no=:a"
            try:
                cursor.execute( test2, a=self.vehicle_id.ljust(15) )
            except: #Unknown error
                tm.showerror( error_type, "Unexpected Error\nErr 0xa2-13" )
                return

            if len( cursor.fetchall() ) == 0:
                tm.showerror( error_type, "Vehicle ID '" + self.vehicle_id + "' does not exist\nErr 0xa2-14" )

            #Else, seller not prmiary owner
            else:
                tm.showerror( error_type, "The seller does not have permission to sell this vehicle:\
                                           Must be Primary Owner\nErr 0xa2-15" )
            cursor.close()
            return

        #####################################################

        #Create the auto_sale
        sale_statement = "INSERT INTO auto_sale VALUES( :a, :b, :c, :d, :e, :f )"
        try:
            cursor.execute( sale_statement, a=self.transaction_id, b=self.seller_id, \
                            c=self.buyer_id, d=self.vehicle_id, e=self.sale_date, f=self.price )
        except cx_Oracle.DatabaseError as exc:
            cursor.execute( "ROLLBACK to App2Save" )
            cursor.close()
            error, = exc.args
            if error.code == 1: #Transaction ID already exists
                tm.showerror( error_type, "Transaction ID '" + \
                    str(self.transaction_id) + "' is already in the database\nErr 0xa2-16" )
            elif error.code == 2291: #Seller and vehicle already verified -> Buyer does not exist
                tm.showerror( error_type, "Buyer ID '" + \
                    self.buyer_id + "' does not exist\nErr 0xa2-17" )
            else: #Unknown error
                tm.showerror( error_type, error.message + "\nErr 0xa2-18" )
            return
                
        #####################################################

        #Delete old owners
        try:
            cursor.execute( "DELETE FROM owner WHERE vehicle_id=:a", a=self.vehicle_id.ljust(15) )
        except cx_Oracle.DatabaseError as exc:
            cursor.execute( "ROLLBACK to App2Save" )
            cursor.close()
            error, = exc.args
            #Unknown error
            tm.showerror( error_type, error.message + "\nErr 0xa2-19" )
            return

        #####################################################

        #Try to insert Primary owner
        primary_owner_statement = "INSERT INTO owner VALUES( :a, :b, 'y' )"
        try:
            cursor.execute( primary_owner_statement, a=self.buyer_id, b=self.vehicle_id )
        except cx_Oracle.DatabaseError as exc:
            cursor.execute("ROLLBACK to App2Save" )
            cursor.close()
            error, = exc.args
            if error.code == 2291: #Buyer ID does not exist
                tm.showerror( error_type, "Buyer ID '" + self.seller_id + "' does not exist\nErr 0xa2-20" )
            elif error.code == 1400: #Primary_owner_id was empty string (read as NULL)
                tm.showerror( error_type, "You must have exactly one primary owner\nErr 0xa2-21" )
            else: #Unknown error
                tm.showerror( error_type, error.message + "\nErr 0xa2-22" )
            return

        #####################################################

        #Try to insert other owners
        secondary_owner_statement = "INSERT INTO owner VALUES( :a, :b, 'n' )"
        for owner_id in self.owner_id_list:
            try:
                cursor.execute( secondary_owner_statement, a=owner_id, b=self.vehicle_id )
            except cx_Oracle.DatabaseError as exc:
                cursor.execute("ROLLBACK to App2Save" )
                cursor.close()
                error, = exc.args
                if error.code == 1: #Duplicate owner_id
                    tm.showerror( error_type, "Owner ID '" + owner_id + "' entered more than once\nErr 0xa2-23" )
                elif error.code == 2291: #Owner ID does not exist
                    tm.showerror( error_type, "Owner ID '" + owner_id + "' does not exist\nErr 0xa2-24" )
                else: #Unknown error
                    tm.showerror( error_type, error.message + "\nErr 0xa2-25" )
                return

        #####################################################

        #SQL statements executed successfully
        cursor.close()
        self.userCx.commit()

        #Success message
        successInfo = "Vehicle '" + self.vehicle_id + "' has been sold\n" + \
                      "New Primary Owner ID: " + self.buyer_id + "\n" + \
                      "Other new Owner ID's: " + ", ".join(self.owner_id_list)
        tm.showinfo( "Success!", successInfo )  
        self.destroy()
            
    #Type checking
    def validate_input( self ):
        error_type = "Input Error"

        #seller_id validation 
        if self.seller_id == '' or len( self.seller_id ) > 15:
            msg = "Invalid Seller ID: Must not be blank or longer than 15 character\nErr 0xa2-2"
            tm.showerror( error_type, msg )
            return

        #transaction_id validation
        try:
            self.transaction_id = int( self.transaction_id )
            if not ( -2147483648 <= self.transaction_id < 2147483648 ):
                raise
        except:
            msg = "Invalid Transaction ID: Must be an integer between -(2^31)-1 and (2^31)-1\nErr 0xa2-3"
            tm.showerror( error_type, msg )
            return

        #vehicle_id validation
        if self.vehicle_id == '' or len( self.vehicle_id ) > 15:
            msg = "Invalid Vehicle ID: Must not be blank or longer than 15 characters\nErr 0xa2-4"
            tm.showerror( error_type, msg )
            return

        #sale_date validation
        try:
            date = datetime.strptime( self.sale_date, "%d-%b-%Y" )
        except:
            msg = "Invalid Sale Date: Format must be DD-MMM-YYYY\nEx: 04-OCT-2015\nErr 0xa2-5"
            tm.showerror( error_type, msg )
            return
        if date > datetime.now():
            msg = "Invalid Sale Date: Sale cannot occur in the future\nErr 0xa2-6"
            tm.showerror( error_type, msg )
            return
        elif date.date() < datetime.now().date():
            if not tm.askyesno( "Input Confirmation", "The sale date is listed as before today. Is that correct?" ):
                return

        #price validation
        try:
            self.price = float( self.price )
            if not ( 0 <= self.price < 10000000 ):
                raise
        except:
            msg = "Invalid Price: Must be a number between 0 and 9999999\nErr 0xa2-7"
            tm.showerror( error_type, msg )
            return

        #buyer_id validation
        if self.buyer_id == '' or len( self.buyer_id ) > 15:
            msg = "Invalid Buyer ID: Must not be blank or longer than 15 characters\nErr 0xa2-8"
            tm.showerror( error_type, msg )
            return

        #buyer != seller
        if self.buyer_id == self.seller_id:
            msg = "Invalid Buyer ID: The seller cannot sell to themself\nErr 0xa2-9"
            tm.showerror( error_type, msg )
            return

        if self.owner_id_list == ['']:
            self.owner_id_list = []
        #owner_id validation
        for owner_id in self.owner_id_list:
            if owner_id == '' or len( owner_id ) > 15:
                msg = "Invalid Owner ID '" + owner_id + "': Must not be blank or longer than 15 characters\nErr 0xa2-10"
                tm.showerror( error_type, msg )
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
