import mysql.connector

database = mysql.connector.connect(
    host="oege.ie.hva.nl",
    user="keladab",
    password="ariUD31oXoqVdy",
    database="zkeladab"
)
def main():


    cursor = database.cursor()
    cursor.execute("INSERT INTO`Fys` (`name`, `score`) "
               "VALUES('bart', '5' );")

    database.commit()

if __name__== "__main__":main()
