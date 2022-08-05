from asyncio.windows_events import NULL
import datetime
from distutils.log import error
import re
import logging
from tabulate import tabulate
from datetime import date
from datetime import datetime
import mysql.connector
import mySQLconfig as c

def main():
    account = []
    try:
        cnx = mysql.connector.connect(user="root", password="Travel@MySQL", host="localhost", database="project_1")
        cursor = cnx.cursor(buffered = True )
    except mysql.connector.Error as mce:
        print(mce.msg)
        return
    except Exception as e:
        print("ERROR: Exiting program")
        return
    account = []
    logging.basicConfig(filename="projectLog.log", level=logging.DEBUG, format='%(asctime)s :: %(message)s')
    #loadAccount(cursor,cnx)
    #updateAccount(cursor,cnx,[2,False])
    #addItem(cursor,cnx)
    #makePurchase(cursor, cnx, [3,False])
    #storeAccess(cursor, cnx, account)
    #purchaseHistory(cursor, cnx, account)
    print("\nWelcome to the Rays-Shop!")
    print("1) Sign up")
    print("2) Sign in")
    print("3) Quit")
    
    ch1 = input(">>")
    if ch1 not in ["1" , "2"]:
        logging.error("Entry not found quitting program...")
        return
    if ch1 == "1":        
        account = createAccount(cursor, cnx)
        if account == None:
            logging.error("Account not created quitting program...")
            return
    elif ch1 == "2":
        account = loadAccount(cursor, cnx)
        if account == None:
            logging.error("Account not found attempting to create a new one...")
            print("Create a new account?")
            ch2 = input("y/n")
            if ch2 == "y" or ch2 == "Y":
                account = createAccount(cursor, cnx)
                if account == None:
                    logging.error("Account not created quitting program...")
                    return
            else:
                return
    if account[1] == True:
        adminAccount(cursor, cnx,account)
    elif account[1] == False:
        print(account)
        userChoice(cursor,cnx,account)
    else:
        print("Error quitting program")
        return
    



def createAdmin(cursor, cnx):
    q1 = f"select is_admin from useraccounts where is_admin = {True};"
    run = cursor.execute(q1)
    if not run:
        adminentry = [""]
        print("Please enter a username. Must be at least 5 charecters long.")
        adminentry[0]= input(">>")
        
        while len(adminentry[0]) <= 6:
            print("Error length of username must have at least 6 charecters. \nEnter a new username")
            logging.error("Length of username was less than 5 charecters. Trying again...")
            adminentry[0] = input(">>")
        
        print("Please enter your First name.")
        entry = input(">>")
            
        
        while True:
            try:
                for test in entry:
                    if test.isdigit():
                        raise ValueError
                
                
                #re.search('[0-9]', adminentry[1])
            except ValueError as ve:
                print("\nCannot have integers in name.")
                logging.error("User tried to enter an integer to their name, trying again...")    
            else:
                adminentry.append(entry)
                break
            
            print("Please enter your First name.")
            entry = input(">>")
        
        print("Please enter your Last name.")
        entry = input(">>")
        
        while True:
            try:
                for test in entry:
                    if test.isdigit():
                        raise ValueError
                
                
            except ValueError as ve:
                print("\nCannot have integers in name.")
                logging.error("User tried to enter an integer to their name, trying again...")    
            else:
                adminentry.append(entry)
                break
            
            print("Please enter your Last name.")
            entry = input(">>")
            
        

        #address skipped
        adminentry.append("")
        print("Please enter a password. Must be at least 6 charecters long")
        entry = input(">>")
        
        
        while len(entry) < 6:
            print("Error length of password must have at least 5 charecters. \nEnter a new password")
            logging.error("Length of password was less than 6 charecters. Trying again...")
            entry = input(">>")
        adminentry.append(entry)

        q2 = f"insert into useraccounts (userName, firstName, lastName, address, user_password, is_admin) values ( '{adminentry[0]}', '{adminentry[1]}', '{adminentry[2]}' , '{adminentry[3]}' , '{adminentry[4]}' , {True});"
        cursor.execute(q2) 
        cnx.commit()
        q1 = f"select * from useraccounts where userName = '{adminentry[0]}'"
        cursor.execute(q1)
        result = cursor.fetchall() 
        return (result[0][0],True)
        
    else:
        print("Admin already exists.")
        return None

def createAccount(cursor, cnx):
    print("Create Account")
    print("1) New User")
    print("2) Admin")
    print("3) Quit")
    ch1 = input(">>")
        
    if ch1 not in ["1" , "2"]:
        return None
    if ch1 == "2":
        print("Enter Admin Password.")
        adminPswd = input(">>")
        if adminPswd != "Pass123":
            tries = 0
            attempts = 3
            while tries < 4:
                print("Wrong password entered " + str(attempts) + " attempts remaining")
                adminPswd = input("Enter admin password: ")
                if adminPswd != "RayIsTheBest":
                    continue
                else:
                    break
        if adminPswd == "RayIsTheBest":
            return createAdmin(cursor, cnx)
        else:
            return None
    
    q1 = "Select userName from userAccounts;"
    
    cursor.execute(q1)  
    userNames = cursor.fetchall()
    userEntry = [""]
    
    
    print("Please enter a username. Must be at least 5 charecters long.")
    userEntry[0]= input(">>")
    
    while True:
        i = 0
        try:
            if len(userEntry[0]) >= 6:
                for userName in userNames:
                    print(userName[i])
                    if userName[i] == userEntry[0]:
                        raise ValueError
                break
            elif len(userEntry[0]) <= 6:
                print("Username must be at least 6 charecters long...")
        except ValueError:
            logging.error("User name already exsists trying again...")
            print("Error username already exists.")
        print("Please enter a username. Must be at least 5 charecters long.")
        userEntry[0] = input(">>")    
    
    print("Please enter your First name.")
    entry = input(">>")
    userEntry.append(entry)    
    
    while True:
        try:
            for test in entry:
                if test.isdigit():
                    raise ValueError
        except ValueError as ve:
            print("\nCannot have integers in name.")
            logging.error("User tried to enter an integer to their name, trying again...")    
        else:
            break
        
        print("Please enter your First name.")
        entry = input(">>")
        userEntry[1] = entry
    print("Please enter your Last name.")
    entry = input(">>")
    userEntry.append(entry)
    while True:
        try:
            for test in entry:
                if test.isdigit():
                    raise ValueError
        except ValueError as ve:
            print("\nCannot have integers in name.")
            logging.error("User tried to enter an integer to their name, trying again...")    
        else:
            break
        
        print("Please enter your Last name.")
        entry = input(">>")
        userEntry[2] = entry
    
    
    print("Please enter your address.")
    entry = input(">>")
    userEntry.append(entry)
    
    print("Please enter a password. Must be at least 6 charecters long")
    entry = input(">>")
    
    
    while len(entry) < 6:
        print("Error length of password must have at least 5 charecters. \nEnter a new password")
        logging.error("Length of password was less than 6 charecters. Trying again...")
        entry = input(">>") 
    userEntry.append(entry)
 
    q2 = f"insert into useraccounts (userName, firstName, lastName, address, user_password, is_admin) values ( '{userEntry[0]}', '{userEntry[1]}', '{userEntry[2]}' , '{userEntry[3]}' , '{userEntry[4]}' , {False});"
    cursor.execute(q2) 
    cnx.commit()
    q1 = f"select * from useraccounts where userName = '{userEntry[0]}';"
    cursor.execute(q1)
    result = cursor.fetchall()
    return (result[0][0],False)
    
def adminAccount(cursor, cnx,admin):

    print("What would you like to do?")
    print("\t1) View Accounts")
    print("\t2) View purchase history")
    print("\t3) View store")
    print("\t4) Quit")
    ch1 = input(">>")
      
    if ch1 not in  ['1', '2', '3']:
        logging.info("Quitting program...")
        exit() 
    if ch1 == '1':
        accountViewer(cursor, cnx, admin)
        
    elif ch1 == '2':
        purchaseHistory(cursor, cnx, admin)
        
    else:
        storeAccess(cursor, cnx, admin)
        
    
def loadAccount(cursor, cnx):
    q1= "SELECT userID, userName, user_password from useraccounts;"
    cursor.execute(q1)  
    userNames = cursor.fetchall()
    x = 0
    count = 5
    print("Enter your username.")
    user = input(">>")
    print("Enter your password.")
    password = input(">>")
    while x <= 5:
        for i in userNames:
            print(i)
            if i[1] == user and i[2] ==  password:
                is_user = True
                break
            else:
                is_user = False
                continue
        if is_user == True:
            break
        else:
            print(f"Username or password is incorrect please try again, you have {count} more attempts")
            print("Enter your username.")
            user = input(">>")
            print("Enter your password.")
            password = input(">>")
        count -= 1
        x += 1
    q2= f"SELECT userID, userName, firstName, lastName, address, is_admin from useraccounts where userName = '{user}';"
    cursor.execute(q2)

    result = cursor.fetchall()
    print(tabulate(result, headers=['User ID', 'Username', 'First Name', 'Last Name', 'Address', 'Admin'], tablefmt='psql'))
   
    userData =result[0]
    
    input(">>")
    return(userData[0], userData[5])
    
    
              
def storeAccess(cursor, cnx, account):
    query = f"select * from items;"
    cursor.execute(query)
    results = cursor.fetchall()    
    print(tabulate(results, headers=['ItemID', 'Item Name', 'Price', 'Stock'], tablefmt='psql'))
    
    
  
    
    if account[1] == True:    
        print("What would you like to do?")
        print("1) Add item to inventory.")
        print("2) Update item count.")
        adminch = input(">>")
        while adminch not in ['1', '2']:
            print("Error wrong entry, would you like to quit?")
            ch1 = input("y/n:")
            if ch1 != "n":
                exit()
            else:
                print("What would you like to do?")
                print("1) Add item to inventory.")
                print("2) Update item count.")
                adminch = input(">>")
        if  adminch == "1":
            addItem(cursor,cnx)
        elif adminch == "2": 
            updateItem(cursor,cnx)  
    elif account[1] == False:
        makePurchase(cursor, cnx, account)


def accountViewer(cursor, cnx, account):
    if account[1] == True:
        q1 = f"select userID, userName, is_admin from userAccounts order by userID;"
        cursor.execute(q1)
        result = cursor.fetchall()
        print(tabulate(result, headers=['userID', 'Username', 'Is Admin'], tablefmt='psql'))
        print("\nWhat would you like to do?")
        print("1) Update a users admin credentials.")
        print("2) Check users purchase history.")
        print("3) Go to item page.")
        
        ch1 = input(">>")
        while ch1 not in ["1","2","3"]:
            print("Error wrong entry, would you like to quit?")
            ch3 = input("y/n:")
            if ch3 != "n":
                logging.info("User chose to quit program, closing program...")
                exit()
            else:
                print("\nWhat would you like to do?")
                print("1) Update a users admin credentials.")
                print("2) Check users purchase history.")
                print("3) Go to item page.")
                ch2 = input(">>")
        if ch1 == "1":
            updateAccount(cursor,cnx,account)
        elif ch1 == "2":
            purchaseHistory(cursor, cnx, account)
        else:
            storeAccess(cursor, cnx, account)

def userChoice(cursor, cnx, account):
        q2 = f"select userID, userName, firstName, lastName, address, user_password from useraccounts where userID = {account[0]};"
        cursor.execute(q2)
        result = cursor.fetchall()
        print(tabulate(result, headers=['userID', 'Username', 'First Name', 'Last Name', 'Address', 'Password'], tablefmt='psql'))
        print("\nWhat would you like to do?")
        print("1) Update account info")
        print("2) Check purchase history.")
        print("3) Make a purchase.")
        
        ch2 = input(">>")
        while ch2 not in ["1","2","3"]:
            print("Error wrong entry, would you like to quit?")
            ch3 = input("y/n:")
            if ch3 != "n":
                logging.info("User chose to quit program, closing program...")
                exit()
            else:
                print("\nWhat would you like to do?")
                print("1) Update account info")
                print("2) Check purchase history.")
                print("3) Make a purchase.")
                ch2 = input(">>")
        if ch2 == "1":
            updateAccount(cursor,cnx,account)
        elif ch2 == "2":
            purchaseHistory(cursor, cnx, account)
        else:
            makePurchase(cursor, cnx, account)


def purchaseHistory(cursor, cnx, account):
    if account[1] == True:
        query = f"select * from order_history;"
        cursor.execute(query)
        results = cursor.fetchall()        
        print(tabulate(results, headers=['orderID', 'userID', 'Item ID', 'Amount Spent', 'Number of Items', 'Order Date'], tablefmt='psql'))
        print("\nWould you like to do another action?")
        ch = input("Y/N:")
        print(ch)
        if ch == "Y" or ch == "y":
            print("here")
            adminAccount(cursor,cnx,account)
        else:
            quit()
    elif account[1] == False:
        query = f"select * from order_history where userID = {account[0]} order by order_date;"
        cursor.execute(query)
        results = cursor.fetchall()        
        print(tabulate(results, headers=['orderID', 'userID', 'Item ID', 'Amount Spent', 'Number of Items', 'Order Date'], tablefmt='psql'))        
        print("\nWould you like to do another action?")
        ch = input("Y/N:")
        print(ch)
        if ch == "Y" or ch == "y":
            print("here")
            userChoice(cursor,cnx,account)
        else:
            quit()

def makePurchase(cursor, cnx, account):
    query = f"select * from items;"
    cursor.execute(query)
    results = cursor.fetchall()    
    print(tabulate(results, headers=['ItemID', 'Item Name', 'Price', 'Stock'], tablefmt='psql'))
    
    query = f"select * from items;"
    cursor.execute(query)
    itemlist = cursor.fetchall()
    itemData = []
    found = False
    done = False
    for i in itemlist:
        itemData.append(i)
    while done == False:    
        print("What would you like to buy?")
        print("Choose item number.")
        itemID = int(input(">>"))
    
        while True:
            for i in itemData:
                print(i)
                if itemID == i[0]:
                    print(i[3])
                    stock = i[3]
                    price = i[2]
                    found = True

                    break

            if found == True:
 
                if stock == 0:
                    print("Sorry we are currently out of stock of that item")
                    print("Would you like to choose another item?")
                    ch1 = input("y/n:")
                    if ch1 == "y" or ch1 == "Y":
                        print("Choose item number.")
                        itemID = int(input(">>")) 
                    else:
                        quit()
                else:
                    break    
                
            else:
                print("Error wrong entry, would you like to quit?")
                ch1 = input("y/n:")
                if ch1 == "y" or ch1 == "Y":
                    print("Choose item number.")
                    itemID = int(input(">>")) 
                else:
                    quit()
        newStock = 0        
        print("Choose number of items you would like to purchase.")
        itemNum = int(input(">>"))
        while True:
            
            if int(itemNum) > stock:
                print("Not enough stock to fulfill your purchase.")
                print("Would you like to take what we have?")
                ch1 = input("y/n:")
                if ch1 == "y" or ch1 == "Y":
                    itemNum = stock
                    newStock = 0
                    done = True
                else:
                    print("\nWould you like to do another action?")
                    ch = input("Y/N:")
                    if ch == "Y" or ch == "y":
                        userChoice(cursor,cnx,account)
                    else:
                        exit()
                    exit()
                
                break
            elif int(itemNum) <= 0:
                print("Error wrong entry, would you like to quit?")
                ch1 = input("y/n:")
                if ch1 != "n":
                    exit()
                else:
                    print("Choose item ammount.")
                    itemNum = int(input(">>"))
            else: 
                newStock = stock - int(itemNum)
                done = True
                break
    
    now = datetime.now()
    date = now.strftime("%Y-%m-%d")
    print(date)
    query = f"insert into order_history(userID, itemID, amount_spent, numItems, order_date) values ({account[0]}, {int(itemID)}, {(price * int(itemNum))}, {int(itemNum)},str_to_date('{date}','%Y-%m-%d'));" 
    cursor.execute(query)
    cnx.commit()
    query = f"update items set inventory = {newStock} where itemID = {itemID};"
    cursor.execute(query)
    cnx.commit()
    query = f"select * from items;"
    cursor.execute(query)
    results = cursor.fetchall()
    
    print(tabulate(results, headers=['ItemID', 'Item_name', 'Price', 'Stock'], tablefmt='psql'))
    print("\nWould you like to do another action?")
    ch = input("Y/N:")
    if ch == "Y" or ch == "y":
        userChoice(cursor,cnx,account)
    else:
        exit()
    
def addItem(cursor,cnx):
    print("What is the name of the item?")
    name = input(">>")
    while not name:
        logging.error("User did not enter a name, trying again...")
        print("Name cannot be empty.")
        print("Would you like to quit?")
        ch1 = input("y/n:")
        if ch1 != "n":
            logging.info("User chose to quit program, closing program...")
            exit()
        else:
            print("What is the name of the item?")
            name = input(">>")
            
        
    print("What is the price of the item?")
    price = int(input(">>"))
    while type(price) != int:
        logging.error("User did not enter an integer, trying again...")
        print("Price must be an integer.")
        print("Would you like to quit?")
        ch1 = input("y/n:")
        if ch1 != "n":
            logging.info("User chose to quit program, closing program...")
            exit()
        else:
            print("What is the price of the item?")
            price = int(input(">>"))
    print("How many items are being added?")
    inventory = int(input(">>"))
    while type(inventory) != int:
        logging.error("User did not enter an integer, trying again...")
        print("Inventory must be an integer.")
        print("Would you like to quit?")
        ch1 = input("y/n:")
        if ch1 != "n":
            logging.info("User chose to quit program, closing program...")
            exit()
        else:
            print("How many items are being added?")
            inventory = int(input(">>"))
        
    query = f"insert into items(item_name, item_price, inventory) values ('{name}',{price},{inventory});"
    cursor.execute(query)
    cnx.commit()

    query = f"select * from items;"
    cursor.execute(query)
    results = cursor.fetchall()    
    print(tabulate(results, headers=['ItemID', 'Item Name', 'Price', 'Stock'], tablefmt='psql'))
    print("\nWould you like to do another action?")
    ch = input("Y/N:")

    if ch == "Y" or ch == "y":

        adminAccount(cursor,cnx,[1,True])
    else:
        quit()

def updateAccount(cursor,cnx,account):
    if account[1] == True:
        print("here")
        q1 = f"select userID, userName, is_admin from userAccounts order by userID;"
        cursor.execute(q1)
        result = cursor.fetchall()
        print(tabulate(result, headers=['userID', 'Username', 'Is Admin'], tablefmt='psql'))
        print("\nEnter userID you want to update.")
        ch1 = int(input(">>"))
        passd = False
        while passd != True:
            i = 0
            try:
                
                for userID in result:
                    print(userID[0])
                    if userID[0] == ch1:
                        passd = True
                        break    
                if passd == True:
                    break
                else:
                    raise ValueError     
                    
            except ValueError:
                logging.error("UserID not found. trying again...")
                print("Error userID not found, would you like to quit?")
                ch3 = input("y/n:")
                if ch3 != "n" or ch3 !="N":
                    logging.info("User chose to quit program, closing program...")
                    exit()
                print("Please enter a userID")
                ch1 = input(">>")
        print("1) Add admin access")
        print("2) Remove admin access")
        ch2 = input(">>")
        while ch2 not in ["1","2"]:
            logging.error("Entry not recognised. trying again...")
            print("Entry not recognised, would you like to quit?")
            ch3 = input("y/n:")
            if ch3 != "n" or ch3 !="N":
                logging.info("User chose to quit program, closing program...")
                exit()
            print("1) Add admin access")
            print("2) Remove admin access")
            ch2 = input(">>") 
        if ch2  == "1":
            admin = True
        else:
            admin = False
        q2 = f"update userAccounts set is_admin = {admin} where userID = {ch1};"
        cursor.execute(q2)
        cnx.commit()
        q1 = f"select userID, userName, is_admin from userAccounts where userID = {int(ch1)};"        
        cursor.execute(q1)
        result = cursor.fetchall()
        print(tabulate(result, headers=['userID', 'Username', 'First name' , 'Last name', 'Password'], tablefmt='psql'))
        print("Would you like to do another action?")
        ch = input("Y/N:")
        if ch == "Y" or ch == "y":
            accountViewer(cursor,cnx,account)
        else:
            quit()
    else:
        print("What would you like to update?")
        print("1) First Name")
        print("2) Last Name")
        print("3) Address")
        print("4) Password")
        ch4 = input(">>")
        while ch4 not in ["1","2", "3" , "4"]:
            logging.error("Entry not recognised. trying again...")
            print("Entry not recognised, would you like to quit?")
            ch3 = input("y/n:")
            if ch3 != "n" or ch3 !="N":
                logging.info("User chose to quit program, closing program...")
                exit()
            print("What would you like to update?")
            print("1) First Name")
            print("2) Last Name")
            print("3) Address")
            print("4) Password")
            ch4 = input(">>")
        
        if ch4 == "1":
            acct = "firstName"
            print("What would you like to change it to?")
            updt= input(">>")
        elif ch4 == "2":
            acct = "lastName"
            print("What would you like to change it to?")
            updt= input(">>")
        elif ch4 == "3":
            acct = "address"
            print("What would you like to change it to?")
            updt= input(">>")
        else:
            acct = "user_password"
            print("Please enter a new password. Must be at least 6 charecters long")
            updt = input(">>")
            while len(updt) < 6:
                print("Error length of password must have at least 5 charecters. \nEnter a new password")
                logging.error("Length of password was less than 6 charecters. Trying again...")
                updt = input(">>") 
        q2 = f"update userAccounts set {acct} = '{updt}' where userID = {int(account[0])};"
        cursor.execute(q2)
        cnx.commit()
        q1 = f"select userID, userName, firstName, lastName, address, user_password from userAccounts where userID = {int(account[0])} ;"
        cursor.execute(q1)
        result = cursor.fetchall()
        print(tabulate(result, headers=['userID', 'Username', 'First name' , 'Last name', 'Password'], tablefmt='psql'))
        print("Would you like to do another action?")
        ch = input("Y/N:")
        if ch == "Y" or ch == "y":
            userChoice(cursor,cnx,account)
        else:
            quit()
        
        
def updateItem(cursor,cnx):
    query = f"select * from items;"
    cursor.execute(query)
    results = cursor.fetchall()
    
    print(tabulate(results, headers=['ItemID', 'Item_name', 'Price', 'Stock'], tablefmt='psql'))
    print("\nChoose item ID that you would like to update.")
    itemID = int(input(">>"))
    isgood = False 
    while isgood == False:
        if not itemID or type(itemID) != int:
            print("\nWrong entry.")
            print("Choose item ID that you would like to update.")
            itemID = int(input(">>"))
        else:
            for i in results:
                if itemID == i[0]:
                    isgood = True
                    break
            if isgood != True:
                print("Item not found, would you like to quit?")
                ch = input("Y/N:")
                if ch != "N" or ch != "n":
                    exit() 
                print("Choose item ID that you would like to update.")
                itemID = int(input(">>"))
    print("\nWhat would you like to update?")
    print("1) Price")
    print("2) Inventory")
    
    ch2 = input(">>")
    while ch2 not in ['1','2']:
        print("\nWrong entry, would you like to quit?")
        ch3 = input("Y/N:")
        if ch3 != "N" or ch3 != "n":
            exit()
        print("\nWhat would you like to update?")
        print("1) Price")
        print("2) Inventory")
    
        ch2 = input(">>")
    if ch2 == "1":
        col =  "item_price"
        print("\nWhat is the new price?")
        ch4 = int(input(">>")) 
        while True:
            if not ch4 or type(ch4) != int:
                print("\nWrong entry, price must be an integer.")
                print("What is the new price?")
                ch4 = int(input(">>"))
            elif ch4 <= 0:
                print("\nWrong entry, price must be a positive integer.")
                print("What is the new price?")
                ch4 = int(input(">>"))
            else:
                break
                
    elif ch2 == "2":
        col = "inventory"
        print("\nWhat is the new inventory amount?")
        ch4 = int(input(">>"))
        while True:
            if not ch4 or type(ch4) != int:
                print("\nWrong entry, inventory must be an integer.")
                print("What is the new inventory amount?")
                ch4 = int(input(">>"))
            elif ch4 <= 0:
                print("\nWrong entry, inventory must be a positive integer.")
                print("What is the new inventory amount?")
                ch4 = int(input(">>"))
            else:
                break
    q2 = f"update items set {col} = {ch4} where itemID = {itemID};"
    
    cursor.execute(q2)
    cnx.commit()
    query = f"select * from items;"
    cursor.execute(query)
    results = cursor.fetchall()
    
    print(tabulate(results, headers=['ItemID', 'Item_name', 'Price', 'Stock'], tablefmt='psql'))
    print("\nWould you like to do another action?")
    ch = input("Y/N:")
    if ch == "Y" or ch == "y":

        adminAccount(cursor,cnx,[1,True])
    else:
        quit()
main()       
    