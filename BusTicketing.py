from sys import exit
from time import sleep

import mysql.connector
from mysql.connector import Error

class Database:
    _host = "localhost"
    _database = "db_ticketing"
    _user = "root"
    _password = "Familia,2007"

    def __init__(self):
        pass

    def CreateConnection (self):
        try:

            connection = mysql.connector.connect(host=self._host, database=self._database, user=self._user, password=self._password, auth_plugin='mysql_native_password')
            
            if connection.is_connected():
                return connection

        except Error as err:
            print("Error while connecting to MySQL: ", err)
            return False

    def DestroyConnection (self, cursor, connection):

        if (connection.is_connected()):
            cursor.close()
            connection.close()

class Bus:

    def __init__ (self, bus_ID, bus_TotalSeats, bus_AvailSeats = 0):
        if bus_ID != 0:
            self.SetID(bus_ID)

        self.SetTotalSeats(bus_TotalSeats)

        if (bus_AvailSeats != 0):
            self.SetAvailSeats(bus_AvailSeats)
        else:
            self.SetAvailSeats(bus_TotalSeats)

    def SetID(self, bus_ID):
        self.bus_ID = bus_ID
    
    def SetTotalSeats(self, bus_TotalSeats):
        self.bus_TotalSeats = bus_TotalSeats

    def SetAvailSeats(self, bus_AvailSeats):
        self.bus_AvailSeats = bus_AvailSeats
    
    def GetID(self):
        return self.bus_ID
    
    def GetTotalSeats(self):
        return self.bus_TotalSeats

    def GetAvailSeats(self):
        return self.bus_AvailSeats

    def GetOccupiedSeats(self):
        totalSeats = self.GetTotalSeats()
        availSeats = self.GetAvailSeats()
        
        return totalSeats - availSeats

class Bus_Admin:

    database = Database()
    bus = None

    def __init__ (self):
        pass

    def GetBusData(self, filterID = False):

        try:
            connection = self.database.CreateConnection()

            if connection != False:

                cursor = connection.cursor()

                if filterID == False:
                    cursor.execute("SELECT * FROM tbl_bus")
                    arrInitialData = cursor.fetchall()
                else:
                    cursor.execute(f"SELECT * FROM tbl_bus WHERE bus_ID = {filterID};")
                    arrInitialData = cursor.fetchall()[0]

                return arrInitialData

            else:
                exit()
        except Error as e:
            print('Error while fetching data: ', e)
            exit()
        finally:
            self.database.DestroyConnection(cursor, connection)

    def checkAvailSeatsInBus (self, selectedBus, availSeatsRequired, selling = True):
        isValid = False
       
        try:
            connection = self.database.CreateConnection()

            if connection != False:
                cursor = connection.cursor()

                cursor.execute(f"SELECT * FROM tbl_bus WHERE bus_ID = %s" % (selectedBus.GetID()))

                if selling:
                    availSeatsInBus = cursor.fetchall()[0][2]

                    if 0 < int(availSeatsRequired) <= availSeatsInBus:
                        isValid = True
                else:
                    occupiedSeats = cursor.fetchall()[0][1] - cursor.fetchall()[0][2]

                    if 0 < int(availSeatsRequired) <= occupiedSeats:
                        isValid = True 

                return isValid

        except Error as e:
            print(e)
            exit()
        finally:
            self.database.DestroyConnection(cursor, connection)

    def SetNewBus (self, newBus):
        try:
            connection = self.database.CreateConnection()
            if connection != False:
                cursor = connection.cursor()
                sql = "INSERT INTO tbl_bus (bus_TotalSeats, bus_AvailSeats) VALUES (%s, %s)"
                values = (newBus.GetTotalSeats(), newBus.GetAvailSeats())
                cursor.execute(sql,values)
                connection.commit()
            else:
                print("Error while connecting to database.")
        except Error as e:
            print('Error while saving data: ', e)
        finally:
            self.database.DestroyConnection(cursor, connection)

    def DeleteActivePassengers(self, arrPassengers, idBus):
        
        try:
            connection = self.database.CreateConnection()

            if connection != False:
                cursor = connection.cursor()

                condition = ""
                for (i, passenger) in enumerate(arrPassengers):
                        condition += f"(passenger_id = '{passenger.GetId()}' AND passenger_bus = {idBus}) OR "

                condition = condition[:-4]

                cursor.execute(f"DELETE FROM tbl_passenger WHERE {condition}")
                connection.commit()
        except Error as e:
            exit()
        finally:
            self.database.DestroyConnection(cursor, connection)

    def TicketingSelling(self, selectedBus, requestedTickets, arrPassengers):
        isValid = False
        availSeats = selectedBus.GetAvailSeats()

        if availSeats >= requestedTickets:
            availSeats -= requestedTickets
            selectedBus.SetAvailSeats(availSeats)
            
            self.__Db_updateBusStatus(selectedBus, arrPassengers)

            isValid = True

        return isValid

    def checkPassengerInBusById(self, strId):
        try:
            callback = False
            connection = self.database.CreateConnection()
            
            if connection != False:
                cursor = connection.cursor()
                cursor.execute(f"SELECT EXISTS(SELECT * FROM tbl_passenger WHERE passenger_id = '{strId}')")

                arrPassenger = cursor.fetchall()
                isInDatabase = arrPassenger[0][0]

                return isInDatabase

        except Error as e:
            print(e)
            exit()
        finally:
            self.database.DestroyConnection(cursor, connection)


    def TicketingRefunding (self, selectedBus, refundedTickets, arrPassengers):
        isValid = False
        totalSeats = selectedBus.GetTotalSeats()
        availSeats = selectedBus.GetAvailSeats()

        occupiedSeats = selectedBus.GetOccupiedSeats()

        if occupiedSeats >= refundedTickets:
            availSeats += refundedTickets
            selectedBus.SetAvailSeats(availSeats)

            self.DeleteActivePassengers(arrPassengers, selectedBus.GetID())
            self.__Db_updateBusStatus(selectedBus)

            isValid = True

        return isValid
    
    def __Db_updateBusStatus(self, selectedBus, arrPassengers = False):
        try:

            connection = self.database.CreateConnection()

            if connection != False:
                cursor = connection.cursor()

                if arrPassengers != False:
                    for (i, passenger) in enumerate(arrPassengers):
                        instPassenger = arrPassengers[i]
            
                        cursor.execute(f"INSERT INTO tbl_passenger (passenger_name, passenger_id, passenger_bus) VALUES ('{instPassenger.GetName()}', '{instPassenger.GetId()}', {selectedBus.GetID()});")
                        connection.commit()
                        
                    cursor.execute(f"UPDATE tbl_bus SET bus_AvailSeats = {selectedBus.GetAvailSeats()} WHERE (bus_ID = {selectedBus.GetID()});")
                    connection.commit()
                else: 
                    cursor.execute(f"UPDATE tbl_bus SET bus_AvailSeats = {selectedBus.GetAvailSeats()} WHERE (bus_ID = {selectedBus.GetID()});")
                    connection.commit()
            else:
                print("Database connection failed.")
                exit()

        except Error as e:
            print('Error while updating data: ', e)
        finally:
            self.database.DestroyConnection(cursor, connection)
    
    def GetPassengersDataFromBus(self, selectedBus):
        try:
            connection = self.database.CreateConnection()

            if connection != False:
                cursor = connection.cursor()
                cursor.execute(f"SELECT passenger_name, passenger_id FROM tbl_passenger WHERE passenger_bus = {selectedBus.GetID()}")
                
                arrPassengers = cursor.fetchall()

                return arrPassengers

            else:
                exit()

        except Error as e:
            print('Error while updating data: ', e)
        finally:
            self.database.DestroyConnection(cursor, connection)

    def GetStatusTable(self, selectedBus, output, ColoredStr):


        totalSeats      =   selectedBus.GetTotalSeats()
        availSeats      =   selectedBus.GetAvailSeats()
        occupiedSeats   =   selectedBus.GetOccupiedSeats()

        arrSummaryData = [totalSeats, availSeats, occupiedSeats]
        arrSummaryStrings = ['Total Tickets', 'Available Tickets', 'Sold Tickets']

        arrPassengers = self.GetPassengersDataFromBus(selectedBus)

        if output == "console":

            print("SELLING STATUS: \n")

            for intLoop in range(3):

                tab = "\t\t"
                if len(arrSummaryStrings[intLoop]) < 15:
                    tab += "\t"
                
                print(f"%s:{tab}%f" % (ColoredStr(arrSummaryStrings[intLoop],BColors.OKCYAN), arrSummaryData[intLoop]))

            print("\nPassengers: \n")

            for tlPassenger in arrPassengers:
                # print(f"%s\t\t%f" % (ColoredStr(tlPassenger[1], BColors.OKBLUE), tlPassenger[0]))
                print(f"{tlPassenger[0]}\t\tDNI/NIE: {tlPassenger[1]}")
        
class UI:

    def __init__(self):
        self.__helper = Helper()
        pass
    
    def Console_renderBusSelectionMenuOptions (self):
        print (self.__helper.ColoredStr("\nBUS SELECTION:\n\n", BColors.OKBLUE))

        print("1. Select a bus. ")
        print("2. Create new bus.")

        optBusMenu = input(StrControl.option)

        return optBusMenu

    def Console_renderMainMenu (self):
        print()
        print("----------------------------------------------")
        print(self.__helper.ColoredStr("MENU", BColors.OKBLUE))
        print("\n")
        print("1: Ticketing Selling")
        print("2: Ticketing Refunding")
        print("3: Selling Status")
        print("0: Exit")

        mainMenuOptValue = input(StrControl.option)

        return mainMenuOptValue



    def Console_renderBusTable (self, allBusData):

        print(self.__helper.ColoredStr("\n\nSELECT A BUS\n",BColors.OKBLUE))

        tpMenuHeader = (
            self.__helper.ColoredStr("Bus ID", BColors.OKGREEN), 
            self.__helper.ColoredStr("Total Seats", BColors.OKGREEN), 
            self.__helper.ColoredStr("Available Seats", BColors.OKGREEN)
        )
        
        print("%s\t\t%s\t\t%s" % tpMenuHeader)

        for tpBusInfo in allBusData:
            print(f"%s\t\t%s\t\t\t%s" % tpBusInfo)

        optIDBus = input("\nSelecciona el ID de un bus: ")

        return optIDBus

    def Console_renderPassengerDataRequest(self, intNumRequestedTickets):
        arrPassengers = []

        for passengerNumber in range(int(intNumRequestedTickets)):
            print(f"\nData from passenger #{str(passengerNumber + 1)}\n")
            passName = input("Nombre: ")
            passID = input("DNI / NIE: ")

            passenger = Passenger(passID, passName)
            arrPassengers.append(passenger)

        return arrPassengers
        
class BColors:

    def __init__(self):
        pass

    UNDERLINE = '\033[4m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    OKCYAN = '\033[96m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'

class StrControl:
    optOK = "Operation done successfully"
    reqError = "Error: There are not enough seats available."
    setSeatsError = "Invalid value"
    invalidOption = "Non-valid option."
    busCreated = "The new bus has been created successfully."
    option= "\nSelect an option: "
    outOfRange = "Value out of valid range."

class Helper: 
    def __init__ (self):
        pass
    
    def Check_int(self, strNumber, isZeroValid = False, limit = False, strError = None):
        try:
            isValid = False
            if strNumber[0] in ('-', '+'):
                strNumber = strNumber[1:]
            
            if strNumber.isdigit():
                if limit == False:
                    if isZeroValid:
                        if 0 <= int(strNumber):
                            isValid = True
                    else:
                        if 0 < int(strNumber):
                            isValid = True
                else:
                    if isZeroValid:
                        if 0 <= int(strNumber) <= limit:
                            isValid = True
                    else:
                        if 0 < int(strNumber) <= limit:
                            isValid = True
            if not isValid:
                if strError is None:
                    print(self.ColoredStr(StrControl.invalidOption, BColors.FAIL))
                else:
                    print(self.ColoredStr(strError, BColors.FAIL))
            return isValid
        except:
            return False

    def ColoredStr(self, string, color):
        return f"{color}{string}{BColors.ENDC}"

class Passenger:

    def __init__ (self, id, name = ""):
        self.SetName(name)
        self.SetId(id)

    def SetName(self, name):
        self.__name = name

    def SetId(self, id):
        self.__id = id

    def GetName(self):
        return self.__name

    def GetId(self):
        return self.__id


# Instance of bus admin class
instBusAdmin = Bus_Admin()

# Instance of UI
ui = UI()

# Instance of Helper
helper = Helper()

# BUS SELECTION MENU
isBusSelected = False
while not isBusSelected:

    isSelectBusOptValid = False
    while not isSelectBusOptValid:
        
        # Bus Selection Menu rendering 
        optBusMenu = ui.Console_renderBusSelectionMenuOptions()

        isSelectBusOptValid = True if helper.Check_int(optBusMenu, False, 2) else sleep(2)


    optBusMenu = int(optBusMenu)

    # Selection of an existent bus
    if optBusMenu == 1:

        # Get all bus data
        allBusData = instBusAdmin.GetBusData()

        isBusIDValid = False
        while not isBusIDValid:
            
            # Rendering of bus table 
            optIDBus = ui.Console_renderBusTable(allBusData)

            #! By order -> By id
            isBusIDValid = True if helper.Check_int(optIDBus, False, len(allBusData)) else sleep(2)

        # Get data from the selected bus
        (busID, busTotalSeats, busAvailSeats) = instBusAdmin.GetBusData(int(optIDBus))
        selectedBus = Bus(busID, busTotalSeats, busAvailSeats)

        #* Exit to Main Menu
        isBusSelected = True

    elif optBusMenu == 2:

        print(helper.ColoredStr("\n\nNEW BUS", BColors.OKBLUE))

        isNewTotalSeatsValid = False
        while not isNewTotalSeatsValid:

            newBusTotalSeats = input("\nIntroduce la cantidad de asientos del nuevo bus: ")

            print()

            # Is input valid?
            if helper.Check_int(newBusTotalSeats):

                # Create bus in database
                newBus = Bus(0, int(newBusTotalSeats))
                instBusAdmin.SetNewBus(newBus)

                print(helper.ColoredStr(StrControl.busCreated,BColors.OKCYAN))

                isNewTotalSeatsValid = True
                
            sleep(2)


# MAIN MENU
isExitSelected = False
while not isExitSelected:

    isMainMenuOptValid = False
    while not isMainMenuOptValid:

        # Main Menu Rendering
        mainMenuOptValue = ui.Console_renderMainMenu()

        # Is input valid?
        isMainMenuOptValid = True if helper.Check_int(mainMenuOptValue, True, 3) else sleep(2)

    print("\n\n")

    mainMCase = int(mainMenuOptValue)

    if mainMCase == 1:
        print(helper.ColoredStr("TICKETING SELLING: ", BColors.OKBLUE))

        isInputValid = False
        while not isInputValid:

            intNumRequestedTickets = input("\nEnter the number of tickets you need: ")

            # Is input valid?
            isInt = helper.Check_int(intNumRequestedTickets, False, False, StrControl.setSeatsError)
            if isInt:
                isAmountOfTicketsValid = instBusAdmin.checkAvailSeatsInBus(selectedBus, intNumRequestedTickets)
                isInputValid = True if isAmountOfTicketsValid else print(helper.ColoredStr(StrControl.outOfRange, BColors.FAIL))

            if not isInputValid:
                sleep(2)


        # Passenger data
        arrPassengers = ui.Console_renderPassengerDataRequest(intNumRequestedTickets)


        # Control Error: Boolean
        isRequestValid = instBusAdmin.TicketingSelling(selectedBus, int(intNumRequestedTickets), arrPassengers)

        arrOutput = [StrControl.optOK, BColors.OKCYAN] if isRequestValid else [StrControl.reqError, BColors.FAIL]

        # Output
        print(helper.ColoredStr(arrOutput[0], arrOutput[1]))

    elif mainMCase == 2:
        print(helper.ColoredStr("TICKETING REFUNDING: ", BColors.OKBLUE))

        # Loop Control Variable: Boolean
        isInputValid = False
        while not isInputValid:

            intNumRefundedTickets = input("\nEnter the number of tickets you need: ")

            # Is input valid?
            isInt = helper.Check_int(intNumRefundedTickets, False, False, StrControl.setSeatsError)
            if isInt:
                isAmountOfTicketsValid = instBusAdmin.checkAvailSeatsInBus(selectedBus, intNumRefundedTickets, False)
                isInputValid = True if isAmountOfTicketsValid else print(helper.ColoredStr(StrControl.outOfRange, BColors.FAIL))

            if not isInputValid:
                sleep(2)

        # Passenger data
        arrPassengers = []
        contLoop = 1

        while 0 < contLoop <= int(intNumRefundedTickets):
        # while passengerNumer in range(int(intNumRefundedTickets)):
            print(f"\nData from passenger #{str(contLoop)}")
            passID = input("DNI / NIE: ")

            isInDatabase = instBusAdmin.checkPassengerInBusById(passID)
            if (isInDatabase):
                passenger = Passenger(passID)
                arrPassengers.append(passenger)
                contLoop+=1
            else: 
                contLoop = 0
                print(helper.ColoredStr("The inserted value don't exist", BColors.FAIL))

        # Control Error: Boolean
        if contLoop != 0:
            isRequestValid = instBusAdmin.TicketingRefunding( selectedBus, int(intNumRefundedTickets), arrPassengers)
        else: 
            isRequestValid = False
        
        arrOutput = [StrControl.optOK, BColors.OKCYAN] if isRequestValid else [StrControl.reqError, BColors.FAIL]

        # Output
        print(helper.ColoredStr(arrOutput[0], arrOutput[1]))

    elif mainMCase == 3:

        # Render table of selected bus info
        instBusAdmin.GetStatusTable(selectedBus, 'console', helper.ColoredStr)
    
    else:

        # Exit
        print(helper.ColoredStr("Exiting...", BColors.WARNING))
        isExitSelected = True
        
    # Stop rendering until a key press.
    if mainMCase != 0:
         input("\n" + helper.ColoredStr("Press Enter to continue...", BColors.OKGREEN))
