import psycopg2

config = {
    "host": "79.174.89.27",
    "port":19957,
    "user": "bagdanmyh3",
    "password": "Wasd3!520@~!",
    "dbname": "bagdanmyh3"
}
def exitsSession(telegramidchat: int) -> bool:
    return len(getSession(telegramidchat=telegramidchat)) > 0

def getSession(telegramidchat: int) -> tuple:
    conn = psycopg2.connect(dbname=config["dbname"], user=config["user"], password=config["password"], host=config["host"], port=config["port"])
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM sessions WHERE telegramidchat={telegramidchat};")
    return cursor.fetchall()

def newSession(telegramidchat: int) -> None:
    conn = psycopg2.connect(dbname=config["dbname"], user=config["user"], password=config["password"], host=config["host"], port=config["port"])
    cursor = conn.cursor()
    cursor.execute(f"INSERT INTO sessions VALUES ({len(getAllSessions())}, {telegramidchat}, 1, 0);")
    conn.commit()

def updateSession(telegramidchat: int, nameColumnUpdate: str, newCaribla: str):
    conn = psycopg2.connect(dbname=config["dbname"], user=config["user"], password=config["password"], host=config["host"], port=config["port"])
    cursor = conn.cursor()
    cursor.execute(f"UPDATE sessions SET {nameColumnUpdate}={newCaribla} WHERE telegramidchat={telegramidchat}")
    conn.commit()
def getAllSessions():
    conn = psycopg2.connect(dbname=config["dbname"], user=config["user"], password=config["password"], host=config["host"], port=config["port"])
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM sessions WHERE 1=1")
    return cursor.fetchall()
# print(updateSession(1433304275, "differentcharacters", "3"))
print(getAllSessions())