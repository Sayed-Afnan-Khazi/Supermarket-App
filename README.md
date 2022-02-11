# Supermarket-App
My first ever large scale project- A comprehensive Supermarket POS, stock management and employee management application! \
This project was my submission for the end of high school CS project. \
This project was coded in python and interfaced with MySQL for database management.
# How to start?
## Pre-requisites:
The repository contains extra files that are all needed for the app to run. \
Please ensure you have MySQL 8.0+ and Python 3.7+ before starting up. 
## Setting up the application:
Upon running the main script, you will be prompted to enter your MySQL credentials. \
After that, please use the given Admin login ID and password for initial setup. \
Follow the onscreen instructions to automatically setup the database, tables and the optional (Sample Products) initial data.  
# MySQL Database:
The database ("supermarketapp") contains two tables- 
* products2 - 
  * Product Name: pname -> varchar(50) 
  * Product Barcode: pbarcode -> double, primary key (unique values only) 
  * Product Price: pprice -> float 
  * Product Inventory Quantity: invqty -> integer, default value =0 
* employee2 - 
  * Employee Number: enum -> integer, Primary Key (Unique values only) 
  * Employee Name: ename -> varchar(50) 
  * Employee Login Username: eusername -> varchar(50) 
  * Employee Login Password: epassword -> varchar(50) 
  * Employee Salary: salary -> float 
  * Employee Bonus: bonus -> float
# Python Files:
* CompiledSupermarketAppV1.97.py -
  * This file is the main script that you need to run in order to run the application.
  * It is a short script creating the main menu and integrating the other modules together.
* SupermarketappAdminModule,py -
  * This file contains the main login interface, setup of application and all employee, product and stock management features.
  * This script is run when you enter option 1 in the main script.
* SupermarketappFunctionsModule.py -
  * This file contains all the functions that make the application work.
  * It contains a seperate section at the end where the stock/inventory management functions are defined.
# Additional Files:
* supermarketappconfiginfo.bin -
  * Stores MySQL login information and the hardlimit maximum number of purchases per item per checkout entry.
  * Upon the start of the main script, the script retrieves data from this file and uses it to login to the MySQL server.
  * If the login was unsuccessful, the script will try to ask the user to input the updated credentials to overwrite this file.
* ProfileManager.bin -
  * Stores profile/employee data, the login system is based on retrieving data from this file.
* attendancelogs.csv -
  * Stores employee attendance tag-ins and tag-outs as seperate lines
  * Lines are stored in chronological order of tag-ins/outs
 
(Future me, please type more info about the features here)
# Bug Report:
Please raise any issues you find in issues
