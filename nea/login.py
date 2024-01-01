import sqlite3
from hashlib import sha256
from re import fullmatch
import getpass
from databasesetup import Setup

class Login(object):

    def __init__(self,username=None, password=None):
        """Initialises the login class - a class is only used here to group functions better"""
        self.__username = username
        self.__password = password
        self.__userid = None
        self.__authenticated = False
        
        first = False #For checking if it is the first time setup for the database
        try: self.__conn = sqlite3.connect("file:master.db?mode=rw", uri=True) #If the database doesnt exist we need to do some extra stuff before registering
        except: self.__conn, first = sqlite3.connect("master.db"), True #Creates the database if it doesnt exist
        
        self.__c = self.__conn.cursor() #Setup the cursor for shorter commands

        if first == True: #If we just created the database then we need to setup the table for user log in.
            self.__firsttime()
        elif not((username is None) and (password is None)): #If the user has supplied values for both username and password
            #try: assert self.__userlookup() #Try to looku
            #except: raise Exception("User doesn't exist") #If not close the program. This shouldn't be too much p if the username existsof a concern as this class will be called by the tkinter interface
            if self.__login(): #runs the login function
                self.__authenticated = True #Change the authentication flag that allows other parts of the program to check if the user is logged in. Provides an easy way of avoiding errors later.
            else:
                print("Invalid username/password combination")
                exit(1)
        else:
            self.register() #Otherwise, the user just didnt supply any values for logging in so we make them a account. WIll probably e called through a tkinter button.
        #elf.__firsttime()
        ##############################################################
        #Enter main code here
        ##############################################################
        self.__conn.close() #close the cursor - not sure if i have to do this everywhere but i havent and it isnt breaking yet.

    def __firsttime(self):
        """First time setup for the user table in the database"""
        self.__c.execute('''CREATE TABLE users (userid INTEGER PRIMARY KEY, username UNIQUE NOT NULL, hash TEXT)''')
        self.__conn.commit() #Commits change, useful for testing and debugging as well as a generally safety precaution when modifying the database to allow for rollback
        Setup()
        self.register() #Register the user

    def __userlookup(self) -> bool:
        """Looks up if the user is in the database already. We have to perform a comparison on the string literal result of a fetchall on a select statement to check if the user exists"""
        return bool(str(self.__c.execute(f"SELECT username FROM users WHERE username='{self.__username}'").fetchall()) == "[(1,)]") #DUe to a quirk in how the sqlite select statment works: it doesnt return the results, it returns a cursor object
    
    
    def __login(self): #Private function because it should only ever be used in context of the class instance
        """Used to 'log in' the user: sets the userid parameter and its return results sets the authenticated parameter"""
        password = sha256(self.__password.encode()).hexdigest()
        userid = str(self.__c.execute(f"SELECT userid FROM users WHERE username ='{self.__username}' AND hash ='{password}'").fetchall())
        if userid == "[(1,)]": #Check if there are any results that match both hash and username
            self.__userid = userid
            return self.__userid
        else:
            return False
    
    def loggedin(self) -> bool:
        """Returns the state of the authenticated flag so that other functions and classes can see if a user is logged in"""
        return self.__authenticated #so that other functions can check
    
    def __validPassword(self) -> bool:
        """Uses regex statements to check if the password if of suitable strength and meets all the requirements"""
        return fullmatch(r"/(?=.*\d.*)(?=.*[a-zA-Z].*).{8,}/gm",self.__password) == None #at least one digit, one lowercase and one uppercase letter. At least 8 characters.

    def register(self) -> bool:
        """Register the user in the database"""
        self.__username = input("\nEnter a username to register: ")
        usernamecheck = str(self.__c.execute(f"SELECT COUNT(*) FROM users WHERE username='{self.__username}'").fetchall())
        while usernamecheck == "[(1,)]": #Uses the sqlite3 string literal for "Resuts exist" to verify 
            print("Username in use. Please pick another")
            self.__username = input("Enter a different username to register: ")
            usernamecheck = str(self.__c.execute(f"SELECT COUNT(*) FROM users WHERE username='{self.__username}'").fetchall())
        
        self.__password = getpass.getpass("Enter the password you want to use for this account: ")
        while self.__validPassword() != True: #Check if the password meets every requirement
            self.__password = getpass.getpass("Please enter a different password, Check it meets all the requirments (8 characters, at least one uppercase letter, lowercase letter and number must be present): ")
        
        hash = sha256(self.__password.encode()).hexdigest() #human and processing friendly string version of password hash in hexidecimal
        self.__c.execute(f'''INSERT INTO users(username,hash) VALUES(?,?)''',(self.__username,hash)) # No error checking is needed here because of the two loops earlier preventing databsae errors due to duplication
        self.__conn.commit() #Write changes
        return True #verfiy function ran correctly

    def getuserid(self) -> int:
        """Returns the userid of the currently logged in user, or None if there isn't one"""
        return self.__userid #Userid is techincally not private information anc could in theory be worked out, expecically for a small number of users over a short period of time. however: having userid set tp private means we can set authenticated flag if hash name and id all agree
     
    def __resetDatabase(self):
        """Used to reset the databsae for testing"""
        pass
