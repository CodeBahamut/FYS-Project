import mysql.connector

database = mysql.connector.connect(
    host="oege.ie.hva.nl",
    user="keladab",
    password="ariUD31oXoqVdy",
    database="zkeladab"
)
def main():

# hier laat je met cursor.execute zien wat je in je database wilt zetten en welke values het heeft
    cursor = database.cursor()
    cursor.execute("INSERT INTO`Fys` (`name`, `score`) "
               "VALUES('bart', '5' );")

    database.commit()

# hiermee laat je zien wat je wilt hebben uit je database
    cursor.execute("SELECT`name`, `score` FROM`Fys`")

# hiermee pak je alles uit naam en score 
    result = cursor.fetchall()

    for row in result:
        print("Name player: " + row[0] + ", Score: " + str (row[1]))

if __name__== "__main__":main()
