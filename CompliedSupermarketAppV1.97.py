# -*- coding: utf-8 -*-
"""
Created on Sun Nov 29 15:43:27 2020

@author: Sayed Afnan Khazi
"""
#####SUPERMARKET COMPLETE APPLICATION V1.97 Build 17 May 2021#####
#####Compiling 2 Modules into a User Interface
#####Made by Afnan

import SupermarketappFunctionsModule as a
import SupermarketappAdminModule as m
while True:
    try:
        print("*************************************************************")
        print("*****WELCOME TO PAS SUPERMARKET MANAGEMENT APPLICATION!******")
        print("*************************************************************")
        print()      #This program has over 30++ options of features, 1000+ lines of code
        print("\t Press 1 to open the administrative menu(Login,attendance,profile management, product management, etc.)")
        print("\t Press 2 to start billing")
        print("\t Press 3 to exit the program")
        print()
        print("NOTE: Press 1 for initialization and application setup")
        print()
        print("*************************************************************")
        choice=int(input("Enter an option:"))
        if choice==3:
            break
        elif choice==1:
            try:
                m.AdministrativeMode()          #COMPLETE MODULE FUNCTION CALL
            except:
                print("An Error Occurred in the Admin Module(AMError)")
        elif choice==2:
            while True:
                print("*************************************************************")
                print("*****Welcome to billing mode*****")
                print("*************************************************************")
                print()
                print("\t Press 1 to checkout using product names")
                print("\t Press 2 to checkout using product barcodes")
                print("\t Press 3 to find the price of a product")
                print("\t Press 4 to go back")
                print()
                print("*************************************************************")
                checkoutchoice=int(input("Enter an option:"))
                if checkoutchoice==1:
                    try:
                        print("*************************************************************")
                        a.CheckoutByProductName()
                    except:
                        print("Invalid Product Name/An Error Occurred")
                elif checkoutchoice==2:
                    try:
                        print("*************************************************************")
                        a.CheckoutByProductBarcode()
                    except:
                        print("Invalid Product Barcode/An Error Occurred")
                elif checkoutchoice==4:
                    break
                elif checkoutchoice==3:
                    while True:
                        try:
                            print("*************************************************************")
                            print("*****Welcome to price checking mode*****")
                            print("*************************************************************")
                            print()
                            print("\t Press 1 to check the price using the product name")
                            print("\t Press 2 to check the price using the product barcode")
                            print("\t Press 3 to go back")
                            print()
                            print("*************************************************************")
                            pricecheckchoice=int(input("Enter an option:"))
                            if pricecheckchoice==1:
                                pname=input("Enter the product's name:")
                                a.SearchPriceByProductName(pname)
                            elif pricecheckchoice==2:
                                pbarcode=input("Enter the product barcode:")
                                a.checkbarcode(pbarcode)
                                pbarcode=int(pbarcode)
                                a.SearchPriceByProductBarcode(pbarcode)
                            elif pricecheckchoice==3:
                                break
                        except:
                            print("An Error Occurred while retrieving product prices(PPError)")
    except:
        print("An Error Occurred: Error Code: wError1")   # an error in the wide program, i.e. the module compiler         
                