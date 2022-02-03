# -*- coding: utf-8 -*-
"""
Created on Thu Nov 26 14:34:11 2020

@author: Sayed Afnan Khazi
    """
######Admin Module######                         
import SupermarketappFunctionsModule as m  
m.getenvvariables()      
m.importandconnect(sqlusername=m.env_sqlusername,sqlpasswd=m.env_sqlpassword,hosty=m.env_sqlhost)
import pickle
import os                                 
import csv
import datetime
def AdministrativeMode():                                 
#if True:
    print("*****Welcome to Administrative mode!*****")
    username=input("Enter Username(Use 'Admin' for first time run):")   #already put [Name:'Admin',Username:'Admin',Password:1,Role:'Admin']
    pwd=input("Enter Password(Press 1 for first time run):") 
    try:
        fobj=open("ProfileManager.bin","rb")
        while True:
            UserIsAdmin=False                    #User is not admin unless proven otherwise
            UserIsEmployee=False
            profilerec=pickle.load(fobj)
            if profilerec[1]==username and profilerec[2]==pwd:               ##0-name,1-username,2-password,3-role
                if profilerec[3]=='Admin':
                    UserIsAdmin=True
                    print("*************************************************************")
                    print('*****Welcome',profilerec[0],',Admin Priviledges Granted!*****')
                    print("*************************************************************")
                    fobj.close()
                    break
                elif profilerec[3]=='Employee': #MARK ATTENDANCE AND CHECK SAL 
                    UserIsEmployee=True
                    print("*************************************************************")
                    print('*****Welcome employee:',profilerec[0],'!*****')
                    print("*************************************************************")
                    break
                    fobj.close()
    except EOFError:
        print("*****Incorrect Username Or Password*****")
        print("Error:UserNotFound/Does Not Exist")
    if UserIsAdmin:
        progcontinue=1
        while progcontinue==1:
            print("Here you can manage product details, like names, barcodes and cost")
            print("You can also manage your employees\'s credentials and salaries as well.")
            print()
            print("*************************************************************")
            print("\t Press 0 to Open the Inventory Management Sofware")
            print("\t Press 1 to configure/set up the application (First time run)")       
            print("\t Press 2 to create/manage a profile")
            print("\t Press 3 to manage product details")
            print("\t Press 4 to manage employee details")
            print("\t Press 5 to open employee attendance logs")
            print("\t Press 6 to exit Admin mode")          
            print("*************************************************************")
            ca=int(input("Enter an option:"))
            print()
            if ca==1:
                print('*****WARNING: If you have configured the application before, it will DELETE your data!!*****')
                ca1i=int(input("Are you sure? :(1=No,2=Yes)"))
                if ca1i==2:
                    print("====[SupermarketApp]==== \n Configuring Databases...")
                    try:
                        m.curobj.execute("CREATE DATABASE IF NOT EXISTS supermarketapp")
                        m.curobj.execute("USE supermarketapp")
                        print()
                        m.curobj.execute("""CREATE TABLE IF NOT EXISTS products2 (
                                            pname VARCHAR(50),
                                            pbarcode DOUBLE PRIMARY KEY,
                                            pprice float,
                                            invqty int DEFAULT 0)""")
                        m.curobj.execute("""CREATE TABLE IF NOT EXISTS employee2 (
                                            enum INTEGER PRIMARY KEY,
                                            ename VARCHAR(50) NOT NULL,
                                            eusername VARCHAR(50) NOT NULL,
                                            epassword VARCHAR(50) NOT NULL,
                                            salary float NOT NULL,
                                            bonus float NOT NULL)""")
                        initch1=int(input("Would you like to insert sample products?(1=Yes,2=No)"))
                        if initch1==1:
                            o=int(input("Enter the amount of each products to be inserted:"))
                            while True:
                                if o<0 or o>1000:
                                    print("You cannot enter a negative number, OR It is not advisable to have more than 1000 items of the same stock in the system")
                                else:
                                    break
                            m.curobj.execute("INSERT INTO products2 VALUES('LaysChips',123456789012,10.0,"+str(o)+")")
                            m.curobj.execute("INSERT INTO products2 VALUES('Tide1kg',234567890123,500.0,"+str(o)+")")
                            m.curobj.execute("INSERT INTO products2 VALUES('Bisleri500ml',345678901234,18.0,"+str(o)+")")
                            m.curobj.execute("INSERT INTO products2 VALUES('Act2Popcorn',456789012345,45.0,"+str(o)+")")
                            m.curobj.execute("INSERT INTO products2 VALUES('Stylus',567890123456,500.0,"+str(o)+")")
                            m.curobj.execute("INSERT INTO products2 VALUES('Tide5kg',678901234567,2200.0,"+str(o)+")")
                            m.curobj.execute("INSERT INTO products2 VALUES('LemonJuice',789012345678,60.0,"+str(o)+")")
                            m.curobj.execute("INSERT INTO products2 VALUES('WaterBottle',890123456789,180.0,"+str(o)+")")
                            m.curobj.execute("INSERT INTO products2 VALUES('KitKat',901234567890,6.0,"+str(o)+")")
                            print("Successfully Added All Sample Products.")
                    except:
                        print("An Error Occured while creating the tables OR inserting the sample data")
            elif ca==0:
                while True:
                    print("*************************************************************")
                    print("*****Welcome to the Inventory manager!*****")
                    print("*************************************************************")
                    print("\t Press 0 to display all product details and inventory")
                    print("\t Press 1 to check if a reorder is required")
                    print("\t Press 2 to recieve stock(Add stock/accept reorder)")
                    print("\t Press 3 to exit from the inventory manager")
                    print("*************************************************************")
                    cinv=int(input("Enter an option:"))
                    if cinv==0:                         #ADD ElSE  (ADDED)
                        try:
                            m.curobj.execute("select pname,pbarcode,pprice,invqty from products2")
                            resultset=m.curobj.fetchall()
                            print('*'*83)
                            print('|','%24s'%'Product Name','|','%16s'%'Product Barcode','|','%10s'%'Price','|','%20s'%'Inventory Quantity','|')
                            print('*'*83)
                            for j in resultset:
                                print('|','%24s'%j[0],'|','%16s'%int(j[1]),'|','%10s'%j[2],'|','%20s'%j[3],'|')
                            print('*'*83)
                        except:
                            print("An Error Occurred whiile retrieving the data.")
                    elif cinv==3:
                        break
                    elif cinv==1:
                        print("*************************************************************")
                        minqty=int(input("Enter the minimum quantity of products for search:"))
                        m.displayreordersrequired(minqty)
                    elif cinv==2:
                        while True:
                            print("*************************************************************")
                            print("\t Press 1 to accept a reorder based on Product names")
                            print("\t Press 2 to accept a reorder based on Product barcodes")
                            print("\t Press 3 to go back")
                            print("*************************************************************")
                            cinvx=int(input("Enter an option:"))
                            if cinvx==3:
                                break
                            elif cinvx==1:
                                try:
                                    pname=input("Enter the Product's name:")
                                    qty=int(input("Enter quantity received:"))
                                    m.acceptreorderpname(pname,qty)
                                except:
                                    print("An Error Occurred(InvErr1)")
                            elif cinvx==2:
                                try:
                                    pbarcode=int(input("Enter the Product's barcode:"))
                                    qty=int(input("Enter the quantity received:"))
                                    m.acceptreorderpbarcode(pbarcode,qty)
                                except:
                                    print("An Error Occurred(InvErr2)")
                    else:
                        print("Incorrect Answer")
            elif ca==2:         ##PROFILE CREATION
                profileexe=1                               ##Infinite loop controler/for menu program
                while profileexe==1:
                    print("*************************************************************")
                    print("*****Welcome to the profile manager/creator!*****")
                    print("*************************************************************")
                    print("\t Press 1 to create a new profile")
                    print("\t Press 2 to manage profiles")
                    print("\t Press 3 to exit from the profile manager")
                    print("*************************************************************")
                    ca2i=int(input("Enter an option:"))
                    print()
                    if ca2i==1:
                         try:
                            print("*************************************************************")
                            print("*****You are now Creating a new profile!*****")
                            print("*************************************************************")
                            fobj=open("ProfileManager.bin","ab+")
                            enum=int(input('Enter the employee number:'))
                            ename=input("Enter the profile name:")
                            eusername=input("Enter the profile's login username:")
                            epassword=input("Enter the profile's password:")
                            salary=float(input("Enter the employee's salary:"))
                            bonus=salary*0.05
                            while True:
                                erole=input("Enter the user's role('Admin' or 'Employee'):")
                                if erole=='Admin' or erole=='Employee':
                                    break
                                else:
                                    continue
                            eprofilerec=[ename,eusername,epassword,erole]
                            pickle.dump(eprofilerec,fobj)
                            m.curobj.execute("insert into employee2 VALUES({},'{}','{}','{}',{},{})".format(enum,ename,eusername,epassword,salary,bonus))
                            m.mycon.commit()
                            print("*************************************************************")
                            print()
                            print("Profile Created! \n Name:",ename,"\n Username:",eusername,"\n Password:",epassword,"\n Role:",erole)
                            print("*************************************************************")
                            fobj.close()
                         except:
                             print("An Error Occured in ca2iA (Error Code)")
                    elif ca2i==2:
                        print("*************************************************************")
                        print("*****Welcome to the Profiles manager!*****")
                        print("*************************************************************")
                        print("\t Press 1 to display all profiles")
                        print("\t Press 2 to delete a profile")
                        print("\t Press 3 to go back")  
                        print("*************************************************************")
                        ca2ij=int(input("Enter your option:"))
                        if ca2ij==1:
                            try:
                                fobj=open("ProfileManager.bin","rb")
                                resultset=[]
                                while True:
                                    profilerec=pickle.load(fobj)
                                    resultset.append(profilerec)
                            except EOFError:
                                fobj.close()
                                c=-1
                                print("*"*107)
                                print("*"*107)
                                print('|','%30s'%'Name','|','%26s'%'Username','|','%28s'%'Password','|','%10s'%'Role','|')
                                print("*"*107)
                                for x in resultset:
                                    c+=1
                                    print('|','%30s'%x[0],'|','%26s'%x[1],'|','%28s'%x[2],'|','%10s'%x[3],'|')
                                else:
                                    print("*"*107)
                                    print("The Total Number of Employees/records fetched is",c)
                                    print("*"*107)
                                    print()
                                    print()
                        elif ca2ij==2:
                            try:
                                deletedqn=False
                                print("*************************************************************")
                                print("*****You are now deleting a user profile from the system!*****")
                                print("*************************************************************")
                                username=input("Enter the username:")
                                fobj=open("ProfileManager.bin","rb")
                                fobj2=open("dummy.bin","wb")
                                while True:
                                    rec=pickle.load(fobj)
                                    if rec[1]==username:
                                        deletedqn=True
                                        m.curobj.execute("delete from employee2 where eusername='{}'".format(username))
                                        m.mycon.commit()
                                    else:
                                        pickle.dump(rec,fobj2)
                            except EOFError:
                                fobj.close()
                                fobj2.close()
                                if deletedqn==True:
                                    print("*************************************************************")
                                    print("The record with username",username,"was deleted.")
                                    print("*************************************************************")
                                elif deletedqn==False:
                                    print("*************************************************************")
                                    print("The record with username",username,"was not deleted because either doesn't exist, or an error occurred")
                                    print("*************************************************************")
                                else:
                                    print("An Error Occured while deleting the employee details. Please contact the Administrator.")
                                os.remove("ProfileManager.bin")
                                os.rename("dummy.bin","ProfileManager.bin")
                        elif ca2ij==3:
                            print('Exiting The Profile Manager!')
                    elif ca2i==3:
                        profileexe=0
            elif ca==6:
                progcontinue=2
            elif ca==3:
                productexe=1
                while productexe==1:
                    print("*************************************************************")
                    print("*****Welcome to the product details editor!*****") 
                    print("*************************************************************")
                    print("\t Press 0 to view all product details")
                    print("\t Press 1 to update a product's price, name or barcode")
                    print("\t Press 2 to insert a product")
                    print("\t Press 3 to delete a product")
                    print("\t Press 4 to go back")
                    print("*************************************************************")
                    ca3i=int(input("Enter an option:"))
                    if ca3i==1:
                        m.updatemodulefun()
                    elif ca3i==0:
                        try:
                            m.curobj.execute("select pname,pbarcode,pprice,invqty from products2")
                            resultset=m.curobj.fetchall()
                            print('*'*83)
                            print('|','%24s'%'Product Name','|','%16s'%'Product Barcode','|','%10s'%'Price','|','%20s'%'Inventory Quantity','|')
                            print('*'*83)
                            for j in resultset:
                                print('|','%24s'%j[0],'|','%16s'%int(j[1]),'|','%10s'%j[2],'|','%20s'%j[3],'|')
                            print('*'*83)
                        except:
                            print("An Error Occurred whiile retrieving the data.")
                    elif ca3i==3:
                        productexei=1
                        try:
                            while productexei==1:
                                print("*************************************************************")
                                print("*****Welcome to the product deletion menu!*****")
                                print("*************************************************************")
                                print("\t Press 1 to delete using a product name")
                                print("\t Press 2 to delete using a product barcode")
                                print("\t Press 3 to go back")
                                print("*************************************************************")
                                ca3i2=int(input("Enter an option:"))
                                if ca3i2==1:
                                    pname=input("Enter the product name of the product you want to delete:")
                                    m.DeleteByProductName(pname)
                                    print("*****Product successfully Deleted!*****")
                                elif ca3i2==2:
                                    pbarcode=input("Enter the product barcode of the product you want to delete:")
                                    m.DeleteByProductBarcode(pbarcode)
                                    print("*****Product successfully Deleted!*****")
                                elif ca3i2==3:
                                    productexei=2
                                else:
                                    print("Incorrect answer, please try again")
                        except:
                            print("*****An Error Occurred while deleting*****")
                    elif ca3i==2:
                        try:
                            while True:
                                print("*************************************************************")
                                print("*****Welcome to the product insertion menu!*****")
                                print("*************************************************************")
                                print("\t Press 1 to insert a product")
                                print("\t Press 2 to go back")
                                print("*************************************************************")
                                ca3ij=int(input("Enter an option:"))
                                if ca3ij==1:
                                    pname=input("Enter the product's name:")
                                    pbarcode=input("Enter the product's barcode:")
                                    m.checkbarcode(pbarcode)
                                    pbarcode=int(pbarcode)
                                    pprice=float(input("Enter the product's price:"))
                                    m.InsertProduct(pname,pbarcode,pprice)
                                    print("*****Product successfully Inserted!*****")
                                elif ca3ij==2:
                                    break
                        except:
                            print("*****An Error Occurred while inserting*****")
                    elif ca3i==4:
                        productexe=2
            elif ca==4:
               while True:
                    print("*************************************************************")
                    print("*****Welcome To The Employee Details Manager!*****")
                    print("*************************************************************")
                    print()
                    print("\t Press 0 to see all employee details")
                    print("\t Press 1 to update a profile's password")
                    print("\t Press 2 to update an employee's salary")
                    print("\t Press 3 to update a profile's name")
                    print("\t Press 4 to update a profile's username")
                    print("\t Press 5 to change a profile's role")
                    print("\t Press 6 to go back")
                    print()
                    print("*************************************************************")
                    cai=int(input("Enter an option:"))
                    if cai==6:
                        break
                    elif cai==0:
                        try:
                            m.curobj.execute("select enum,ename,eusername,epassword,salary,bonus from employee2")
                            resultset=m.curobj.fetchall()
                            print('*'*119)
                            print('|','%10s'%'eno','|','%20s'%'ename','|','%20s'%'eusername','|','%20s'%'epassword','|','%20s'%'Salary','|','%10s'%'Bonus','|')
                            print('*'*119)
                            for i in resultset:
                                print('|','%10s'%i[0],'|','%20s'%i[1],'|','%20s'%i[2],'|','%20s'%i[3],'|','%20s'%i[4],'|','%10s'%i[5],'|')
                            print('*'*119)
                        except:
                            print("An Error Occurred whiile retrieving the data.")
                    elif cai==1:
                        try:
                            print("*************************************************************")
                            updatedqn=False
                            username=input("Enter the (current) username:")
                            newpassword=input("Enter the updated password:")
                            print("*************************************************************")
                            fobj=open("ProfileManager.bin","rb")
                            fobj2=open("dummy.bin","wb")
                            while True:
                                rec=pickle.load(fobj)
                                if rec[1]==username:
                                    oldpassword=rec[2]
                                    rec[2]=newpassword
                                    m.curobj.execute("update employee2 set epassword='{}' where eusername='{}'".format(newpassword,username))
                                    m.mycon.commit()
                                    updatedqn=True
                                    pickle.dump(rec,fobj2)
                                else:
                                    pickle.dump(rec,fobj2)
                        except EOFError:
                            fobj.close()
                            fobj2.close()
                            if updatedqn==True:
                                print("*************************************************************")
                                print("The password of the record with username",username,"with the old password",oldpassword,"was updated to",newpassword)
                            elif updatedqn==False:
                                print("*************************************************************")
                                print("An Error occurred and could not change the password.")
                            else:
                                print("An Error Occured while updating")
                            print("*************************************************************")
                            os.remove("ProfileManager.bin")
                            os.rename("dummy.bin","ProfileManager.bin")
                    elif cai==2:
                        try:
                            updatedqn=False
                            print("*************************************************************")
                            username=input("Enter the username of the profile you want to update:")
                            newsal=float(input("Enter the user's new salary:"))
                            newbonus=0.05*newsal
                            print("*************************************************************")
                            m.curobj.execute("update employee2 set salary={} where eusername='{}'".format(newsal,username))
                            m.curobj.execute("update employee2 set bonus={} where eusername='{}'".format(newbonus,username))
                            m.mycon.commit()
                            updatedqn=True
                            if updatedqn==True:
                                print("*************************************************************")
                                print("The salary and bonus of the record with the username",username,"was updated to",newsal,'&',newbonus)
                                print("*************************************************************")
                        except:
                            print("An Error occurred and could not change the salary.")
                    elif cai==3:
                        try:
                            updatedqn=False
                            print("*************************************************************")
                            username=input("Enter the current username:")
                            newename=input("Enter the new name:")
                            print("*************************************************************")
                            fobj=open("ProfileManager.bin","rb")
                            fobj2=open("dummy.bin","wb")
                            while True:
                                rec=pickle.load(fobj)
                                if rec[1]==username:
                                    oldename=rec[0]
                                    rec[0]=newename
                                    m.curobj.execute("update employee2 set ename='{}' where eusername='{}'".format(newename,username))
                                    m.mycon.commit()
                                    updatedqn=True
                                    pickle.dump(rec,fobj2)
                                else:
                                    pickle.dump(rec,fobj2)
                        except EOFError:
                            fobj.close()
                            fobj2.close()
                            if updatedqn==True:
                                print("*************************************************************")
                                print("The name of the record with username",username,"with the old name",oldename,"was updated to",newename)
                            elif updatedqn==False:
                                print("*************************************************************")
                                print("AN Error occurred and could not change the name.")
                            else:
                                print("An Error Occured while updating")
                            print("*************************************************************")
                            os.remove("ProfileManager.bin")
                            os.rename("dummy.bin","ProfileManager.bin")
                    elif cai==4:
                        try:
                            updatedqn=False
                            print("*************************************************************")
                            oldusername=input("Enter the current username:")
                            newusername=input("Enter the new username:")
                            print("*************************************************************")
                            fobj=open("ProfileManager.bin","rb")
                            fobj2=open("dummy.bin","wb")
                            while True:
                                rec=pickle.load(fobj)
                                if rec[1]==oldusername:
                                    rec[1]=newusername
                                    m.curobj.execute("update employee2 set eusername='{}' where eusername='{}'".format(newusername,oldusername))
                                    m.mycon.commit()
                                    updatedqn=True
                                    pickle.dump(rec,fobj2)
                                else:
                                    pickle.dump(rec,fobj2)
                        except EOFError:
                            fobj.close()
                            fobj2.close()
                            if updatedqn==True:
                                print("*************************************************************")
                                print("The username of the record with the old username",oldusername,"was updated to",newusername)
                            elif updatedqn==False:
                                print("*************************************************************")
                                print("AN Error occurred and could not change the username.")
                            else:
                                print("An Error Occured while updating")
                            print("*************************************************************")
                            os.remove("ProfileManager.bin")
                            os.rename("dummy.bin","ProfileManager.bin")
                    elif cai==5:
                        try:
                            updatedqn=False
                            print("*************************************************************")
                            username=input("Enter the username of the profile you want to update:")
                            while True:
                                newrole=input("Enter the user's new role('Admin' or 'Employee'):")
                                if newrole=='Admin' or newrole=='Employee':
                                    break
                                else:
                                    continue
                            print("*************************************************************")
                            fobj=open("ProfileManager.bin","rb")
                            fobj2=open("dummy.bin","wb")
                            while True:
                                rec=pickle.load(fobj)
                                if rec[1]==username:
                                    oldrole=rec[3]
                                    rec[3]=newrole
                                    updatedqn=True
                                    pickle.dump(rec,fobj2)
                                else:
                                    pickle.dump(rec,fobj2)
                        except EOFError:
                            fobj.close()
                            fobj2.close()
                            if updatedqn==True:
                                print("*************************************************************")
                                print("The role of the record with the username",username,"and old role",oldrole,"was updated to",newrole)
                            elif updatedqn==False:
                                print("*************************************************************")
                                print("AN Error occurred and could not change the role.")
                            else:
                                print("An Error Occurred while updating")
                            print("*************************************************************")
                            os.remove("ProfileManager.bin")
                            os.rename("dummy.bin","ProfileManager.bin")
            elif ca==5:                ###VIEW ATTENDANCE
                print("*****Welcome to the Employee Attendance Logs Portal!*****")
                print("Here you can view the attendance logs of employees along with the date and time of their log entry.")
                logscounter=3+int(input("Enter the amount of records you want to retrieve(The last 'n' entries):"))
                try:    
                    logsfobj=open("attendancelogs.csv","r")
                    logslist=[]
                    logsreader=csv.reader(logsfobj)
                    for x in logsreader:
                        if x!=[]:
                            logslist.append(x)
                    else:
                        logslist.append(['Name','Type','log entry date and time   '])
                    print('*'*76)
                    for x in range(-1,-(logscounter-1),-1):
                            print('|','%20s'%logslist[x][0],'|','%20s'%logslist[x][1],'|', '%20s'%logslist[x][2],'|')
                    else:
                        print('*'*76)
                except:
                    print("*****End of log*****")
            ######EMPLOYEE MODE
    if UserIsEmployee:
        while True:
            print("*************************************************************")
            print("*****Welcome to the Employee Portal!*****")
            print("\t Press 1 to mark your attendance")
            print("\t Press 2 to view your salary and bonus")
            print("\t Press 3 to exit the portal")
            print("*************************************************************")
            print("NOTE:To change any of your credentials, please contact your administrator or employer.")
            print("*************************************************************")
            ce=int(input("Enter an option:"))
            if ce==3:
                break
            elif ce==2:
                m.curobj.execute("select salary,bonus from employee2 where eusername='{}'".format(username))
                res=m.curobj.fetchone()
                esal=res[0]
                ebonus=res[1]
                print("*************************************************************")
                print("The salary and bonus of the employee with the username:",username)
                print("Salary:",esal)
                print("Bonus:",ebonus)
                print("*************************************************************")
            elif ce==1:
                logsfobj=open("attendancelogs.csv","a")
                logswriter=csv.writer(logsfobj)
                while True:                   #Data validation
                    cei=input("Enter 'Tag-in' or 'Tag-out':")
                    if cei=='Tag-in' or cei=='Tag-out':
                        break
                    else:
                        print("Please input the reply exactly!")
                m.curobj.execute("select ename from employee2 where eusername='{}'".format(username))
                res=m.curobj.fetchone()
                ename=res[0]
                logswriter.writerow([ename,cei,datetime.datetime.now()])

                
                
                