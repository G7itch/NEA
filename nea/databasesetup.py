import sqlite3

class Setup(object):

    def __init__(self):
        self.__conn = sqlite3.connect("file:master.db?mode=rw", uri=True)
        self.__conn.execute("PRAGMA foreign_keys = 1")
        self.__c = self.__conn.cursor()
        self.__c.execute('''CREATE TABLE highscores (userid INTEGER, score INTEGER, FOREIGN KEY (userid) REFERENCES users (userid) )''')
        self.__c.execute('''CREATE TABLE challenges (challengeid INTEGER PRIMARY KEY, challengedesc TEXT, difficulty REAL, reward REAL)''')
        self.__conn.commit()
        with open("achievements.json", "w") as achievements: #create and close file
            pass
        self.__populateDB()
        self.__conn.close()

    def __populateDB(self):
        challenges = {
            0 : ["Entangle two particles", 1.0, 10],
            1 : ["Use a hadamard gate for the first time",0.5,5],
            2 : ["Teleport a particle",2.5,50],
        }
        for i in range(len(challenges)):
            self.__c.execute(f'''INSERT INTO challenges(challengedesc,difficulty,reward) VALUES(?,?,?)''',(challenges[i][0],challenges[i][1],challenges[i][2]))
            self.__conn.commit()
