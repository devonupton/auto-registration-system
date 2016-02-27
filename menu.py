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
			pw = getpass.getpass()
			con_string = user + "/" + pw + "@gwynne.cs.ualberta.ca:1521/CRS"
			con = cx_Oracle.connect( con_string )
			if con == None:
				raise ValueError
			con.autocommit = 1
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

welcome()
userCx = login()

userCx.close()
try:
	userCx.close()
except:
	print( "userCx.close() successful...")

call_exit()