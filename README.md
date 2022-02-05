# Supermarket-App
My first ever large scale project- A comprehensive Supermarket POS, stock management and employee management application!
This project was my submission for the end of high school CS project.
This project was coded in python and interfaced with MySQL for database management
# How to start?
# Pre-requisites:
The repository contains extra files that are all needed for the app to run.
Please ensure you have MySQL 8.0+ and Python 3.7+ before starting up.
# Setting up the application:
Upon running the main script, you will be prompted to enter your MySQL credentials.
After that, please use the given Admin login ID and password for initial setup.
Follow the onscreen instructions to automatically setup the database, tables and the optional initial data (Sample Products)
# MySQL Database:
The database ("supermarketapp") contains two tables- \n
products2 - \n
\t  Product Name: pname -> varchar(50)
\t  Product Barcode: pbarcode -> double, primary key (unique values only)
\t  Product Price: pprice -> float
\t  Product Inventory Quantity: invqty -> integer, default value =0
employee2 - \n
\t  Employee Number: enum -> integer, Primary Key (Unique values only)
\t  Employee Name: ename -> varchar(50)
\t  Employee Login Username: eusername -> varchar(50)
\t  Employee Login Password: epassword -> varchar(50)
\t  Employee Salary: salary -> float
\t  Employee Bonus: bonus -> float
 
(Future me, please type more info about the tables and features here)
# Bug Report:
Please raise any issues you find in issues
