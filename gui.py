
from tkinter import *

def app1_command():
    top = Toplevel()
    top.title( "app1 TopLevel" )

    msg = Message( top, text="This is app1!", padx=5, pady=5 )
    msg.pack()

    button = Button( top, text="Dismiss", command=top.destroy )
    button.pack()

def app2_command():
    print( "i ha2e buttons" )

def app3_command():
    print( "i hat3 buttons" )

def app4_command():
    print( "4 hate buttons" )

def app5_command():
    print( "i h5te button5" )

# could probably make this an object, but I want functionalitiy :/
top = Tk()

# App1 button
top.app1_button = Button(top)
top.app1_button["text"] = "app1"
top.app1_button["command"] = app1_command
top.app1_button.pack( side="top" )

# App2 button
top.app2_button = Button(top)
top.app2_button["text"] = "app2"
top.app2_button["command"] = app2_command
top.app2_button.pack( side="top" )

# App3 button
top.app3_button = Button(top)
top.app3_button["text"] = "app3"
top.app3_button["command"] = app3_command
top.app3_button.pack( side="top" )

# App4 button
top.app4_button = Button(top)
top.app4_button["text"] = "app4"
top.app4_button["command"] = app4_command
top.app4_button.pack( side="top" )

# App5 button
top.app5_button = Button(top)
top.app5_button["text"] = "app5"
top.app5_button["command"] = app5_command
top.app5_button.pack( side="top" )

top.mainloop()