import cx_Oracle
import sys
import getpass

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

	call_exit()

# Exits Python. Only use if the user has requested it.
def call_exit():
	print()
	print( "EXITING...".center( 80 ) )
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
	print( "= " * 40 )
	print( "MAIN MENU".center( 80 ) )
	print( "( TYPE YOUR SELECTION )".center( 80 ) )
	print( "= " * 40 )
	getOptions()

	while True:
		choice = input( "CHOICE: " ).strip()

		if len( choice ) == 0:
			call_exit()

		if len( choice ) > 1:
			getError()
			continue

		try:
			choice = int( choice )
		except:
			getError()
			continue
def main():
    welcome()
    userCx = login()

    menu( userCx )

    try:
        userCx.close()
    except:
        if userCx != "DEBUG":
            print( "ERROR:\tuserCx.close() unsuccessful..." )
        else:
            print( "EXITING DEBUG MODE...".center( 80 ) )
            call_exit()

    call_exit()

if __name__ == '__main__':
    main()
