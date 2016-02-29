import cx_Oracle
import sys
import getpass

import apps.new_vehicle_registration as app1
import apps.auto_transaction as app2
import apps.driver_license_registration as app3
import apps.violation_records as app4
import apps.search_engine as app5

# Displays the introduction title for the ARS.
def welcome():
    welcomeMSG = "WELCOME TO THE AUTO REGISTRATION SYSTEM v0226"
    print( "\n" * 20 )
    print( "=" * 80 )
    print( "= " * 40 )
    print( welcomeMSG.center( 80 ) )
    print( "= " * 40 )
    print( "=" * 80 ) 
    print()

# gets an Oracle login for use with the program.
def login():
    con = ''
    firstTime = False
    while True:
        try:
            if not firstTime:
                print( "Leave the username blank if you wish to exit..." )
                firstTime = True

            user = input( "Oracle username: " )
            if len( user ) == 0:
                break

            if user == "DEBUG":
                return user

            pw = getpass.getpass()

            con_string = user + "/" + pw + "@gwynne.cs.ualberta.ca:1521/CRS"
            con = cx_Oracle.connect( con_string )
            if con == None:
                # The connection failed, raise Error to loop again.
                raise ValueError

            print( "\nSuccessfully connected to:", con.dsn, end="\n\n" )

            #con.autocommit = 1
            # idk what the above does tbh...

            # Return the connection
            return con

        except:
            print( "\nERROR:\tPLEASE CHECK YOUR USERNAME", end=" " )
            print( "AND PASSWORD AND TRY AGAIN...\n" )
            continue

    call_exit( con )

# Exits Python. Only use if the user has requested it.
def call_exit( userCx ):
    print()
    print( "EXITING...".center( 80 ) )
    
    try:
        userCx.close()
    except:
        if userCx == "":
            print( end="" )
        elif userCx != "DEBUG":
            print( "ERROR:\tuserCx.close() unsuccessful..." )
    
    print( "THANK YOU. HAVE A NICE DAY.".center( 80 ) )
    print()
    exit()

def getOptions():
    print()
    print( "[ 1 ]: NEW VEHICLE REGISTRATION" )
    print( "[ 2 ]: AUTO TRANSACTION" )
    print( "[ 3 ]: DRIVER LICENCE REGISTRATION" )
    print( "[ 4 ]: VIOLATION RECORDS" )
    print( "[ 5 ]: SEARCH ENGINE" )
    print( "[ ENTER ]: EXIT PROGRAM" )
    print()

def getError():
    print( "ERROR:\tINVALID OPTION.")
    print()

def menu( userCx ):
    print()
    print( "= " * 40 )
    print( "MAIN MENU".center( 80 ) )
    print( "( TYPE YOUR SELECTION )".center( 80 ) )
    print( "= " * 40 )
    getOptions()

    while True:
        choice = input( "CHOICE: " ).strip()

        # Check user's choice, run app, return/reload function to get title splash
        if len( choice ) == 0:
            call_exit( userCx )
            return
        elif choice == '1':
            app1.run( userCx )
            return
        elif choice == '2':
            app2.run( userCx )
            return
        elif choice == '3':
            app3.run( userCx )
            return
        elif choice == '4':
            app4.run( userCx )
            return
        elif choice == '5':
            app5.run( userCx )
            return
        else:
            getError()
            continue
        
        
def main():
    welcome()
    userCx = login()

    # loop menu title on return, user can only call call_exit in menu function.
    while True:
        menu( userCx )

if __name__ == '__main__':
    main()
