from DBOperation import DBOperation
import sys
import sqlite3 as sql
import pandas as pd
import matplotlib.pyplot as plt
import random 

def main():
    states = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA", "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]
    #declare connection
    databaseData = DBOperation()
    ok = False
    con = sql.connect("climbing.db")
    cur = con.cursor()

    # Input validation 
    while ok != True:
        print('Choose an option:')
        print('a) Load Data')
        print('b) Information about climbing in the US')
        print('c) Visualization of climbing data in the US')
        print('d) Manipulate climbing data')
        print('e) Log-Out')

        choice = str(input())
        if choice.lower() not in ('a', 'b', 'c', 'd', 'e'):
            print("Not an appropriate choice.")
            ok = False
        
        else:
            # main_menu = True
            # while ok != True:
            if choice == "a":
                print('loading data....')
                databaseData.loadData()

            #find routes
            elif choice.lower() == "b":
                state = input("enter location (use abbreviation): \n")
                state = state.upper()
                while state not in states:
                    state = input("enter location (use abbreviation): \n")
                    state = state.upper()

                print('number of crags:')
                crags =  f"SELECT count(area.Crags) FROM area JOIN climb ON area.ST = climb.ST WHERE area.ST = '{state}';"
                cur.execute(crags)
                print(cur.fetchone()[0])

                print('number of climbs:')
                climbs =  f"SELECT SUM(state.num) FROM state JOIN climb ON state.ST = climb.ST WHERE state.ST = '{state}';"
                cur.execute(climbs)
                print(cur.fetchone()[0])  

                print('number of trad, sport, and boulder routes:')
                climb_type =  f"SELECT SUM(Trad), SUM(Sport), SUM(Boulder) FROM climb WHERE ST = '{state}';"
                cur.execute(climb_type)
                print(cur.fetchone())  

                print('largest crag in state:')
                largest_crag =  f"SELECT MAX(Climbs), Crags FROM area WHERE ST = '{state}';"
                cur.execute(largest_crag)
                print(cur.fetchone())

                specific = input('specific query y/n? (using WHERE)')
                if specific.lower() == 'y':
                    data = input("Climbs, Crags, Aid, Alpine, Boulder, Ice, Mixed, Sport, Toprope, Trad: \n")
                    try:
                        specific_query =  ("SELECT climb.'%s' FROM climb WHERE climb.ST = '%s'" % (data, state))
                        cur.execute(specific_query)
                        print(cur.fetchone()[0])
                    except:
                        print('does not exist')
                
            #graph
            elif choice.lower() == "c":
                choice = input('Enter (s) to graph state data and (c) to enter countrywide data: ')
                
                # bar graph 
                if choice.lower() == "s":
                    graphChoice = input("Enter the state you'd like to Graph(use abbreviation): ")
                    graphChoice = graphChoice.upper()
                    while graphChoice not in states:
                        graphChoice.upper()
                        graphChoice = input("Enter the state you'd like to Graph (use abbreviation): ")
                    query = f"SELECT ST, type, num FROM state WHERE ST = '{graphChoice}'"
                    data = pd.read_sql(query, con)
                    plt.bar(data.type, data.num)
                    title = "Climbing data in " , str(graphChoice)
                    plt.xlabel("Type of Climbs")
                    plt.ylabel("Number of Climbs")
                    plt.title(label = title,
                    fontsize = 40)
                    plt.show()

                # scatter plot 
                elif choice.lower() == "c":
                    query = f"SELECT ST, Climbs FROM climb"
                    data = pd.read_sql(query, con)
                    plt.scatter(data.ST, data.Climbs)
                    plt.show()

            #change
            elif choice == "d":
                edit = input('enter (c) to change, (i) to insert, or (d) to delete:')

                #update data
                if edit.lower() == 'i':
                    crag = input("enter a new crag:")
                    climb_num = input('enter a new number of climbs:')
                    location = input('enter a new state:')
                    change = f"INSERT INTO area (Numb, Crags, Climbs, ST) VALUES ('{random.randint(1,10000)}', '{crag}', '{climb_num}', '{location}');"
                    cur.execute(change)
                    print('done')
                    con.commit()
                    final =  f"SELECT * FROM area WHERE area.Crags = '{crag}';"
                    cur.execute(final)
                    print(cur.fetchall())

                #change data
                elif edit.lower() == 'c':
                    table = input("which table would you like to change?\n")
                    column = input("which column would you like to change?\n")
                    old_val = input('which value?')
                    new_value = input("enter a new value:")
                    change = f"UPDATE '{table}' SET '{column}' = '{new_value}' WHERE '{table}'.'{column}' = '{old_val}';"
                    cur.execute(change)
                    print('done')
                    con.commit() 
                    final =  f"SELECT * FROM '{table}' WHERE '{table}'.'{column}' = '{new_value}';"
                    cur.execute(final)
                    print(cur.fetchall())

                #delete 
                elif edit.lower() == 'd':
                    table = input("which table would you like to delete from?\n")
                    column = input("which column would you like to delete?\n")
                    record = input("which value would you like to delete?\n")
                    change = f"DELETE FROM '{table}' WHERE '{table}'.'{column}' = '{record}';"
                    cur.execute(change)
                    print('deleted')
                    con.commit() 


            #logout
            elif choice.lower() == 'e':
                print('goodbye')
                ok == True
                sys.exit()
            
            else:
                again = input("try again? (y/n): ")
                if again == 'n':
                    print("goodbye")
                    ok == False
                    sys.exit()
                
    # Query to find climbing routes 
    
main()
