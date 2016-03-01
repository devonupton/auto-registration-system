''' Search Engine Application '''

from tkinter import *
import tkinter.messagebox as tm
import cx_Oracle

def run( userCx ):
    # prevents use of app if user hasn't logged in.
    #if userCx == None:
    #    tm.showerror( "Error", "You need to login before using this app.\nErr 0xa5-1" )
    #    return
    
    top = Tk()
    top.title( "app1 TopLevel" )

    # LIST1 ====================================================================
    info1 = "entering either a licence_no or a given name."
    msg1 = Message( top, text=info1, padx=5, pady=5, width=200 )
    msg1.grid( row=0, sticky=N, columnspan=2 )

    name_strVar = StringVar()
    name_strVar.set( "Enter Name" )
    name_entry = Entry( top, textvariable=name_strVar )
    name_entry.grid( row=1, column=0, sticky=W )
    
    licNo_strVar = StringVar()
    licNo_strVar.set( "Enter licence_no" )
    licNo_entry = Entry( top, textvariable=licNo_strVar )
    licNo_entry.grid( row=1, column=1, sticky=E )

    def searchOne( userCx, strVar, isLicNo ):
        if isLicNo:
            print( "LicNo:", strVar.get() )
        else:
            print( "Name:", strVar.get() )
    
    searchName_button = Button( top, text="Search By Name", command=lambda: searchOne( userCx, name_strVar, False ) )
    searchName_button.grid( row=2, column=0, sticky=W )
    
    searchLicNo_button = Button( top, text="Search By licence_no", command=lambda: searchOne( userCx, LicNo_strVar, True ) )
    searchLicNo_button.grid( row=2, column=1, sticky=E )

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
