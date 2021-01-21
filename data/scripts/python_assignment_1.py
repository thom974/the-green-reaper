# Author: Thomas Luc
# Date: January 21, 2021
# File Name: python_assignment_1.py
# Description: assignment for TEJ3M containing all questions, from 1-3

print('This program implements the appropriate functionality as per the Python Assignment doc.')
# Display menu options
print('   MENU')
print('==========')
print('S to start')
print('H for help')
print('==========')
print(' ')
choice = input('Option?: ')     # get user's choice

if choice == 'H':
    print('This program will ask you certain inputs. Answer the prompts appropriately.')
elif choice == 'S':
    # first question
    user_num = int(input("enter in an integer: "))  # ask user for number and store in variable
    condition_1, condition_2 = '', ''  # declare two variables storing the two conditions we are checking for (even/odd, +/-/0)

    # check for first condition
    if user_num % 2 == 0:  # if the remainder is 0 when user_num is divided by 2, it must be even
        condition_1 = 'even'  # set condition_1 to 'even' so that we can format this value later
    else:
        condition_1 = 'odd'  # if the remainder is not 0 the number is odd, so set condition_1 to 'odd'

    # check for second condition
    if user_num > 0:  # if the number is greater than 0 it is positive.
        condition_2 = 'positive'  # change condition_2 to 'positive'
    elif user_num < 0:  # otherwise, if the number is less than 0, it is negative.
        condition_2 = 'negative'
    else:
        condition_2 = '0'

    print("your number is %s. it is %s" % (condition_1, condition_2))  # use string formatting to print results

    # second question
    year = int(input('enter in a year '))
    is_leap_year = ''
    if year % 4 == 0:  # first step. checks if year is evenly divisible by 4.
        if year % 100 == 0:  # second step. checks if year is evenly divisible by 100.
            if year % 400 == 0:  # third step. checks if year is evenly divisible by 400.
                is_leap_year = 'yes'
            else:  # executes when the year is not evenly divisible by 400.
                is_leap_year = 'no'
        else:  # executes when the year is not evenly divisible by 100.
            is_leap_year = 'yes'
    else:  # executes when the year is not evenly divisible by 4.
        is_leap_year = 'no'

    print('is the year %d a leap year? %s' % (year, is_leap_year))  # use string formatting to print results

    # third question
    birthdate = input("Enter your birthday in this form e.g (September 23): ").split()  # store user input in a list.
    month, day = birthdate[0], int(
        birthdate[1])  # assign 0th index to var 'month'. assign 1st index to var 'day' and convert to int.

    if month == "January":  # this entire if-elif block first determines what month the user inputted
        if day < 20:  # each month contains two signs. the program then checks if the day entered is less or equal to than the point where the astrological sign changes.
            print("Capricorn")
        else:  # if the first condition is not satisfied then this executes. the sign must be the other of the two.
            print("Aquarius")
    elif month == "February":  # this process continues, checking each month, then date.
        if day < 19:
            print("Aquarius")
        else:
            print("Pisces")
    elif month == "March":
        if day <= 20:
            print("Pisces")
        else:
            print("Aries")
    elif month == "April":
        if day < 20:
            print("Aries")
        else:
            print("Taurus")
    elif month == "May":
        if day <= 20:
            print("Taurus")
        else:
            print("Gemini")
    elif month == "June":
        if day <= 21:
            print("Gemini")
        else:
            print("Cancer")
    elif month == "July":
        if day < 23:
            print("Cancer")
        else:
            print("Leo")
    elif month == "August":
        if day < 23:
            print("Leo")
        else:
            print("Virgo")
    elif month == "September":
        if day <= 22:
            print("Virgo")
        else:
            print("Libra")
    elif month == "October":
        if day <= 23:
            print("Libra")
        else:
            print("Scorpio")
    elif month == "November":
        if day < 22:
            print("Scorpio")
        else:
            print("Sagitarius")
    elif month == "December":
        if day <= 21:
            print("Sagitarius")
        else:
            print("Capricorn")
    else:
        print('you entered an invalid date.')
else:
    print('Not a valid choice. Only S and H are valid choices')
