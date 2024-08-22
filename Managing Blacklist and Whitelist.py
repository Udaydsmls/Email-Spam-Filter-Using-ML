import pickle


def read_blacklist():
    with open("blacklist.pkl", "rb") as f:
        blacklist = pickle.load(f)
    return blacklist


def read_whitelist():
    with open("whitelist.pkl", "rb") as f:
        whitelist = pickle.load(f)
    return whitelist


def remove_blacklist(string):
    blacklist = read_blacklist()
    if string in blacklist:
        index = blacklist.index(string)
        blacklist.pop(index)
    with open("blacklist.pkl", "wb") as f:
        pickle.dump(blacklist, f)


def remove_whitelist(string):
    whitelist = read_whitelist()
    if string in whitelist:
        index = whitelist.index(string)
        whitelist.pop(index)
        blacklist = read_blacklist()
        blacklist.append(string)
        with open("blacklist.pkl", "wb") as f:
            pickle.dump(blacklist, f)
    with open("whitelist.pkl", "wb") as f:
        pickle.dump(whitelist, f)


def add_whitelist(string):
    whitelist = read_whitelist()
    blacklist = read_blacklist()
    if string in blacklist:
        remove_blacklist(string)
    if string not in whitelist:
        whitelist.append(string)
        with open("whitelist.pkl", "wb") as f:
            pickle.dump(whitelist, f)


def add_blacklist(string):
    blacklist = read_blacklist()
    whitelist = read_whitelist()
    if string in whitelist:
        remove_whitelist(string)
    elif string not in blacklist:
        blacklist.append(string)
        with open("blacklist.pkl", "wb") as f:
            pickle.dump(blacklist, f)


while True:
    # Removing from Whitelist will automatically add to Blacklist
    # Same is not true for Removing from Blacklist
    print("\n1. Read Blacklist")
    print("2. Read Whitelist")
    print("3. Remove From Blacklist")
    print("4. Remove from Whitelist")
    print("5. Add to Whitelist")
    print("6. Add to Blacklist\n")
    choice = int(input())

    if choice == 1:
        print(read_blacklist())
    elif choice == 2:
        print(read_whitelist())
    elif choice == 3:
        string = input('Enter a valid email: ')
        remove_blacklist(string)
        print('Operation Completed')
    elif choice == 4:
        string = input('Enter a valid email: ')
        remove_whitelist(string)
        print('Operation Completed')
    elif choice == 5:
        string = input('Enter a valid email: ')
        add_whitelist(string)
        print('Operation Completed')
    elif choice == 6:
        string = input('Enter a valid email: ')
        add_blacklist(string)
        print('Operation Completed')
    else:
        print("Enter valid choice.....")
