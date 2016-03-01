''' Search Engine Application '''

from tkinter import *
import tkinter.messagebox as tm
import cx_Oracle

# List the name, licence_no, addr, birthday, driving class,
# driving_condition, and the expiring_data of a driver by entering either 
# a licence_no or a given name. It shall display all the entries if a
# duplicate name is given.
def searchOne( userCx, strVar, isLicNo ):
        if len( strVar ) < 1:
            type = "licence_no" if isLicNo else "Name"
            tm.showerror( "Invalid Input", "You need to specifiy a " +\
                          type + " to search!\nErr 0xa5-2" )
            return
            
        if isLicNo:
            statement = "SELECT P.name, L.licence_no, P.addr, P.birthday, L.class, L.expiring_date " +\
                        "FROM People P, drive_Licence L "+\
                        "WHERE P.sin = L.sin " + "AND L.licence_no = " + "'" + strVar + "'"
        else:
            statement = "SELECT * FROM People"
            
        print( statement )
        thisCursor = userCx.cursor()
        try:
            thisCursor.execute( statement )
        except:
            tm.showerror( "Invalid Input", "There is a problem with your search option, please try again." )
        rows = thisCursor.fetchall()
        print( len(rows) )
        for row in rows:
            print( row )

def run( userCx ):
    # prevents use of app if user hasn't logged in.
    if userCx == None:
        tm.showerror( "Error", "You need to login before using this app.\nErr 0xa5-1" )
        return
    
    top = Tk()
    top.title( "app5: Search Engine" )

    # LIST1 ====================================================================
    info1 = "entering either a licence_no or a given name."
    msg1 = Message( top, text=info1, padx=5, pady=5, width=200 )
    msg1.grid( row=0, sticky=N, columnspan=2 )

    #name_strVar = StringVar()
    #name_strVar.set( "Enter Name" )
    name_entry = Entry( top )
    name_entry.grid( row=1, column=0, sticky=EW )
    name_entry.insert( 0, "Enter a name...")
    
    #licNo_strVar = StringVar()
    licNo_entry = Entry( top )
    #licNo_strVar.set( "Enter licence_no" )
    licNo_entry.grid( row=1, column=1, sticky=EW )
    licNo_entry.insert( 0, "Enter a licence_no..." )
    
    searchName_button = Button( top, text="Search By Name", command=lambda: searchOne( userCx, name_entry.get(), False ) )
    searchName_button.grid( row=2, column=0, sticky=EW )
    
    searchLicNo_button = Button( top, text="Search By licence_no", command=lambda: searchOne( userCx, licNo_entry.get(), True ) )
    searchLicNo_button.grid( row=2, column=1, sticky=EW )

    mainloop()
    
    # LIST2 ====================================================================
    info2 = "drive licence_no or sin of a person  is entered."
    msg2 = Message( top, text=info2, padx=5, pady=5 )
    msg2.pack()

    strVar2 = StringVar()
    strVar2.set( "Licence_no or SIN" )
    entry2 = Entry( top, textvariable=strVar2 )
    entry2.pack()

    def list2():
        print( strVar2.get() )

    button2 = Button( top, text="Search Violations", command=list2 )
    button2.pack()

    # LIST3 ====================================================================
    info3 = "entering the vehicle's serial number."
    msg3 = Message( top, text=info3, padx=5, pady=5 )
    msg3.pack()

    strVar3 = StringVar()
    strVar3.set( "Enter a VIN" )
    entry3 = Entry( top, textvariable=strVar3 )
    entry3.pack()

    # Perform the search for 
    def list3():
        print( strVar3.get() )

    button3 = Button( top, text="Search Vehicle History", command=list3 )
    button3.pack()

    #mainloop
    mainloop()