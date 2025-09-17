# design_project.py
# ENDG 233 F24
# STUDENT NAME(S): Youssef Ibrahim, David Caranay
# GROUP NAME: T1 
# A terminal-based data analysis and visualization program in Python.
# You must follow the specifications provided in the project description.
# Remember to include docstrings and comments throughout your code.

import user_csv # File for reading and writing on .csv files
import numpy as np
import matplotlib.pyplot as plt

"""
Instead of being assigned at the start, the .csv file variables
are instead called in their own functions due to being able
to be changed (champion_tierlist in particular)
"""

# Functions

def champ_tier(champion, role, include_headers):
    """Provides the selected champion's role, position and tier. 
    If the champion is not found, allows user to add their own champion to the file.
    
    Parameters:
        champion (str): a champion from the list
        role (str): a role from the list
        include_headers (bool): if headers should be included

    Returns:
        Champion data if they are found, if not prompts user to add their own and add them to the list.
    """
    champion_tierlist = np.array(user_csv.read_csv("data_files/Champion_Tierlist.csv", include_headers))
    if include_headers:
        print(f"{champion_tierlist[0][0]}\t\t{champion_tierlist[0][1]}\t\t{champion_tierlist[0][2]}\t\t{champion_tierlist[0][3]}") # we get here
    for entry in champion_tierlist:
        if (entry[0].lower() == champion.lower()) and (entry[2].lower() == role.lower()):
            print(f"{entry[0]}\t\t{entry[1]}\t\t{entry[2]}\t\t{entry[3]}")
            return

    # If query is not found in file
    print("Champion not found in that role.")
    query = input("Would you like to add this champion and role to the tier list? (Y/N)")
    if query.lower() == "y" or query.lower() == "yes":

        # Ask for missing info: champion class and tier
        new_line = [champion, "Class", role, "Tier"]
        new_line[1] = input("Enter the champions class:")
        new_line[3] = input("Enter the champions tier:").upper()

        # Create a new line, then write the info for the new champion.
        user_csv.write_csv("data_files/Champion_Tierlist.csv","\n",False)
        # For every entry in the line that is being written
        for entry in new_line:
            # Overwrite is "False" so it appends the champion to the file
            user_csv.write_csv("data_files/Champion_Tierlist.csv",str(entry + ","),False)

def champ_performance(champion, role, include_headers):
    """Prints the selected champion's average score, change in winrate from last season, and average KDA ratio in selected role.
    
    Parameters:
        champion (str): a champion from the list
        role (str): a role from the list
        include_headers (bool): if headers should be included
    """
    champion_performance = np.array(user_csv.read_csv("data_files/Champion_Performance.csv", include_headers))

    if include_headers:
        print(f"{champion_performance[0][0]}\t\t{champion_performance[0][1]}\t\t{champion_performance[0][2]}\t\t{champion_performance[0][3]}\t\t{champion_performance[0][4]}") # we get here
    for entry in champion_performance:
        if (entry[0].lower() == champion.lower()) and (entry[1].lower() == role.lower()):
            print(f"{entry[0]}\t\t{entry[1]}\t\t{entry[2]}\t\t{entry[3]}\t\t{entry[4]}")
            return
    print("Champion not found in that role.")

def champ_percentages(champion, role, include_headers):
    """Prints selected champion in the selected role's
     average win, role, pick, and ban percentages.
    
    Parameters:
        champion (str): a champion from the list
        role (str): a role from the list
        include_headers (bool): if headers should be included
    """
    champion_percentages = np.array(user_csv.read_csv("data_files/Champion_Percentages.csv", include_headers))
    if include_headers:
        print(f"{champion_percentages[0][0]}\t{champion_percentages[0][1]}\t{champion_percentages[0][2]}\t{champion_percentages[0][3]}\t{champion_percentages[0][4]}\t{champion_percentages[0][5]}") # we get here
    for entry in champion_percentages:
        if (entry[0].lower() == champion.lower()) and (entry[1].lower() == role.lower()):
            print(f"{entry[0]}\t{entry[1]}\t{float(entry[2])*100}\t{float(entry[3])*100}\t{float(entry[4])*100}\t{float(entry[5])*100}")
            return
    print("Champion not found in that role.")

def role_rates(role, include_headers):
    """Finds and prints the champion with the lowest and highest win-rate in the selected role.

    Parameters:
        role (str): a champion role from the list
        include_headers (bool): if headers should be included
    """
    champion_percentages = np.array(user_csv.read_csv("data_files/Champion_Percentages.csv", include_headers))
    winrates_list = []
    champ_name = ""

    # Creating a list from all of the champion win-rates
    for champion in champion_percentages:
        if champion[1].lower() == role.lower():
            winrates_list += [float(champion[2])]

    # Finding maximum winrate among champions
    maximum_winrate = np.max(np.array(winrates_list))
    for champion in champion_percentages:
        if (champion[1].lower() == role.lower()) and (float(champion[2]) == maximum_winrate):
            champ_name = champion[0]

    print(f"The champion with the highest winrate in {role.upper()} is {champ_name} with a win-rate of {maximum_winrate*100}%")

    # Finding minimum winrate among champions
    minimum_winrate = np.min(np.array(winrates_list))
    for champion in champion_percentages:
        if (champion[1].lower() == role.lower()) and (float(champion[2]) == minimum_winrate):
            champ_name = champion[0]

    print(f"The champion with the lowest winrate in {role.upper()} is {champ_name} with a win-rate of {minimum_winrate*100}%")




def role_statistics(role, include_headers):
    """Creates a scatter graph of pickrate to winrate 
    and a histogram of champion tiers in the provided role.
    
    Parameters:
        role (str): a role from the list
    
    Returns:
        A scatter graph of the winrate of champions in relation to their pickrate in the selected role.
        The other graph is a bar graph of the amount of champions in each tier in the selected role.
        The graphs are then saved to a png file.
    """

    # Getting two .csv files to read
    champion_percentages = user_csv.read_csv("data_files/Champion_Percentages.csv", include_headers)
    champion_tierlist = user_csv.read_csv("data_files/Champion_Tierlist.csv", False)

    plt.figure(figsize = (20, 10)) # create and set the size of the figure
    play_rates = [] # scatter x axis
    win_rates = [] # scatter y axis
    champion_tiers = [] # histogram

    print("Generating graphs...")
    # Adding champion play and win rates from role to their lists
    for champion in champion_percentages:
        if champion[1].lower() == role.lower():
            # To get percentages, we multiply decimals by 100
            play_rates += [float(champion[4])*100]
            win_rates += [float(champion[2])*100]

    # Adding champion tiers from the role to the list
    for champion in champion_tierlist:
        if champion[2].lower() == role.lower():
            champion_tiers += [champion[3]]
    
    # Champion playrate vs winrate scatter
    plt.subplot(1, 2, 1)
    plt.scatter(play_rates, win_rates)
    plt.xlabel("Champion Play-rate (%)")
    plt.ylabel("Champion Win-rate (%)")
    plt.title("Play rates vs. Win rates for the " + role + " role")

    # Champion tier histogram
    plt.subplot(1,2,2)
    plt.title("Number of champions per role for the " + role + " role")
    plt.xlabel("Champion tier")
    plt.ylabel("Number of entries")
    plt.hist(champion_tiers, color = "Red")

    # Saving the graphs to the final_plots folder
    print("Graphs saved to final_plots folder.")
    plt.savefig("final_plots/champion_graphs.png") 

    print("Displaying graphs...")
    # Display the graph. "block = False" means the program continues
    plt.show(block = False)

def print_options():
    """Prints out a list of options to choose from and waits for user input

    Returns:
        chosen_option (int): The entered number selection of the user
    """
    chosen_option = int(input("\nPlease choose an option.\n\t1. View champion tier in role\n\t2. View champion win rate, ban rate, pick rate in role\n\t3. View champion's average match performance stats in role\n\t4. Find weakest and strongest champion in chosen role (win-rate wise)\n\t5. View graphs for role statistics\n\t6. Exit\n\t>> "))
    return chosen_option

# Main Function

print(f"Welcome to the League of Legends Season 13 Champion Database!")

while True: # Program continues until user exits
    chosen_option = print_options()

    if (chosen_option == 1): # Champion Tier
        champion = input("Please enter a champion: ")
        role = input("Please enter a role that champion is played in. (Top, Mid, Support, Jungle, ADC): ")
        champ_tier(champion,role,True)
    elif (chosen_option == 2): # Champion Percentage
        champion = input("Please enter a champion: ")
        role = input("Please enter a role that champion is played in. (Top, Mid, Support, Jungle, ADC): ")
        champ_percentages(champion,role,True)
    elif (chosen_option == 3): # Champion Match Statistics
        champion = input("Please enter a champion: ")
        role = input("Please enter a role that champion is played in. (Top, Mid, Support, Jungle, ADC): ")
        champ_performance(champion,role,True)
    elif (chosen_option == 4): # Prints champion with highest and lowest winrate in the role
        role = input("Please enter a role. (Top, Mid, Support, Jungle, ADC): ")
        role_rates(role,True)
    elif (chosen_option == 5): # "Role Statistics" graphs: scatter and histogram
        role = input("Please enter a role. (Top, Mid, Support, Jungle, ADC): ")
        role_statistics(role, True)
    elif (chosen_option == 6): # Exits program by breaking loop
        print("Exiting...")
        break
    else: # If an invalid selection is entered
        print("Invalid option selected.")
    
    # Divider
    print("\n============================================================")