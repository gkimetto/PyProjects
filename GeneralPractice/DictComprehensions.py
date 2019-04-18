def main():
    ctemps = [0, 12, 34, 100]
    tempDict = {t: (t*9/5)+32 for t in ctemps if t <100}
    print(tempDict)
    print(tempDict[12])
    # Use comprehensions to build a dictionary
    
    team1 = {"Jones":24, "Jameson":18, "smith":58, "Burns":7}
    team2 = {"White": 12, "Macke": 88, "Perce":4}
    # Merge the 2 dictionaries
    # Linit to 2 expressions
    
    newTeam = {k:v for team in (team1, team2) for k,v in team.items()}
    print(newTeam)
if __name__ == "__main__":
    main()