from os import truncate
from collections import OrderedDict
import sqlite3
import pytz
from datetime import datetime


class DB:

    validName = ['Tun', 'Ice', 'Fain', 'Pong', 'Palm', 'JJ', 'Palmcm']

    def __init__(self, dbPath, season, timezone):
        self.db = sqlite3.connect(dbPath)
        self.timezone = pytz.timezone(timezone)
        self.season = int(season)
        self.initializeDatabase()

    def initializeDatabase(self):
        try:
            cur = self.db.cursor()
            cur.execute(
                f"""CREATE TABLE IF NOT EXISTS PalmCounter_{str(self.season)} (
                    id integer PRIMARY KEY,
                    counter_owner_name text NOT NULL,
                    datetime datetime NOT NULL
                );""")

            self.db.commit()
        except sqlite3.Error as err:
            print(
                f"[{self.currentTime()}] [Database Error] Error Initialize DB: {err}")

    def isValidSeason(self, season):
        try:
            season = str(int(season))
            cur = self.db.cursor()
            cur.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name=?", (
                f"PalmCounter_{season}",
            ))
            return False if cur.fetchone() == None else True
        except:
            return False

    def currentTime(self):
        return datetime.now().astimezone(self.timezone)

    def lastCounter(self):
        cur = self.db.cursor()
        cur.execute(
            f'SELECT * FROM PalmCounter_{str(self.season)} WHERE datetime = (SELECT MAX(datetime) From PalmCounter_{str(self.season)});')
        return cur.fetchone()

    def listCounter(self):
        cur = self.db.cursor()
        cur.execute(
            f'SELECT * FROM PalmCounter_{str(self.season)} ORDER BY datetime DESC')
        return cur.fetchall()

    def countName(self, name, season):
        if not self.isValidSeason(season):
            return 0
        cur = self.db.cursor()
        cur.execute(f'SELECT count(*) FROM PalmCounter_{str(season)} WHERE counter_owner_name=?', (
            name,
        ))
        return cur.fetchone()[0]

    def isCountToday(self):
        lastCounter = self.lastCounter()
        if (lastCounter == None):
            return False
        elif self.currentTime().strftime('%Y-%m-%d') == datetime.fromisoformat(lastCounter[2]).strftime('%Y-%m-%d'):
            return lastCounter[1]
        else:
            return False

    def addCounter(self, name):
        name = [e for e in self.validName if name.lower() == e.lower()]
        if (len(name) == 0):
            return "Invalid name"
        name = name[0]

        todayName = self.isCountToday()
        if (todayName == False):
            cur = self.db.cursor()
            cur.execute(f'INSERT INTO PalmCounter_{str(self.season)} (counter_owner_name, datetime) VALUES (?, ?)', (
                name,
                self.currentTime(),
            ))
            self.db.commit()
            print(
                f"[{self.currentTime()}] [Database Log] Add {name} To Database Successfully")
            return name
        else:
            return "Duplicated date " + todayName

    def getScore(self, season):
        isValidSeason = self.isValidSeason(season)
        data = OrderedDict()
        dataList = []

        for name in self.validName:
            dataList.append(( (self.countName(name,season) if isValidSeason else 0),name ))
        dataList.sort(reverse=True)
        for (i,j) in dataList:
            data[j]=i

        
        return data

    def listScore(self, season):
        data = self.getScore(season)
        output = []
        for i, j in data.items():
            if j != 0:
                output.append([j, i])

        if len(output) == 0:
            return "Empty"

        output.sort(reverse=True)
        output = [f"{j} {str(i)}" for [i, j] in output]
        return '\n'.join(output)

    def getLastScore(self):
        data = self.lastCounter()
        return {'name': data[1], 'datetime': data[2].split(".")[0]} if data != None else None
