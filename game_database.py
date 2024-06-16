import os
import csv
from tabulate import tabulate

games = []

####################### READ AND WRITE FILES #####################

def read_games_file(): #opens file and creates one if required
    try:
        with open('games.csv', 'r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                games.append(row)
    except FileNotFoundError:
        pass # Prevents an error and just shows blank on user request

def save_games_file():
    with open('games.csv', 'w', newline = '') as file: #opens file in append mode
        fieldnames = ['Game Name', 'Platform', 'Completion Status']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(games)
            
####################### VIEW GAMES #########################

def search_games():
    print("You may search for either a game title or  platform. \n")
    search_for = input("Enter the game or platform you wish to search for: ")
    
    with open('games.csv', 'r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)
        data = [row for row in csv_reader if search_for.lower() in row[0].lower() or search_for.lower() in row[1].lower()]
        if data:
            print("Search results: \n")
            print(tabulate(data,headers=["Game Name", "Platform", "Completion Status"], tablefmt="grid"))
        else:
            print("No results found.")

def view_all_games():
    with open('games.csv', 'r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader) #skips first line as contains headers
        data = [row for row in csv_reader] #contents of csv file stored in variable
        data.sort(key=lambda x: x[0]) #sorts entries by alphabtical order from row 0
        #use the tabulate module to display games in a more readable format
        print(tabulate(data, headers=["Game Name", "Platform", "Completion Status"], tablefmt="grid"))

def view_complete_games():
    with open('games.csv', 'r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader) #skips first line as contains headers
        #stores only entries that have 'complete' in row[2]
        data = [[row[0], row[1]] for row in csv_reader if row[2].lower() == 'complete']
        data.sort(key=lambda x: x[0]) #sorts entries by alphabtical order from row 0
        #use the tabulate module to display games in a more readable format
        print(tabulate(data, headers =["Game Name", "Platform"], tablefmt="grid"))

def view_incomplete_games():
    with open('games.csv', 'r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader) #skips first line as contains headers
        #stores only entries that have 'incomplete' in row[2]
        data = [[row[0], row[1]] for row in csv_reader if row[2].lower() == 'incomplete']
        data.sort(key=lambda x: x[0]) #sorts entries by alphabtical order from row 0
        #use the tabulate module to display games in a more readable format
        print(tabulate(data, headers=["Game Name", "Platform"],tablefmt="grid"))

def view_multiplayer_games():
    with open('games.csv', 'r')as file:
        csv_reader = csv.reader(file)
        next(csv_reader) #skips first line as contains headers
        #stores only entries that have 'multiplayer' in row[2]
        data = [[row[0], row[1]] for row in csv_reader if row[2] == 'multiplayer']
        data.sort(key=lambda x: x[0]) #sorts entries by alphabtical order from row 0
        #use the tabulate module to display games in a more readable format
        print(tabulate(data, headers =["Game Name", "Platform"], tablefmt="grid"))

####################### ADD GAMES ##########################

def duplication_check(game_name, platform):
    # Check if the game already exists
    with open('games.csv', 'r')as file:
        csv_reader = csv.reader(file)
        next(csv_reader) #skip first line as contains headers
        for row in csv_reader:
            if row[0].lower() == game_name.lower() and row[1].lower() == platform.lower():
                return True #Duplicate found
    return False # No duplicate found

def add_games():
    while True:
        while True:#get details from the user
            game_name = input("\n Please type name of the game: ")
            platform = input("\n Please type the platform this game runs on: ")
            status = input("\n What is the status of this game? \n\n Please type 'complete', 'incomplete' or 'multiplayer' \n\n Status: ").lower()
            if status in ['complete', 'incomplete', 'multiplayer']: # checks only peritted status is entered
                break
            else:
                print("Incorrect status. Please use one the following: 'Complete', 'Incomplete' or 'Multiplayer'")
        
        if not duplication_check(game_name, platform): #call function to check for duplicates
            games.append({'Game Name' : game_name, 'Platform': platform, 'Completion Status': status})
            print("\n Game added! \n")
            save_games_file()
        else:
            print("\n This game already exists. \n")
                        
        add_another = input("\n Do you wish to add another game? (y/n)").lower()
        if add_another != "y":
            break

    

####################### CHANGE GAMES #######################

def change_game_status():
    print("\n CHANGE A GAME'S STATUS\n\n")
    #get user details of game that requires changing
    game_change = input("Enter the name of the game whose status you wish to change: ")
    platform_change = input("Enter the game's platform: ")
    #check the game exists
    found = False
    for game in games:
        if game['Game Name'].lower() == game_change.lower() and game['Platform'].lower() == platform_change.lower():
            found = True
            print("Found the following game: \n")
            #display the game found
            print(tabulate([[game['Game Name'], game['Platform'],game['Completion Status']]], headers=["Game Name", "Platform", "Completion Status"], tablefmt='grid'))
            #check with user they wish to make changes to this game
            confirm = input("Do you wish to make changes to status of this game? y/n: ")
            if confirm == 'y':
                # Provide options for changing the status
                new_status = input("Enter the new status for the game (complete/incomplete/multiplayer): ").lower()
                if new_status in ['complete', 'incomplete', 'multiplayer']:
                    # Update the status of the game
                    game['Completion Status'] = new_status
                    print("\nGame status updated successfully.")
                else:
                    print("\nIncorrect status. Please use one of the following: 'complete', 'incomplete', or 'multiplayer'.")
            else:#game will not be deleted
                print("\n Game status change has been cancelled.")
            break
    if not found:
        print("\n Game not found. ")
        
    save_games_file()
                

def delete_game(): 
    print("\n DELETE A GAME\n\n")
    #get user deatils of game to be deleted
    game_delete = input("Enter the name of the game you wish to delete: ")
    platform_delete = input("Enter the platform of the game you wish to delete: ")
    #check the game exists
    found = False
    for game in games:
        if game['Game Name'].lower() == game_delete.lower() and game['Platform'].lower() == platform_delete.lower():
            found = True
            print("\n Found the following game for deletion: ")
            #display the game found
            print(tabulate([[game['Game Name'], game['Platform'],game['Completion Status']]], headers=["Game Name", "Platform", "Completion Status"], tablefmt='grid'))
            #check with user theu wish to delete this game
            confirm = input("Do you wish to delete this game? y/n: ")
            if confirm == 'y':
                games.remove(game)
                print("\n Game has been deleted succesfully")
            else:#game will not be deleted
                print("\n Game deletion has been cancelled.")
            break
    if not found:
        print("\n Game not found. ")
        
    save_games_file()


####################### SUB MENUS ##############################

def view_games_sub_menu(): ############## SUB MENU VIEW GAMES ###################
    while True:
        #View games sub menu
        print("\n WELCOME TO VIEW GAMES")
        print("\n The following options are available: \n")
        print("\n 1. Search for a specific game \n 2. View All Games \n 3. View All Completed Games \n 4. View All Incomplete Games \n 5. View All Multiplayer Games \n 6. Return to Main Menu")
        
        view_selection = input ("\n \n Please make a selection (1-6) : ")
        if view_selection == "1":
            # Call search game function
            search_games()
        elif view_selection == "2":
            # Call view all games function
            view_all_games()
        elif view_selection == "3":
            #Call view completed games function
            view_complete_games()
        elif view_selection == "4":
            #Call view incomplete games function
            view_incomplete_games()
        elif view_selection == "5":
            #Call view multiplayer games functions
            view_multiplayer_games()
        elif view_selection == "6":
            #return to main menu
            break
        else:
            print("\n Please make a valid selection \n \n ")
            continue
        

def change_game_sub_menu(): ###################### SUB MENU CHANGE GAMES #####################
     while True:
        #View games sub menu
        print("\n WELCOME TO MAKE CHANGES TO GAMES")
        print("\n The following options are available: \n")
        print("\n 1. Make Change to a Game's Status \n 2. Add New Games \n 3. Delete Games \n 4. Return to Main Menu")
        
        view_selection = input ("\n \n Please make a selection (1-6) : ")
        if view_selection == "1":
            # Call change status function
            change_game_status()
        elif view_selection == "2":
            # Call add games function
            add_games()
        elif view_selection == "3":
            # Call delete games function
            delete_game()
        elif view_selection == "4":
            # Return to main menu
            break
        else:
            print("\n Please make a valid selection \n \n ")
            continue

def options_sub_menu():
    pass

####################### MAIN PROGRAM ############################

if __name__ == "__main__": 
    read_games_file()
    
    while True:
                
        # Main Menu
        print("\n \n WELCOME TO MY GAMES DATABASE")
        print("\n The following options are available: \n")
        print("\n 1. View Games in Database \n 2. Make Changes to Games Database \n 3. Options \n 4. Exit app")
    
        selection = input("\n\n Please make a selection (1-4) : ")
        if selection == "1":
            # Call view games sub menu function
            view_games_sub_menu()
        elif selection == "2":
            # Call make changes sub menu function
            change_game_sub_menu()
        elif selection == "3":
            # Call options sub menu function ############# functions and sub menu undefined##############
            pass
        elif selection == "4":
            #exit the app
            save_games_file()
            exit()
        else:
            print("\n Please make a valid selection \n\n")
            continue