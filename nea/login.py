import sqlite3
from hashlib import sha256
from re import fullmatch
import getpass
from databasesetup import Setup


class Login(object):
    """The login class contains all the necessary functionality for a user access control system"""
    def __init__(self, username=None, password=None) -> None:
        """
        Initialises the login class - a class is only used here to group functions better
        @param username: Username to log in with
        @param password: User password
        @return: None
        """
        self.__username = username
        self.__password = password
        self.__userid = None
        self.__authenticated = False
        first = False  # For checking if it is the first time setup for the database
        try:
            self.__conn = sqlite3.connect("file:master.db?mode=rw", uri=True)
            # If the database doesn't exist, we need to do some extra stuff before registering
        except sqlite3.Error:
            self.__conn, first = sqlite3.connect("master.db"), True  # Creates the database if it doesn't exist

        self.__c = self.__conn.cursor()  # Set up the cursor for shorter commands

        if first:  # If we just created the database, then we need to set up the table for user log in.
            self.__firsttime()
        elif not ((username is None) and (password is None)):
            # If the user has supplied values for both username and password
            if self.__login():  # runs the login function
                self.__authenticated = True
                # Change the authentication flag that allows other parts of the program
                # to check if the user is logged in.
                # This provides an easy way of avoiding errors later.
            else:
                print("Invalid username/password combination")
                exit(1)
        else:
            self.register()
            # Otherwise, the user just didn't supply any values for logging in, so we make them an account.
            # Will probably be called through a tkinter button.

        self.__conn.close()
        # close the cursor - not sure if I have to do this everywhere, but I haven't, and it isn't breaking yet.

    def __firsttime(self) -> None:
        """
        First time setup for the user table in the database
        @return: None
        """
        self.__c.execute('''CREATE TABLE users (userid INTEGER PRIMARY KEY, username UNIQUE NOT NULL, hash TEXT)''')
        self.__conn.commit()
        # Commits change, useful for testing and debugging as well as a generally safety precaution when modifying
        # the database to allow for rollback
        Setup()
        self.register()  # Register the user

    def __userlookup(self) -> bool:
        """
        It looks up if the user is in the database already.
        We have to perform a comparison on the string literal result of a fetchall on a select statement
        to check if the user exists
        @return: True if the user is in the table, false otherwise"""
        return bool(str(self.__c.execute(
            f"SELECT username FROM users WHERE username='{self.__username}'").fetchall()) == "[(1,)]")
        # Due to a quirk in how the sqlite select statement works: it doesn't return the results,
        # it returns a cursor object

    def __login(self) -> str | bool:
        """
        Used to 'log in' the user: sets the userid parameter, and its return results sets the authenticated
        parameter.
        Private function because it should only ever be used in the context of the class instance
        @return: userid if successful, False otherwise
        """
        password = sha256(self.__password.encode()).hexdigest()
        userid = str(self.__c.execute(
            f"SELECT userid FROM users WHERE username ='{self.__username}' AND hash ='{password}'").fetchall())
        if userid == "[(1,)]":  # Check if there are any results that match both hash and username
            self.__userid = userid
            return self.__userid
        else:
            return False

    def loggedin(self) -> bool:
        """
        Returns the state of the authenticated flag so that other functions and classes can see if a user is
        logged in
        @return: True if the user is logged in, False otherwise"""
        return self.__authenticated

    def __validPassword(self) -> bool:
        """
        Uses regex statements to check if the password is of suitable strength and meets all the requirements
        @return: True if the password meets requirements, False otherwise
        """
        return fullmatch(r"/(?=.*\d.*)(?=.*[a-zA-Z].*).{8,}/gm", self.__password) is None
        # At least one digit, one lowercase and one uppercase letter. At least 8 characters.

    def register(self) -> bool:
        """
        Register the user in the database
        @return: True
        """
        self.__username = input("\nEnter a username to register: ")
        usernamecheck = str(
            self.__c.execute(f"SELECT COUNT(*) FROM users WHERE username='{self.__username}'").fetchall())
        while usernamecheck == "[(1,)]":  # Uses the sqlite3 string literal for "Results exist" to verify
            print("Username in use. Please pick another")
            self.__username = input("Enter a different username to register: ")
            usernamecheck = str(
                self.__c.execute(f"SELECT COUNT(*) FROM users WHERE username='{self.__username}'").fetchall())

        self.__password = getpass.getpass("Enter the password you want to use for this account: ")
        while not self.__validPassword():  # Check if the password meets every requirement
            self.__password = getpass.getpass(
                "Please enter a different password, Check it meets all the requirements (8 characters, at least one "
                "uppercase letter, lowercase letter and number must be present): ")

        pass_hash = sha256(
            self.__password.encode()).hexdigest()
        # human and processing friendly string version of password pass_hash in hexadecimal
        self.__c.execute(f'''INSERT INTO users(username, hash) VALUES(?,?)''',
                         (self.__username, pass_hash))
        # No error checking is needed here because of the two loops earlier preventing database errors due to
        # duplication
        self.__conn.commit()
        return True  # verify function ran correctly

    def update_password(self):
        self.__password = getpass.getpass("Enter the password you want to use for this account: ")
        while not self.__validPassword():  # Check if the password meets every requirement
            self.__password = getpass.getpass(
                "Please enter a different password, Check it meets all the requirements (8 characters, at least one "
                "uppercase letter, lowercase letter and number must be present): ")

        pass_hash = sha256(
            self.__password.encode()).hexdigest()
        # human and processing friendly string version of password pass_hash in hexadecimal
        self.__c.execute(f"""UPDATE users SET hash={pass_hash} WHERE userid='{self.getuserid()}'""")
        self.__conn.commit()

    def delete_user(self):
        self.__c.execute(f"""DELETE FROM users WHERE userid='{self.getuserid()}'""")
        self.__conn.commit()

    def getuserid(self) -> int:
        """
        Returns the userid of the currently logged-in user, or None if there isn't one
        @return: userid
        """
        return self.__userid
        # Userid is technically not private information and could in theory be worked out, specifically for a small
        # number of users over a short period of time.
        # however: having userid set tp private means we can set
        # an authenticated flag if hash name and id all agree

    def __resetDatabase(self) -> bool:
        """
        Used to reset the database for testing
        @return: True to indicate a successful run
        """
        del_users = f'''DELETE FROM users'''
        del_challenges = f'''DELETE FROM challenges'''
        del_highscore = f'''DELETE FROM highscores'''
        self.__c.execute(del_users)
        self.__c.execute(del_challenges)
        self.__c.execute(del_highscore)
        self.__conn.commit()
        return True
