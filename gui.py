
from tkinter import *

# NEW VEHICLE REGISTRATION
def app1_command():
    print( "1 ha1e buttonz" )

# AUTO TRANSATCTION
def app2_command():
    print( "i ha2e buttons" )

# DRIVER LICENCE REGISTRATION
def app3_command():
    print( "i hat3 buttons" )

# VIOLATION RECORD 
def app4_command():
    print( "4 hate buttons" )

# SEARCH ENGINE
# probably need to import this to app1 but I'm laz.
def app5_command():
    top = Toplevel()
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

    def list1():
        print( strVar1.get() )

    button1 = Button( top, text="Search Drivers", command=list1 )
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

# MAIN =========================================================================
# could probably make this an object, but I want functionalitiy :/
top = Tk()
top.wm_title( "ARS v0228" )
top.resizable( width=FALSE, height=FALSE )
top.geometry( '{}x{}'.format( 250, 300 ) )

# App1 =========================================================================
info1 = "New Vehicle Registration:"
msg1 = Message( top, text=info1, padx=5, pady=5, width=200 )
msg1.pack()

top.app1_button = Button( top, padx=5, pady=5, width=50 )
top.app1_button["text"] = "goto"
top.app1_button["command"] = app1_command
top.app1_button.pack( side="top" )

# App2 =========================================================================
info2 = "Auto Transaction:"
msg2 = Message( top, text=info2, padx=5, pady=5, width=200 )
msg2.pack()

top.app2_button = Button( top, padx=5, pady=5, width=50 )
top.app2_button["text"] = "goto"
top.app2_button["command"] = app2_command
top.app2_button.pack( side="top" )

# App3 =========================================================================
info3 = "Driver Licence Registration:"
msg3 = Message( top, text=info3, padx=5, pady=5, width=200 )
msg3.pack()

top.app3_button = Button( top, padx=5, pady=5, width=50 )
top.app3_button["text"] = "goto"
top.app3_button["command"] = app3_command
top.app3_button.pack( side="top" )

# App4 =========================================================================
info4 = "Violation Record:"
msg4 = Message( top, text=info4, padx=5, pady=5, width=200 )
msg4.pack()

top.app4_button = Button( top, padx=5, pady=5, width=50 )
top.app4_button["text"] = "goto"
top.app4_button["command"] = app4_command
top.app4_button.pack( side="top" )

# App5 =========================================================================
info5 = "Search Engine:"
msg5 = Message( top, text=info5, padx=5, pady=5, width=200 )
msg5.pack()

top.app5_button = Button( top, padx=5, pady=5, width=50 )
top.app5_button["text"] = "goto"
top.app5_button["command"] = app5_command
top.app5_button.pack( side="top" )

top.mainloop()