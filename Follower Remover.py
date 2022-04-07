try:
    import time
    import colorama
    import requests
    import configparser
    import os
    from colorama import init, Fore, Back, Style
    init()

except ImportError:
    print("[ERROR] Failed to import some modules, install the required modules listed:\n- requests\n- colorama\n- configparser\n\nThese can be installed via going to the cmd, and typing pip install (moduleName)")
    input()

config = configparser.ConfigParser()
config.read_file(open(r"Config.ini"))
cookie = str(config.get("auth","cookie"))

config.read_file(open(r"Config.ini"))

session = requests.Session()
session.cookies[".ROBLOSECURITY"] = cookie

# send first request
req = session.post(
    url="https://auth.roblox.com/"
)

if "X-CSRF-Token" in req.headers:  # check if token is in response headers
    session.headers["X-CSRF-Token"] = req.headers["X-CSRF-Token"]  # store the response header in the session

# send second request
req2 = session.post(
    url="https://auth.roblox.com/"
)

try:
    getuser = session.get("https://users.roblox.com/v1/users/authenticated")
    getuser2 = getuser.json()
    getuser3 = getuser2['id']
    getuser4 = getuser2['name']
    print(f"{Back.GREEN}{Fore.BLACK}[Authentication]{Back.BLACK}{Fore.WHITE} Logged in as {getuser4}")

except:
    print(f"{Back.RED}{Fore.BLACK}[ERROR]{Back.BLACK}{Fore.WHITE} Your cookie is invalid")
    print(f"{Back.YELLOW}{Fore.BLACK}[INFO]{Back.BLACK}{Fore.WHITE} Please restart the program, with a valid cookie")
    input()

print(f"{Back.MAGENTA}{Fore.BLACK}[FETCHING]{Back.BLACK}{Fore.WHITE} Fetching for friends")
response = session.get(f"https://friends.roblox.com/v1/users/{getuser3}/friends?userSort=StatusFrequents")
ids_and_item_types = response.json()["data"]
friendslist = [datum["id"] for datum in ids_and_item_types]
print(f"{Back.MAGENTA}{Fore.BLACK}[FETCHED]{Back.BLACK}{Fore.WHITE} Finished getting all friends")

count = session.get(f"https://friends.roblox.com/v1/users/{getuser3}/followers/count")
count5 = count.json()
count3 = count5['count']
val = True
if count3 == 0:
    print(f"{Back.RED}{Fore.BLACK}[ERROR]{Back.BLACK}{Fore.WHITE} Your followers have been removed already")
    val = False
    input()


friendslist = []
times = 0

while val == True:
    
    def program():
        global times
        global count
        global val
        global cookie
        global session
        getfollower = session.get(f"https://friends.roblox.com/v1/users/{getuser3}/followers")
        followes = getfollower.json()
        followers2 = followes['data'][0]['id']
        if followers2 in friendslist:
            print(f"{Back.YELLOW}{Fore.BLACK}[Notification]{Back.BLACK}{Fore.WHITE} A friend has been removed (id: {followers2})")
            with open('FriendsToAddBack.txt','a') as file:
                write = file.writelines(str(followers2)+'\n')
                file.close()
                pass
        
        block = session.post(f"https://accountsettings.roblox.com/v1/users/{followers2}/block")
        unblock = session.post(f"https://accountsettings.roblox.com/v1/users/{followers2}/unblock")
        
        if block.status_code == 400:
            print(f"{Back.RED}{Fore.BLACK}[RATELIMIT]{Back.BLACK}{Fore.WHITE} Too much requests being sent (codes: {block.status_code}/{unblock.status_code})")
            
        elif unblock.status_code == 400:
            unblockx = session.post(f"https://accountsettings.roblox.com/v1/users/{followers2}/unblock")

        elif block.status_code == 401 and unblock.status_code == 401:
            print(f"{Back.RED}{Fore.BLACK}[AUTH]{Back.BLACK}{Fore.WHITE} Token Validation Failed (codes: {block.status_code}/{unblock.status_code})")
            val = False
            print(f"{Back.YELLOW}{Fore.BLACK}[INFO]{Back.BLACK}{Fore.WHITE} Please restart the program, with a new cookie")
            input()
            
        elif block.status_code == 403 and unblock.status_code == 403:
            print(f"{Back.RED}{Fore.BLACK}[AUTH]{Back.BLACK}{Fore.WHITE} Renewing X-CSRF token") 
            session = requests.Session()
            session.cookies[".ROBLOSECURITY"] = cookie
            # send first request
            req = session.post(
                url="https://auth.roblox.com/"
            )

            if "X-CSRF-Token" in req.headers:  # check if token is in response headers
                session.headers["X-CSRF-Token"] = req.headers["X-CSRF-Token"]  # store the response header in the session

            # send second request
            req2 = session.post(
                url="https://auth.roblox.com/"
            )
        elif block.status_code == 200 and unblock.status_code == 200: 
            times+=1
            timescomma = "{:,}".format(times)
            count3comma = "{:,}".format(count3)
            print(f"{Back.BLUE}{Fore.BLACK}[Progress]{Fore.WHITE}{Back.BLACK} {timescomma}/{count3comma}")

    program()

    if times >= count3:
        print(f"{Back.GREEN}{Fore.BLACK}[SUCCESS]{Back.BLACK}{Fore.WHITE} Removed all followers")
        print(f"{Back.YELLOW}{Fore.BLACK}[INFO]{Back.BLACK}{Fore.WHITE} You may want to check if you have any friends to add back in: FriendsToAddBack.txt")
        input()
    
        

        
