import APIfuncties as APIfunc
import sqlite3


def checking_station(stationToCheck):
    'Checks if the db contains the value of stationToCheck'

    # connect to the database
    db = sqlite3.connect('reisplanner.db')

    # get a cursor object
    cursor = db.cursor()

    # Check if stationToCheck exists in the db 'stations' and returns a boolean of existence
    try:
        cursor.execute('''SELECT * FROM stations WHERE naamKort = ? OR naamMiddel = ? OR naamLang = ?''', (stationToCheck.lower(), stationToCheck.lower(), stationToCheck.lower()))
        return bool(cursor.fetchone())
    except:
        return False


def updating_stations_db():
    'Updates the database with all the stations that are available'
    'Writes it to reisplanner.db with TABLE stations'

    # call the API and save it to 'apiResponse'
    apiResponse = APIfunc.stationLijst_api()

    # connect to the database
    db = sqlite3.connect('reisplanner.db')

    # get a cursor object
    cursor = db.cursor()

    # drops table stations if table exists
    try:
        cursor.execute('''DROP TABLE stations''')
        db.commit()
        print("table dropped")
    except:
        # When the table does not exists
        print("There is no table to be dropped")

    # create a new table if it not already exists and commit it to the db
    cursor.execute('''CREATE TABLE IF NOT EXISTS stations(id INTEGER PRIMARY KEY, code TEXT unique, type TEXT, naamKort TEXT,
                      naamMiddel TEXT, naamLang TEXT, land TEXT)''')
    db.commit()

    # iterate and insert all needed values in the db
    for row in apiResponse["Stations"]["Station"]:
        cursor.execute('''INSERT INTO stations(code, type, naamKort, naamMiddel, naamLang, land)
                          VALUES (?,?,?,?,?,?)''', (row["Code"], row["Type"], row["Namen"]["Kort"].lower(), row["Namen"]["Middel"].lower(), row["Namen"]["Lang"].lower(), row["Land"]))
        db.commit()

    # closing the db
    db.close()


# in progress
def reismogelijkheden_to_db(apiResponse):
    'Writes all the reismogelijkheden to the database'
    'Writes it to reisplanner.db with TABLE reisinfo and reismogelijkheden'

    # connect to the database
    db = sqlite3.connect('reisplanner.db')

    # get a cursor object
    cursor = db.cursor()

    # drops TABLE reisinfo if table exists
    try:
        cursor.execute('''DROP TABLE reismogelijkheden''')
        db.commit()
        print("table dropped")
    except:
        # When the table does not exists
        print("There is no table to be dropped")

    # create a new TABLE reisinfo if it not already exists, with all the reizen available, and commit it to the db
    cursor.execute(
        '''CREATE TABLE IF NOT EXISTS reismogelijkheden(id INTEGER PRIMARY KEY, ritnummer TEXT, aantaloverstappen INTEGER, reistijd TEXT, vertrektijd TEXT, aankomsttijd TEXT, vertrekspoor TEXT, aankomstspoor TEXT, status TEXT)''')
    db.commit()

    try:
        # Try to write everything to the database

        # iterate over the XMLresponse, select the wanted values and insert it into the database
        for row in apiResponse["ReisMogelijkheden"]["ReisMogelijkheid"]:
            try:
                # When there isn't a train transfer involved
                cursor.execute('''INSERT INTO reismogelijkheden(ritnummer, aantaloverstappen, reistijd, vertrektijd, aankomsttijd, vertrekspoor, aankomstspoor, status) VALUES (?,?,?,?,?,?,?,?)''',
                            (row["ReisDeel"]["RitNummer"], row["AantalOverstappen"], row["ActueleReisTijd"], row["ActueleVertrekTijd"], row["ActueleAankomstTijd"], row["ReisDeel"]["ReisStop"][0]["Spoor"]["#text"], row["ReisDeel"]["ReisStop"][-1]["Spoor"]["#text"], row["Status"]))
            except:
                # When there is 1 or more transfers to another train
                try:
                    # When "ReisDeel" returns as a list
                    cursor.execute('''INSERT INTO reismogelijkheden(ritnummer, aantaloverstappen, reistijd, vertrektijd, aankomsttijd, vertrekspoor, aankomstspoor, status) VALUES (?,?,?,?,?,?,?,?)''',
                                (row["ReisDeel"][0]["RitNummer"], row["AantalOverstappen"], row["ActueleReisTijd"], row["ActueleVertrekTijd"], row["ActueleAankomstTijd"],
                                 row["ReisDeel"][0]["ReisStop"][0]["Spoor"]["#text"], row["ReisDeel"][-1]["ReisStop"][-1]["Spoor"]["#text"], row["Status"]))
                except:
                    # When "ReisDeel"doesn't returns as a list
                    cursor.execute('''INSERT INTO reismogelijkheden(ritnummer, aantaloverstappen, reistijd, vertrektijd, aankomsttijd, vertrekspoor, aankomstspoor, status) VALUES (?,?,?,?,?,?,?,?)''',
                                (row["ReisDeel"][0]["RitNummer"], row["AantalOverstappen"], row["ActueleReisTijd"], row["ActueleVertrekTijd"], row["ActueleAankomstTijd"], "BUS", row["ReisDeel"][-1]["ReisStop"][-1]["Spoor"]["#text"], row["Status"]))
    except Exception as e:
        # When there happens something unexpected
        print("Something has gone wrong:\n{0}".format(e))

    # commit it to the db
    db.commit()

    # closing the db
    db.close()


def storingen_to_db(StationToQuery):
    'Updates the database with all the actual storingen'
    'Writes it to reisplanner.db with TABLE storingen'

    # call the API and save it to 'apiResponse'
    apiResponse = APIfunc.storingen_api(StationToQuery)

    # connect to the database
    db = sqlite3.connect('reisplanner.db')

    # get a cursor object
    cursor = db.cursor()

    # drops table storingen if table exists
    try:
        cursor.execute('''DROP TABLE storingen''')
        db.commit()
        print("table dropped")
    except:
        # When the table does not exists
        print("There is no table to be dropped")

    # create a new table if it not already exists and commit it to the db
    cursor.execute('''CREATE TABLE IF NOT EXISTS storingen(id INTEGER PRIMARY KEY, traject TEXT, periode TEXT, reden TEXT, advies TEXT, bericht TEXT )''')
    db.commit()

    # iterate and insert all needed values in the db
    for row in apiResponse["Storingen"]["Gepland"]["Storing"]:
        try:
            # if reden and/or advies don't exist print NULL in their place
            cursor.execute('''INSERT INTO storingen(traject, periode, reden, advies, bericht)
                                VALUES (?,?,?,?,?)''', (row["Traject"], row["Periode"], row["Reden"], row["Advies"], row["Bericht"]))
        except:
            cursor.execute('''INSERT INTO storingen(traject, periode, reden, advies, bericht)
                                VALUES (?,?,NULL ,NULL ,?)''', (row["Traject"], row["Periode"], row["Bericht"]))
    db.commit()

    # closing the db
    db.close()


def reading_current_station():
    'Open huidigstation.txt and return the station of installment'

    try:
        # try to open the file
        with open('huidigstation.txt') as file:
            content = file.read()
        return content
    except:
        # when the file cannot be opened
        print("The file cannot be read")


def updating_current_station():
    'updates huidigstation.txt with the station of installment'

    while True:
        currentStation = str(input("What is the station of installment: "))
        # check if currentStation exists
        if checking_station(currentStation):
            break
    try:
        # open the file and write the current station in it
        with open('huidigstation.txt', 'w') as file:
            file.write(currentStation)
        print("Het huidige station is ingesteld als: {0}".format(currentStation))
    except:
        print("The file cannot be written")