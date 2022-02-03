# -*- coding: utf-8 -*-
"""
Created on Wed Nov 25 20:08:20 2020

@author: Sayed Afnan Khazi
"""
######MODULES OF FUNCTIONS#######

env_sqlusername=''
env_sqlpassword=''
env_sqlhost=''
env_buylimit=10
def getenvvariables():
    #try:
        global env_sqlusername
        global env_sqlpassword
        global env_sqlhost
        global env_buylimit
        import pickle
        fobj=open("supermarketappconfiginfo.bin",'rb') 
        d=pickle.load(fobj)
        env_sqlusername=d['sqlusername']
        env_sqlpassword=d['sqlpassword']
        env_buylimit=d['buylimit']
        env_sqlhost=d['sqlhost']
        fobj.close()
    #except:
        #print("An Error occurred retrieving the env_variables")

def importandconnect(sqlusername=env_sqlusername,sqlpasswd=env_sqlpassword,hosty=env_sqlhost):
    import mysql.connector as sqltor
    global mycon
    global curobj
    try:
        mycon=sqltor.connect(host=hosty,user=sqlusername,passwd=sqlpasswd,database="supermarketapp")  
        curobj=mycon.cursor()
        print("*****Connected to the SQL Server Successfully!*****")
    except:
        print("*****Connection to the SQL Server Failed.*****")
        while True:
            try:
                sqlconnchoice=int(input("Would you like to input updated (MySQL) credentials and try connecting again?(1=Yes,0=No)"))
                if sqlconnchoice in [1,0]:
                    break
            except:
                print("Please try again.")
        if sqlconnchoice==1:
            try:
                import pickle
                fobj=open("supermarketappconfiginfo.bin",'rb+')
                d=pickle.load(fobj)
                d['sqlusername']=input("Enter your MySQL Username:")
                d['sqlpassword']=input("Enter your MySQL Password:")
                while True:
                    try:
                        d['buylimit']=int(input("Enter the buylimit (on products while checkout)(Greater than 0):"))
                        if d['buylimit']>0:
                            break
                    except:
                        print("Try Again!")
                d['sqlhost']=input("Enter your MySQL host:")
                fobj.seek(0)
                pickle.dump(d,fobj)
                print("Successfully Updated configinfo")
                fobj.close()
            except:
                print("An Error occurred while updating configinfo")
            getenvvariables()
            try:
                mycon=sqltor.connect(host=env_sqlhost,user=env_sqlusername,passwd=env_sqlpassword)  
                curobj=mycon.cursor()
                print("*****Connected to the SQL Server Successfully!*****")
            except:
                print("*****Connection to the SQL Server Failed.*****")
        
def checkbarcode(pbarcode):         #Broken because pbarcode turns out to be a local variable
    while True:
            if len(pbarcode)!=12:
                print("Barcodes are 12 digits in length, Please try again")
                pbarcode=input("Enter the barcode (numeric)")
            else:
                break
    return

def InsertProduct(pname,pbarcode,pprice,invqty=0):
    pinsertst="insert into products2 values('{}',{},{},{})".format(pname,pbarcode,pprice,invqty)
    curobj.execute(pinsertst)
    mycon.commit()
    
def SearchPriceByProductName(pname):
    try:
        ppricecheckst="select pprice from products2 where pname='{}'".format(pname)
        curobj.execute(ppricecheckst)
        pprice=curobj.fetchone()
        print("Price=",pprice)
    except:
        print("Invalid Product Name")

def SearchPriceByProductBarcode(pbarcode):                  ###CONSIDERS BARCODES HAVE BEEN CHECKED BEFOREHAND
    try:
        ppricecheckst="select pprice from products2 where pbarcode={}".format(pbarcode)
        curobj.execute(ppricecheckst)
        pprice=curobj.fetchone()
        print("Price=",pprice)
    except:
        print("Invalid Product Name")

def CheckoutByProductName():              
                price=0
                print("--------Starting a checkout...--------")
                print("You are now checking out using product names")
                ans=1  #Boolean True
                ckcount=1
                ckppricelist=[["Item Number","Product Barcode","Product Name","Quantity","Product Price","Total Product Price","18% G.S.T."]]
                while ans==1:
                    print("Product Number:",ckcount)
                    while True:
                        ckpname=input("Enter the product \'s name:")
                        comlst=ckpname.split()
                        while comlst[0].lower()=='!search':
                            if comlst[1][0].lower()=='%' or comlst[1][-1].lower()=='%':
                                st="select pbarcode,pname,pprice from products2 where pname like '{}'".format(comlst[1])
                            else:
                                st="select pbarcode,pname,pprice from products2 where pname like '%{}%'".format(comlst[1])
                            curobj.execute(st)
                            res=curobj.fetchall()
                            if len(res)==0:
                                print("No results found.(You can only search product names.)")
                            else:
                                print('*'*60)
                                print('|','%18s'%"Product Barcode",'|','%16s'%"Product Name",'|','%16s'%"Product Price",'|')
                                print('*'*60)
                                for x in res:
                                    print('|','%18s'%x[0],'|','%16s'%x[1],'|','%16s'%x[2],'|')
                                else:
                                    print('*'*60)
                            ckpname=input("Enter the product \'s name:")
                            comlst=ckpname.split()
                        try:
                            ckpricest="select pprice,pbarcode,invqty from products2 where pname='{}'".format(ckpname)
                            curobj.execute(ckpricest)
                            ckprice1=curobj.fetchone()
                            ckprice=ckprice1[0]
                            ckpbarcode=ckprice1[1]
                            ckpinvqty=ckprice1[2]
                            break
                        except:
                            print("Invalid product name, please try again.")
                    checkster=True
                    while checkster==True:
                        pcount=int(input("How many"+' '+ckpname+' '+"do you want to purchase:"))
                        if pcount>ckpinvqty:
                            print("You cannot purchase more than what stock is available.")
                            continue
                        if pcount<=0 or pcount>env_buylimit:
                            print("You cannot purchase 0, a negative value, or more than",env_buylimit," at once. \n If you want to purchase more than",env_buylimit," items, specify",env_buylimit," here and the rest in another entry.")
                        else:
                            checkster=False
                    print(pcount,'x ',ckpname,"Costs",ckprice,"*",pcount,"=",ckprice*pcount)
                    checkster2=True
                    checkster2cont=True
                    while checkster2==True:
                        confirmation=int(input("Are you sure you want to purchase "+str(pcount)+'x '+ckpname+' '+"for "+str(ckprice*pcount)+" ?(1=Yes)"))
                        if confirmation==1:
                            checkster2=False
                        else:
                            checkster2cont=False
                            checkster2=False
                    if checkster2cont==False:
                        continue
                    price=price+ckprice*pcount+ckprice*pcount*0.18
                    ckppricelist.append([ckcount,int(ckpbarcode),ckpname,pcount,ckprice,ckprice*pcount,round((ckprice*pcount*0.18),4)])
                    ckcount+=1
                    ans=int(input("Do you want to add another product?(1=Yes)"))
                    print()
                checkster3=True
                while checkster3==True:
                    print("Customer Reciept:")
                    print()
                    print("*"*119)
                    for x in ckppricelist:
                        print('|','%12s'%x[0],'|','%16s'%x[1],'|','%16s'%x[2],'|','%9s'%x[3],'|','%14s'%x[4],'|','%20s'%x[5],'|','%10s'%x[6],'|')
                    print("*"*119)
                    print('Total Price=',round(price,2))
                    print("*"*119)
                    confirmation2=int(input("Do you want to remove any item(s) from this list?(1=No,2=Yes)"))
                    if confirmation2==2:
                        removefromcartitemno=int(input("Enter the item number from the above reciept which you want to discard:"))
                        rckprice=ckppricelist[removefromcartitemno][4]
                        rckpcount=ckppricelist[removefromcartitemno][3]
                        price=price-(rckprice*rckpcount+rckprice*rckpcount*0.18)
                        rem=ckppricelist.pop(removefromcartitemno)
                        print("Removed:",rem,"from cart!")
                        print()
                        for i in range(removefromcartitemno,len(ckppricelist)):
                            ckppricelist[i][0]=i
                    else:
                        checkster3=False
                        print("Customer Reciept:")
                        print()
                        print("*"*119)
                        finalpricelist=[]
                        for x in ckppricelist:
                            print('|','%12s'%x[0],'|','%16s'%x[1],'|','%16s'%x[2],'|','%9s'%x[3],'|','%14s'%x[4],'|','%20s'%x[5],'|','%10s'%x[6],'|')
                            finalpricelist.append(x)
                        else:
                            finalpricelist.pop(0)
                            for x in finalpricelist:
                                reducestockpbarcode(x[1],x[3])
                        print("*"*119)
                        print('Total Price=',round(price,2))
                        # while True:
                        #     try:
                        #         recch=int(input("Would you like to print the reciept?(1=Yes,2=No):"))
                        #         if recch==1:
                        #             try:
                        #                 import os,tempfile
                        #                 filename = tempfile.mktemp(".txt")
                        #                 f=open(filename , "w+")
                        #                 for p in ckppricelist:
                        #                     f.write('|'+'%12s'%x[0]+'|'+'%16s'%x[1]+'|'+'%16s'%x[2]+'|'+'%9s'%x[3]+'|'+'%14s'%x[4]+'|'+'%20s'%x[5]+'|'+'%10s'%x[6]+'|'+'\n')
                        #                 else:
                        #                     f.seek(0)
                        #                     print(f.read())
                        #                     os.startfile(filename, "print")
                        #             except:
                        #                 print("An Error Occurred while printing the receipt.") 
                        #         else:
                        #             break
                        #     except:
                        #         print("Try Again.")
                        print("*"*119)
                        print("\n Thank you for shopping with us, Have a nice day :)")
                        print("*"*119)
                    
def CheckoutByProductBarcode():
                price=0
                print("--------Starting a checkout...--------")
                print("You are now checking out using product barcodes")
                print()
                ans=1  #Boolean True
                ckcount=1
                ckppricelist=[["Item Number","Product Barcode","Product Name","Quantity","Product Price","Total Product Price","18% G.S.T."]]
                while ans==1:
                    print("Product Number:",ckcount)
                    while True:
                        ckpbarcode=input("Enter the product barcode:")
                        comlst=ckpbarcode.split()
                        while comlst[0].lower()=='!search':
                            if comlst[1][0].lower()=='%' or comlst[1][-1].lower()=='%':
                                st="select pbarcode,pname,pprice from products2 where pname like '{}'".format(comlst[1])
                            else:
                                st="select pbarcode,pname,pprice from products2 where pname like '%{}%'".format(comlst[1])
                            curobj.execute(st)
                            res=curobj.fetchall()
                            if len(res)==0:
                                print("No results found.(You can only search product names.)")
                            else:
                                print('*'*60)
                                print('|','%18s'%"Product Barcode",'|','%16s'%"Product Name",'|','%16s'%"Product Price",'|')
                                print('*'*60)
                                for x in res:
                                    print('|','%18s'%x[0],'|','%16s'%x[1],'|','%16s'%x[2],'|')
                                else:
                                    print('*'*60)
                            ckpbarcode=input("Enter the product barcode:")
                            comlst=ckpbarcode.split()
                        try:
                            checkbarcode(ckpbarcode)
                            ckpbarcode=int(ckpbarcode)
                            ckpricest="select pprice,pname from products2 where pbarcode={}".format(ckpbarcode)
                            curobj.execute(ckpricest)
                            ckprice1=curobj.fetchone()
                            ckprice=ckprice1[0]
                            ckpname=ckprice1[1]
                            ckpinvqty=ckprice1[2]
                            break
                        except:
                            print("Invalid product barcode, please try again.")
                    checkster=True
                    while checkster==True:
                        pcount=int(input("How many"+' '+ckpname+' '+"do you want to purchase:"))
                        if pcount>ckpinvqty:
                            print("You cannot purchase more than what stock is available.")
                            continue
                        if pcount<=0 or pcount>env_buylimit:
                            print("You cannot purchase 0, a negative value, or more than",env_buylimit," at once. \n If you want to purchase more than",env_buylimit," items, specify",env_buylimit," here and the rest in another entry.")
                        else:
                            checkster=False
                    print(pcount,'x ',ckpname,"Costs",ckprice,"*",pcount,"=",ckprice*pcount)
                    checkster2=True
                    checkster2cont=True
                    while checkster2==True:
                        confirmation=int(input("Are you sure you want to purchase "+str(pcount)+'x '+ckpname+' '+"for "+str(ckprice*pcount)+" ?(1=Yes)"))
                        if confirmation==1:
                            checkster2=False
                        else:
                            checkster2cont=False
                            checkster2=False
                    if checkster2cont==False:
                        continue
                    price=price+ckprice*pcount+ckprice*pcount*0.18
                    ckppricelist.append([ckcount,int(ckpbarcode),ckpname,pcount,ckprice,ckprice*pcount,round((ckprice*pcount*0.18),4)])
                    ckcount+=1
                    ans=int(input("Do you want to add another product?(1=Yes)"))
                    print()
                checkster3=True
                while checkster3==True:
                    print("Customer Reciept:")
                    print()
                    print("*"*119)
                    for x in ckppricelist:
                        print('|','%12s'%x[0],'|','%16s'%x[1],'|','%16s'%x[2],'|','%9s'%x[3],'|','%14s'%x[4],'|','%20s'%x[5],'|','%10s'%x[6],'|')
                    print("*"*119)
                    print('Total Price=',round(price,2))
                    print("*"*119)
                    confirmation2=int(input("Do you want to remove any item(s) from this list?(1=No,2=Yes)"))
                    if confirmation2==2:
                        removefromcartitemno=int(input("Enter the item number from the above reciept which you want to discard:"))
                        rckprice=ckppricelist[removefromcartitemno][4]
                        rckpcount=ckppricelist[removefromcartitemno][3]
                        price=price-(rckprice*rckpcount+rckprice*rckpcount*0.18)
                        rem=ckppricelist.pop(removefromcartitemno)
                        print("Removed:",rem,"from cart!")
                        print()
                        for i in range(removefromcartitemno,len(ckppricelist)):
                            ckppricelist[i][0]=i
                    else:
                        checkster3=False
                        print("Customer Reciept:")
                        print()
                        print("*"*119)
                        finalpricelist=[]
                        for x in ckppricelist:
                            print('|','%12s'%x[0],'|','%16s'%x[1],'|','%16s'%x[2],'|','%9s'%x[3],'|','%14s'%x[4],'|','%20s'%x[5],'|','%10s'%x[6],'|')
                            finalpricelist.append(x)
                        else:
                            finalpricelist.pop(0)
                            for x in finalpricelist:
                                reducestockpbarcode(x[1],x[3])
                        print("*"*119)
                        print('Total Price=',round(price,2))
                        print("*"*119)
                        print("\n Thank you for shopping with us, Have a nice day :)")
                        print("*"*119)

def updatemodulefun():
            c5=int(input("Press 1 to update a product\'s name \n or 2 to update a product\'s barcode \n or 3 to update a product\'s price:"))
            if c5==1:
                c5i=int(input("Press 1 to update the product \'s name based on it \' s old product name \n or 2 to update it based on it\'s product barcode:"))
                if c5i==1:
                    pname=input("Enter the product\'s current name:")
                    try:
                        pnameupd=input("Enter the updated product name:")
                        pupdatest="update products2 set pname='{}' where pname='{}'".format(pnameupd,pname)
                        curobj.execute(pupdatest)
                        mycon.commit()
                        print("Successfully changed the name of,",pname,"to",pnameupd)
                    except:
                        print("An Error Occured")
                elif c5i==2:
                    pbarcode=input("Enter the product\'s barcode (numeric):")
                    checkbarcode(pbarcode)
                    pbarcode=int(pbarcode)
                    try:
                        pnameupd=input("Enter the updated product name:")
                        pupdatest="update products2 set pname='{}' where pbarcode={}".format(pnameupd,pbarcode)
                        curobj.execute(pupdatest)
                        mycon.commit()
                        print("Successfully changed the name of",pbarcode,"to",pnameupd)
                    except:
                        print("An Error Occured")
                else:
                    print("Incorrect Reply")
            elif c5==2:
                c5i=int(input("Press 1 to update the barcode based on the product \'s name \n or 2 to update based on it\'s current product barcode:"))
                if c5i==1:
                    pname=input("Enter the product\'s name:")
                    try:
                        pbarcodeupd=input("Enter the updated barcode:")
                        checkbarcode(pbarcodeupd)
                        pbarcodeupd=int(pbarcodeupd)
                        pupdatest="update products2 set pbarcode={} where pname='{}'".format(pbarcodeupd,pname)
                        curobj.execute(pupdatest)
                        mycon.commit()
                        print("Successfully changed the barcode of,",pname,"to",pbarcodeupd)
                    except:
                        print("An Error Occured")
                elif c5i==2:
                    pbarcode=input("Enter the product\'s current barcode (numeric):")
                    checkbarcode(pbarcode)
                    pbarcode=int(pbarcode)
                    try:
                        pbarcodeupd=input("Enter the updated product\'s barcode:")
                        checkbarcode(pbarcodeupd)
                        pbarcodeupd=int(pbarcodeupd)
                        pupdatest="update products2 set pbarcode={} where pbarcode={}".format(pbarcodeupd,pbarcode)
                        curobj.execute(pupdatest)
                        mycon.commit()
                        print("Successfully changed the barcode from,",pbarcode,"to",pbarcodeupd)
                    except:
                        print("An Error Occured")
                else:
                    print("Incorrect Reply")                 
            elif c5==3:
                c5i=int(input("Press 1 to update the price based on the product\'s name \n or 2 to update the price based on it\'s product barcode:"))
                if c5i==1:
                    pname=input("Enter the product\'s name:")
                    try:
                        ppriceupd=int(input("Enter the updated product price:"))
                        pupdatest="update products2 set pprice={} where pname='{}'".format(ppriceupd,pname)
                        curobj.execute(pupdatest)
                        mycon.commit()
                        print("Successfully changed the price of",pname,"to",ppriceupd)
                    except:
                        print("An Error Occured")            
                elif c5i==2:
                    pbarcode=input("Enter the product\'s barcode (numeric):")
                    checkbarcode(pbarcode)
                    pbarcode=int(pbarcode)
                    try:
                        ppriceupd=int(input("Enter the updated product price:"))
                        pupdatest="update products2 set pprice={} where pbarcode={}".format(ppriceupd,pbarcode)
                        curobj.execute(pupdatest)
                        mycon.commit()
                        print("Successfully changed the price of the product with barcode,",pbarcode,"to",ppriceupd)
                    except:
                        print("An Error Occured")
                else:
                    print("Incorrect Reply")
            else:
                print("Incorrect Reply")

def DeleteByProductName(pname):
            try:
               pdeletest="delete from products2 where pname='{}'".format(pname)
               curobj.execute(pdeletest)
               mycon.commit()
            except:
               print("Invalid Product Name, Or An Error Occurred")
                
def DeleteByProductBarcode(pbarcode):
            checkbarcode(pbarcode)
            pbarcode=int(pbarcode)
            try:
                pdeletest="delete from products2 where pbarcode={}".format(pbarcode)
                curobj.execute(pdeletest)
                mycon.commit()
            except:
                print("Invalid Product Name, Or An Error Occurred")
                
                
                
                
###############################################################################################
#InventoryModule
def acceptreorderpname(pname,qty):              #increases stock by qty
    exest="UPDATE products2 SET invqty=invqty+{} where pname='{}'".format(qty,pname)
    curobj.execute(exest)
    mycon.commit()
    
def acceptreorderpbarcode(pbarcode,qty):    #increases stock by qty
    pbarcode=str(pbarcode)
    checkbarcode(pbarcode)
    pbarcode=int(pbarcode)
    exest="UPDATE products2 SET invqty=invqty+{} where pbarcode={}".format(qty,pbarcode)
    curobj.execute(exest)
    mycon.commit()

def reducestockpname(pname,qty):            #reduces stock by qty
    exest="UPDATE products2 SET invqty=invqty-{} where pname='{}'".format(qty,pname)
    curobj.execute(exest)
    mycon.commit()
    
def reducestockpbarcode(pbarcode,qty):      #reduces stock by qty
     pbarcode=str(pbarcode)
     checkbarcode(pbarcode)
     pbarcode=int(pbarcode)
     exest="UPDATE products2 SET invqty=invqty-{} where pbarcode={}".format(qty,pbarcode)
     curobj.execute(exest)
     mycon.commit()
     
def displayreordersrequired(minqty):        #displays all items that are in lesser than minqty quantity
    exest="SELECT pname,invqty FROM products2 where invqty<{}".format(minqty)
    curobj.execute(exest)
    resultset=curobj.fetchall()
    print('*'*42)
    print('|','%15s'%'Product','|','%20s'%'Quantity Remaining','|')
    print('*'*42)
    for j in resultset:
        print('|','%15s'%j[0],'|','%20s'%j[1],'|')
    else:
        print('*'*42)











                
