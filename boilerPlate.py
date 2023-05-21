import subprocess as sp
import pymysql
import pymysql.cursors


def addUser():
    try:
        row = {}
        print("Enter new user details: ")
        row["Username"] = input("Username: ")
        row["Name"] = input("Name: ")
        row["Email_Address"] = input("Email Address: ")
        row["DOB"] = input("Date of Birth (YYYY-MM-DD): ")
        row["Default_Payment_Mode"] = input("Default Payment Mode: ")

        query = "INSERT INTO USERS VALUES('%s', '%s', '%s', '%s', '%s')" % (
            row["Username"], row["Name"], row["Email_Address"], row["DOB"], row["Default_Payment_Mode"]); 

        print(query)
        cur.execute(query)
        con.commit()

        print("Inserted Into Database")


    except Exception as e:
        con.rollback()
        print("Failed to insert into database")
        print(">>>>>>>>>>>>>", e)

    return


def rateDriver():
    try:
        driverid = int(input("Enter Driver ID: "))
        while 1:
            rating = float(input("Enter Rating (0-5): "))
            if rating >= 0 and rating <= 5:
                break
            print("Invalid rating")

        query = "SELECT Rating, No_of_Orders_Completed from DRIVERS WHERE Driver_ID = %d" % (driverid)

        try:
            print(query)
            cur.execute(query)
            con.commit()
        except Exception as f:
            con.rollback()
            print("Invalid Driver ID")
            print(">>>>>>>>>>>>>", f)
            return

        temp = cur.fetchall()
        my_temp=str(temp[0])
        newstr = ''.join((ch if ch in '0123456789.' else ' ') for ch in my_temp)
        listOfNumbers = [float(i) for i in newstr.split()]
        currrating=float(listOfNumbers[0])
        numorders=float(listOfNumbers[1])
        newrating = float(((currrating * numorders)+rating)/(numorders+1))
        query = '''UPDATE DRIVERS SET Rating = %f, No_of_Orders_Completed = %d 
            WHERE Driver_ID = %d''' % (newrating, numorders+1, driverid)
        
        print(query)
        cur.execute(query)
        con.commit()

        print("Updated Database")

    except Exception as e:
        con.rollback()
        print("Failed to update database")
        print(">>>>>>>>>>>>>", e)

    return


def unlikeRestaurant():
    try:
        print("Enter user details: ")
        username = input("Enter Username: ")
        id = int(input("Enter InstaMunchies_ID of restaurant or grocery store to be deleted: "))
        query = "DELETE FROM LIKES WHERE Username = '%s' AND InstaMunchies_ID = %d" % (username, id)

        print(query)
        cur.execute(query)
        con.commit()
        print("Deleted from Database")

    except Exception as e:
        con.rollback()
        print("Failed to delete from database")
        print(">>>>>>>>>>>>>", e)

    return


def ratingLessThan2():
    try:
        query = "SELECT Driver_ID, Name, Rating FROM DRIVERS WHERE Rating < 2"

        cur.execute(query)
        con.commit()

        drivers = cur.fetchall()
        print("DRIVERS")
        for x in drivers:
            print(x)

        query = "SELECT Name, InstaMunchies_ID, Rating FROM SERVICE_PROVIDERS WHERE Rating < 2"
        cur.execute(query)
        con.commit()

        sp = cur.fetchall()
        print("SERVICE PROVIDERS")
        for x in sp:
            print(x)

    except Exception as e:
        con.rollback()
        print("Failed to query database")
        print(">>>>>>>>>>>>>", e)

    return


def UPIPaymentsAmount():
    try:
        query = '''SELECT SUM(Total_Amount) FROM BILLS WHERE Mode_of_Payment = 'UPI' '''

        cur.execute(query)
        con.commit()

        sum = cur.fetchall()
        sum = str(sum[0])
        newstr = ''.join((ch if ch in '0123456789.' else ' ') for ch in sum)
        newstr = newstr.strip()

        print("Amount from all UPI payments = " + str(newstr))  

    except Exception as e:
        con.rollback()
        print("Failed to query database")
        print(">>>>>>>>>>>>>", e)
    
    return


def bestDriver():
    try:
        query = ('''SELECT Driver_ID, Name, Rating FROM DRIVERS WHERE Rating = (SELECT MAX(Rating) FROM DRIVERS)''')

        cur.execute(query)
        con.commit()

        driver = cur.fetchone()
        print("Driver with maximum rating: ")
        print(driver)
    
    except Exception as e:
        con.rollback()
        print("Failed to query database")
        print(">>>>>>>>>>>>>", e)

    return


def searchFood():
    try:
        name = input("Enter Food Name: ")
        query = "SELECT InstaMunchies_ID, Name FROM FOOD WHERE Name LIKE '%"+name+"%'"

        cur.execute(query)
        con.commit()

        foods = cur.fetchall()
        for x in foods:
            print(x)

    except Exception as e:
        con.rollback()
        print("Failed to query database")
        print(">>>>>>>>>>>>>", e)

    return


def jaysCandidates():
    try:
        query = '''SELECT COUNT(InstaMunchies_ID) FROM SERVICE_PROVIDERS'''

        cur.execute(query)
        con.commit()

        temp = cur.fetchone()
        newstr = ''.join((ch if ch in '0123456789.' else ' ') for ch in str(temp))

        query = '''SELECT Name, InstaMunchies_ID FROM SERVICE_PROVIDERS WHERE Open_Time IS NULL AND Close_Time IS NULL AND Rating > 4 
        ORDER BY Average_Prep_Time ASC LIMIT %d''' % (0.2*int(newstr))

        cur.execute(query)
        con.commit()

        sp = cur.fetchall()
        print("The service providers which qualify to be tasted by Jay are: ")
        for x in sp:
            print(x)

    except Exception as e:
        con.rollback()
        print("Failed to query database")
        print(">>>>>>>>>>>>>", e)

    return


def dispatch(ch):
    """
    Function that maps helper functions to option entered
    """

    if(ch == 1):
        addUser()
    elif(ch == 2):
        rateDriver()
    elif(ch == 3):
        unlikeRestaurant()
    elif(ch == 4):
        ratingLessThan2()
    elif(ch == 5):
        UPIPaymentsAmount()
    elif(ch == 6):
        bestDriver()
    elif(ch == 7):
        searchFood()
    elif(ch == 8):
        jaysCandidates()
    else:
        print("Error: Invalid Option")


# Global
while(1):
    tmp = sp.call('clear', shell=True)
    
    # Can be skipped if you want to hardcode username and password
    # username = input("Username: ")
    # password = input("Password: ")

    try:
        # Set db name accordingly which have been create by you
        # Set host to the server's address if you don't want to use local SQL server 
        con = pymysql.connect(host='localhost',
                              port=3306,
                              user='root',
                              password='Sriya_117',
                              db='InstaMunchies',
                              cursorclass=pymysql.cursors.DictCursor)
        tmp = sp.call('clear', shell=True)

        if(con.open):
            print("Connected")
        else:
            print("Failed to connect")

        tmp = input("Enter any key to CONTINUE>")

        with con.cursor() as cur:
            while(1):
                tmp = sp.call('clear', shell=True)
                # Here taking example of Employee Mini-world
                print("1.ADD_USER")  # Insert
                print("2.RATE_DRIVER")  # Update
                print("3.UNLIKE_RESTAURANT")  # Delete
                print("4.RATING_LESS_THAN_2")  # Select
                print("5.UPI_PAYMENTS_AMOUNT") # Project
                print("6.BEST_DRIVER") # Aggregate
                print("7.SEARCH_FOOD") # Search
                print("8.JAY'S_CANDIDATES") # Analysis
                print("9.LOG_OUT") # Logout
                ch = int(input("Enter choice> "))
                tmp = sp.call('clear', shell=True)
                if ch == 9:
                    exit()
                else:
                    dispatch(ch)
                    tmp = input("Enter any key to CONTINUE>")

    except Exception as e:
        tmp = sp.call('clear', shell=True)
        print(e)
        print("Connection Refused: Either username or password is incorrect or user doesn't have access to database")
        tmp = input("Enter any key to CONTINUE>")   