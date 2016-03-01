''' Search Engine Application '''
# SEARCH ENGINE
# probably need to import this to app1 but I'm laz.
def run( userCx ):
    top = Tk()
    top.title( "app1 TopLevel" )

    # msg = Message( top, text="This is app1!", padx=5, pady=5 )
    # msg.pack()

    # strVar1 = StringVar()
    # entry1 = Entry( top, textvariable=strVar1 )
    # entry1.pack()

    # def getText1():
    #     print( strVar1.get() )

    # strVar1.set( "enter words here" )

    # buttonGet1 = Button( top, text="Dismiss", command=getText1 )
    # buttonGet1.pack()

    # LIST1 ====================================================================
    info1 = "entering either a licence_no or a given name."
    msg1 = Message( top, text=info1, padx=5, pady=5 )
    msg1.pack()

    strVar1 = StringVar()
    strVar1.set( "Name or licence_no" )
    entry1 = Entry( top, textvariable=strVar1 )
    entry1.pack()

    def list1( userCx ):
        print( strVar1.get() )

    button1 = Button( top, text="Search Drivers", command=lambda: list1( userCx ) )
    button1.pack()

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
