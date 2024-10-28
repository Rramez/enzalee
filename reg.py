import requests
import os

REGISTRATION_FILE = os.getenv("REGISTRATION_FILE")

def loadRegisterations():
    registrations = {}


    if not os.path.exists(REGISTRATION_FILE):
        with open(REGISTRATION_FILE, 'w') as f:
            pass  # Create an empty file

    with open(REGISTRATION_FILE, 'r') as f:
        for line in f:
            discord_account, codeforces_account = line.strip().split()
            registrations[discord_account] = codeforces_account
    return registrations

def loadHandles():
    registrations = {}
    with open(REGISTRATION_FILE, 'r') as f:
        for line in f:
            discord_account, codeforces_account = line.strip().split()
            registrations[codeforces_account] = discord_account
    return registrations

registeredDiscordUsers = loadRegisterations()
registeredHandles = loadHandles()
regProcess = {}

def getHandleInfo(handle):
    url = f"https://codeforces.com/api/user.info?handles={handle}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data["status"] == "OK":
            return data["result"][0]
        else:
            return None
    else:
        return None


def getLatestSubmission(handle):

    url = f"https://codeforces.com/api/user.status?handle={handle}&from=1&count=1"
    
    response = requests.get(url)
    alotOfStuff = response.json()

    return alotOfStuff["result"][0] if alotOfStuff["result"] else {}


def deleteHandle(discordUserName):

    registered = (discordUserName in registeredDiscordUsers)

    if registered:
        # to allow handle being used again
        handle = registeredDiscordUsers[discordUserName]
        registeredHandles.pop(handle)

    registeredDiscordUsers.pop(discordUserName,"not registered.")

    if registered:
        with open(REGISTRATION_FILE, 'w') as f:
            for discord_account, codeforces_account in registeredDiscordUsers.items():
                f.write(f"{discord_account} {codeforces_account}\n")
    return


def validHandle(handle):

    url = f"https://codeforces.com/api/user.info?handles={handle}"
    respone = requests.get(url)
    info = respone.json()
    if info.get("status")=="FAILED":
        return 0
    
    return 1


def usedHandle(handle):
    return handle in registeredHandles


def usedDiscord(discordName):
    return discordName in registeredDiscordUsers


def userSpamming(discordName):
    return discordName in regProcess


def putInProcess(discordName):
    regProcess[discordName] = 1


def getSumbissionTime(handle):
    userLatestSubmission = getLatestSubmission(handle)
    return userLatestSubmission.get("creationTimeSeconds")

def getSubmissionVerdict(handle):
    userLatestSubmission = getLatestSubmission(handle)
    return userLatestSubmission.get("verdict")

def bind(discordName, handle):
    registeredDiscordUsers[discordName] = handle
    registeredHandles[handle] = discordName
    with open(REGISTRATION_FILE, 'a') as f:
        f.write(f"{discordName} {handle}\n")


def removeFromProcess(discordName):
    regProcess.pop(discordName)


def getHandleInfo(handle):
    url = f"https://codeforces.com/api/user.info?handles={handle}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data["status"] == "OK":
            return data["result"][0]
        else:
            return None
    else:
        return None
