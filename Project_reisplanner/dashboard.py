from reisFuncties import *
import datafuncties as dataFunc
from tkinter import *
import sqlite3
import APIfuncties as APIfunc

# update de stations in de database
dataFunc.updating_stations_db()


def returnToDashboard():
    # hoofdframe (Plan hier uw reis), zoekbalk en de reisadviezen
    frameHeader2 = Frame(master=frameHeader,
                         width=1050,
                         height=600,
                         background="white")
    frameHeader2.place(x=0, y=90)

    # subframe waar alles komt te staan (Plan hier uw reis), zoekbalk en de reisadviezen
    subFrameHeader = Frame(master=frameHeader2,
                           width=940,
                           height=550,
                           background="white")
    subFrameHeader.place(x=54, y=25)

    # welkomsttekst
    hoofLabelText = Label(master=subFrameHeader,
                          text='Welkom bij NS',
                          background="white",
                          foreground='#003067',
                          font=('Helvetica', 24),
                          height=2)
    hoofLabelText.place(x=0, y=0)

    # subtekst welkom
    subMainText = Label(master=subFrameHeader,
                        text='Kies een van de drie onderstaande opties',
                        background="white",
                        foreground='#003067',
                        font=('Helvetica', 17),
                        height=1)
    subMainText.place(x=0, y=65)

    # optie container
    mainFrameOptions = Frame(master=subFrameHeader, background="white")

    # optie 1
    optionOne = Frame(master=mainFrameOptions, background='white', width=270, height=320, bd=2, relief=SUNKEN,
                      bg="#003067")

    reisPlannenKnop = Button(optionOne, text="Reis plannen", padx=40, pady=140, font=('Helvetica', 20), foreground='white', background='#054187', command=openReisPlanner)
    reisPlannenKnop.pack(expand=True, fill='both')

    optionOne.pack(side=LEFT, expand=True, fill='both')

    # optie 2
    optionTwo = Frame(master=mainFrameOptions, background='white', width=270, height=320, bd=2, relief=SUNKEN,
                      bg="#003067")

    reistijdenKnop = Button(optionTwo, text="Actuele reistijden", padx=22, font=('Helvetica', 20), foreground='white',
                            background='#054187', command=actuelereisTijden)
    reistijdenKnop.pack(expand=True, fill='both')

    optionTwo.pack(side=LEFT, padx=(55, 0), expand=True, fill='both')

    # optie 3
    optionThree = Frame(master=mainFrameOptions, background='white', width=270, height=320, bd=2, relief=SUNKEN,
                        bg="#003067")

    storingenKnop = Button(optionThree, text="Actuele storingen", padx=15, font=('Helvetica', 20), foreground='white',
                           background='#054187', command=open_storingen)
    storingenKnop.pack(expand=True, fill='both')

    optionThree.pack(side=LEFT, padx=(55, 0), expand=True, fill='both')

    mainFrameOptions.pack(padx=(5, 0), pady=(150, 0))

def openReisPlanner():


    def planAndDraw():
        'takes the stations and draws the reismogelijkheden'
        travelList = []  # list for storing all the reismogelijkheden
        beginStation = station1.get()  # getting the begin station
        eindStation = station2.get()  # getting the end station

        # checking if stations exists
        if dataFunc.checking_station(beginStation):
            if dataFunc.checking_station(eindStation):
                response = reisPlannen(beginStation, eindStation)
            else:
                return
        else:
            return

        # loops over every reisMogelijkheid and writes it to its own class
        for index in response["ReisMogelijkheden"]["ReisMogelijkheid"]:
            travelList.append(ReisInfo(beginStation, eindStation, index["GeplandeVertrekTijd"][11:16],
                                       index["GeplandeAankomstTijd"][11:16], index["AantalOverstappen"],
                                       index["GeplandeReisTijd"]))
        # loops over every object and print its own frame with info
        for reis in travelList[0:5]:
            reis.writeInfo(reisAdviezen1)

    # hoofdframe(Plan hier uw reis), zoekbalk en de reisadviezen
    frameHeader2 = Frame(master=frameHeader,
                         width=1050,
                         height=600,
                         background="white")
    frameHeader2.place(x=0, y=90)

    # subframe waar alles komt te staan (Plan hier uw reis), zoekbalk en de reisadviezen
    subFrameHeader = Frame(master=frameHeader2,
                           width=940,
                           height=550,
                           background="white")
    subFrameHeader.place(x=54, y=25)

    # Plan hier uw reis
    text = Label(master=subFrameHeader,
                 text='Plan hier uw reis',
                 background="white",
                 foreground='#003067',
                 font=('Helvetica', 23),
                 height=2)
    text.place(x=0, y=0)

    # hoofdframe voor reisadviezen en ernaast
    reisAdviezen = Frame(master=subFrameHeader,
                         width=940,
                         height=400,
                         background="white")
    reisAdviezen.place(x=0, y=145)

    # frame voor waar de reisadviezen komen te staan
    reisAdviezen1 = Frame(master=reisAdviezen,
                          height=400,
                          background="white")
    reisAdviezen1.place(x=0)

    # begin en eindstation invullen
    invoerFrame = Tkint.Frame(master=subFrameHeader)
    invoerFrame.place(width=940, x=0, y=80)

    # symbol >
    symbol = Label(subFrameHeader, text='>',
                   foreground='#003067',
                   font=('Helvetica', 19))
    symbol.place(x=420, y=90)

    # knop voor het activeren van de zoekknop
    zoekButton = Tkint.Button(master=invoerFrame,
                              text="Plannen",
                              command=planAndDraw)
    zoekButton.pack(padx=10, pady=5, side="right")

    # beginstation
    station1 = Tkint.Entry(master=invoerFrame, width=53)
    # eindstation
    station2 = Tkint.Entry(master=invoerFrame, width=53)

    station1.pack(padx=50, pady=17, side="left")
    station2.pack(padx=50, pady=17, side="right")


def actuelereisTijden():

    def actuele_vertrektijden():
        'takes a station, calls to the API and returns the response'
        'The response will be all the departing trains of the station with time'

        'asks for station and outputs all the leaving trains on time and destination'
        queryStation = station1.get()
        if dataFunc.checking_station(queryStation):
            vertrekXML = APIfunc.actuele_vertrektijden_api(queryStation)
        else:
            print("This station is non-existent")
            return

        # Iterate over the data and print the needed information, executes max. 6 rows
        for vertrek in vertrekXML['ActueleVertrekTijden']['VertrekkendeTrein'][0:6]:
            eindBestemming = vertrek['EindBestemming']
            vertrekTijd = vertrek['VertrekTijd'][11:16]
            vertrekSpoor = vertrek["VertrekSpoor"]["#text"]
            ritNummer = vertrek["RitNummer"]

            # writes the vertrekTijd en aankomstTijd to the frame
            dateTime = Frame(master=actuelevertrektijdenFrame, background="white", borderwidth=1, relief="solid")

            uitvoer = Label(master=dateTime, background='white', width=50, pady=10, foreground='#003067',
                            font=('Helvetica', 12), text='{0} -> {1} -> Spoor: {2} -> ritnummer: {3}'.format(vertrekTijd, eindBestemming, vertrekSpoor, ritNummer))
            uitvoer.pack(side=LEFT)

            dateTime.pack(pady=(20, 0))

    # hoofdframe (Plan hier uw reis), zoekbalk en de reisadviezen
    frameHeader2 = Frame(master=frameHeader,
                         width=1050,
                         height=600,
                         background="white")
    frameHeader2.place(x=0, y=90)

    # subframe waar alles komt te staan (Plan hier uw reis), zoekbalk en de reisadviezen
    subFrameHeader = Frame(master=frameHeader2,
                           width=940,
                           height=550,
                           background="white")
    subFrameHeader.place(x=54, y=25)

    # welkomsttekst
    hoofLabelText = Label(master=subFrameHeader,
                          text='Actuele vertrektijden',
                          background="white",
                          foreground='#003067',
                          font=('Helvetica', 23),
                          height=2)
    hoofLabelText.place(x=0, y=0)

    # Contains input station and search button
    invoerFrame = Tkint.Frame(master=subFrameHeader, background='white')

    # Search button that executes actuele_vertrektijden_api
    zoekButton = Tkint.Button(master=invoerFrame, text="Zoek", command=actuele_vertrektijden)
    zoekButton.pack(padx=10, pady=5, side=RIGHT)

    # beginstation
    station1 = Tkint.Entry(master=invoerFrame)
    station1.pack(padx=10, pady=5)

    invoerFrame.pack(side=TOP)
    invoerFrame.place(y=80)

    # Frame that contains actuele reistijden container
    mainFrameOptions = Frame(master=subFrameHeader)

    # Container that contains alle the actuele reistijden in frames.
    actuelevertrektijdenFrame = Frame(master=mainFrameOptions, background='white', width=450, height=420)
    actuelevertrektijdenFrame.pack(side=LEFT)

    mainFrameOptions.pack(padx=(5, 0), pady=(150, 0))


def open_storingen():
    'Opens the frame for all the storingen'

    def calling_storingen():
        'takes a station, calls to the API and returns the response'
        'The response will be all the storingen involved with the current station'

        'asks for station and outputs all the leaving trains on time and destination'
        queryStation = station1.get()
        if dataFunc.checking_station(queryStation):
            dataFunc.storingen_to_db(queryStation)
        else:
            print("This station is non-existent")
            return

        # connect to database
        db = sqlite3.connect('reisplanner.db')

        # get a cursor object
        cursor = db.cursor()

        # select the desired info
        cursor.execute('''SELECT traject, periode, bericht FROM storingen''')
        all_rows = cursor.fetchall()

        # Iterate over the data and print the needed information, executes max. 6 rows
        for storing in all_rows[0:6]:
            treinTraject = storing[0]
            periodeDuur = storing[1]

            # writes the vertrekTijd en aankomstTijd to the frame
            storingFrame = Frame(master=storingenFrame, background="white", borderwidth=1, relief="solid")

            uitvoer1 = Label(master=storingFrame, background='white', width=60, pady=5, foreground='#003067',
                            font=('Helvetica', 12), text='Traject: {0}'.format(treinTraject))
            uitvoer1.pack(side=TOP)

            uitvoer2 = Label(master=storingFrame, background='white', width=60, pady=5, foreground='#003067',
                             font=('Helvetica', 12), text='periode: {0}'.format(periodeDuur))
            uitvoer2.pack(side=BOTTOM)

            storingFrame.pack(pady=(20, 0))

    # hoofdframe (Plan hier uw reis), zoekbalk en de reisadviezen
    frameHeader2 = Frame(master=frameHeader,
                         width=1050,
                         height=600,
                         background="white")
    frameHeader2.place(x=0, y=90)

    # subframe waar alles komt te staan (Plan hier uw reis), zoekbalk en de reisadviezen
    subFrameHeader = Frame(master=frameHeader2,
                           width=940,
                           height=550,
                           background="white")
    subFrameHeader.place(x=54, y=25)

    # welkomsttekst
    hoofLabelText = Label(master=subFrameHeader,
                          text='Actuele storingen',
                          background="white",
                          foreground='#003067',
                          font=('Helvetica', 23),
                          height=2)
    hoofLabelText.place(x=0, y=0)

    # Contains input station and search button
    invoerFrame = Tkint.Frame(master=subFrameHeader, background='white')  # row for inserting stations

    # Search button that executes actuele_vertrektijden_api
    zoekButton = Tkint.Button(master=invoerFrame, text="Zoek", command=calling_storingen)
    zoekButton.pack(padx=10, pady=5, side=RIGHT)

    # beginstation
    station1 = Tkint.Entry(master=invoerFrame)
    station1.pack(padx=10, pady=5)

    invoerFrame.pack(side=TOP)
    invoerFrame.place(y=80)

    # Frame that contains actuele reistijden container
    mainFrameOptions = Frame(master=subFrameHeader)

    # Container that contains alle the actuele reistijden in frames.
    storingenFrame = Frame(master=mainFrameOptions, background='white', width=450, height=420)
    storingenFrame.pack(side=LEFT)

    mainFrameOptions.pack(padx=(5, 0), pady=(150, 0))


# Drawing the Main GUI
root = Tk()
root.title('Nederlandse Spoorwegen')  # titel venster
root.config(width=1200, height=750)  # formaat venster
root.config(background="#FFC917")  # gele achtergrond van ns.nl

# hoofdframe
frameHeader = Frame(master=root,
                    width=1050,
                    height=690,
                    background="#FFC917")
frameHeader.place(x=70, y=10)

# frame voor logo en tekst
frameHeader1 = Frame(master=frameHeader,
                     width=1050,
                     height=90,
                     background="#FFC917")
frameHeader1.place(x=0)

# NS logo
imgpath = 'logo.png'
img = PhotoImage(file=imgpath)
img = img.zoom(3)
img = img.subsample(35)
panel = Label(frameHeader1,
              image=img,
              background="#FFC917")
panel.place(x=0, y=20)

# Reisplanner
logoText = Label(master=frameHeader1,
                 text='Nederlandse Spoorwegen',
                 foreground='#003067',
                 background="#FFC917",
                 font=('Helvetica', 16, 'bold'),
                 width=22,
                 height=3)
logoText.place(x=110, y=6)

returnButton = Button(frameHeader1, text="Terug",font=('Helvetica', 17), bd=2, relief=FLAT, highlightbackground='#003067', bg='#054187', fg='white', command=returnToDashboard)
returnButton.place(x=970, y=18)

# hoofdframe(Plan hier uw reis), zoekbalk en de reisadviezen
frameHeader2 = Frame(master=frameHeader,
                     width=1050,
                     height=600,
                     background="white")
frameHeader2.place(x=0, y=90)

# subframe waar alles komt te staan (Plan hier uw reis), zoekbalk en de reisadviezen
subFrameHeader = Frame(master=frameHeader2,
                       width=940,
                       height=550,
                       background="white")
subFrameHeader.place(x=54, y=25)

# welkomsttekst
hoofLabelText = Label(master=subFrameHeader,
             text='Welkom bij NS',
             background="white",
             foreground='#003067',
             font=('Helvetica', 24),
             height=2)
hoofLabelText.place(x=0, y=0)

# subtekst welkom
subMainText = Label(master=subFrameHeader,
             text='Kies een van de drie onderstaande opties',
             background="white",
             foreground='#003067',
             font=('Helvetica', 17),
             height=1)
subMainText.place(x=0, y=65)


# optie container
mainFrameOptions = Frame(master=subFrameHeader, background="white")


# optie 1
optionOne = Frame(master=mainFrameOptions, background='white', width=270, height=320, bd=2, relief=SUNKEN, bg="#003067")


reisPlannenKnop = Button(optionOne, text="Reis plannen", padx=40, pady=140, font=('Helvetica', 20), foreground='white', background='#054187', command=openReisPlanner)
reisPlannenKnop.pack(expand=True, fill='both')

optionOne.pack(side=LEFT, expand=True, fill='both')


# optie 2
optionTwo = Frame(master=mainFrameOptions, background='white', width=270, height=320, bd=2, relief=SUNKEN, bg="#003067")

reistijdenKnop = Button(optionTwo, text="Actuele reistijden", padx=22, font=('Helvetica', 20), foreground='white', background='#054187', command=actuelereisTijden)
reistijdenKnop.pack(expand=True, fill='both')

optionTwo.pack(side=LEFT, padx=(55, 0), expand=True, fill='both')


# optie 3
optionThree = Frame(master=mainFrameOptions, background='white', width=270, height=320, bd=2, relief=SUNKEN, bg="#003067")

storingenKnop = Button(optionThree, text="Actuele storingen", padx=15, font=('Helvetica', 20), foreground='white', background='#054187', command=open_storingen)
storingenKnop.pack(expand=True, fill='both')

optionThree.pack(side=LEFT, padx=(55, 0), expand=True, fill='both')

mainFrameOptions.pack(padx=(5, 0),pady=(150, 0))


root.mainloop()
