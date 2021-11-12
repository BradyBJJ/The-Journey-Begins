#!python3
import os, random, string, csv
data = []
passwordData = {}

def main():
    while True:
        add = input('Would you like to add a user? ')
        if add.lower() == 'yes' or add.lower() == 'y' or add.lower() == 1:
            email = str(getEmail())
        else:
            writeToCSV(data)
            return
        # first, last, and username
        first, last, username = firstLastUser(email)
        # Get the license of the user
        licenseLevel = getLicense()
        # Get admin level
        adminLevel = getAdmin()
        # Can Publish? (True/False)
        canPublish = getPublishing()
        # Append temp data to global data variable and write user/pass info to passwordData
        appendData(username, passwordGen(), first, last, licenseLevel, adminLevel, canPublish, email)

def getEmail():
    email = input('Enter user email: ')
    return email

def firstLastUser(email):
    # Get first name
    split = email.split('.')
    # Get last name
    splitted = split[1].split('@')
    # Get first.last
    username = email.split('@')[0]
    return split[0], splitted[0], username;

def getLicense():
    licenses = {'C': 'Creator', 'E':'Explorer', 'V': 'Viewer', 'U': 'Unlicensed'}
    ans = input('License level: (C, E, V, U) ')
    if ans == '':
        return licenses['V']
    elif ans[0].upper() not in licenses.keys():
        return getLicense()
    else:
        return licenses[ans[0].upper()]

def getAdmin():
    # System, Site, None
    levels = ['system', 'site', 'none']
    ans = input('Admin level: (System, Site, None) ')
    if ans == '':
        return 'None'
    elif ans.lower() not in levels:
        return getAdmin()
    else:
        return ans[0].upper() + ans[1:]


def getPublishing():
    ans = input('Can the user publish?: (True or False)' )
    if ans == '':
        return False
    elif ans == 'T' or ans == 'True':
        return True
    else:
        return False

# Generate password
def passwordGen():
    length = 12
    chars = string.ascii_letters + string.digits + '!@#$%^&*()'
    random.seed = (os.urandom(1024))

    return ''.join(random.choice(chars) for i in range(length))

def appendData(username, password, first, last, licenseLevel, adminLevel, canPublish, email):
    # Create a spreadsheet which maps the username to the password
    userToPass(username, password)
    # Add data to temporary list
    tempData = []
    tempData = [username, password, first +' '+last, licenseLevel, adminLevel, canPublish, email]
    # Append user information to global variable
    data.append(tempData)
    return data

def userToPass(user, password):
    passwordData[user] = password
    # Write password data to .txt file
    with open('passwords.txt', 'w') as passwordFile:
        for key, value in passwordData.items():
            passwordFile.write('%s:%s\n' % (key, value))

def writeToCSV(userInfo):
    with open('Tableau.csv', 'w', encoding='UTF8', newline='') as file:
        writer = csv.writer(file)
        # Write multiple rows using data
        writer.writerows(userInfo)

main()

