#!python3
# Takes a CSV file with usernames in format: first.last
# and creates a CSV file which will be imported into Tableau.
# This file will create "Viewers" along with their login credentials."
import re, os, random, string, csv

userData = []
userPasswords = {}
def main():
	users = readCSV()
	for user in users:
		# Get the display name of users in format: "First Last"
		displayName = getDisplayName(''.join(user))
		# Turn username into email: first.last@id.me
		emailAddress = ''.join(user) + '@id.me'
		# Generates a strong password
		password = getPassword(''.join(user))
		# Append userdata to list: Assumes user is a VIEWER
		appendData(''.join(user), password, displayName, emailAddress)
	# Write user data to CSV file which will be imported to Tableau
	writeToCSV()
	# Generate a email script which contains users login credentials
	getEmail(users)
	
# Returns users within CSV file as a list
def readCSV():
	userList = []
	with open('testCSV.csv') as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')
		for row in csv_reader:
			userList.append(row)
	return userList

# Seperates first and last to get display name
def getDisplayName(username):
	matchName = re.match(r'(.*)\.(.*)', username)
	return matchName.group(1).capitalize() + ' ' + matchName.group(2).capitalize()

# Generate password
def getPassword(username):
	length = 12
	chars = string.ascii_letters + string.digits + '!@#$%^&*()'
	random.seed = (os.urandom(1024))
	password = ''.join(random.choice(chars) for i in range(length))
	# Link username to password and store in dictionary
	userPasswords[username] = password
	return password
	
# Append user data to list which will then be written to CSV
def appendData(username, password, name, email):
	tempData = [username, password, name, 'Viewer', 'None', 'False', email]
	userData.append(tempData)

# Write data acquired into CSV file
def writeToCSV():
	with open('importThisUserList.csv', 'w', encoding='UTF8', newline='') as file:
		writer = csv.writer(file)
		# Write multiple rows using data
		writer.writerows(userData)

# Write email script to txt file containing login information
def getEmail(userList):
	with open('loginCredentials.txt', 'w') as loginFile:
		for i in userList:
			username = ''.join(i)
			password = userPasswords[''.join(i)]
			loginFile.write(f"\nhttps://tableau.idmeinct.net\n Username: {username}\n Password: {password}\n Please change your password upon logging in. Please note you must be in office and/or on the VPN in order to connect. Let me know if you have any questions.\n As usual requests must be approved until if/when standard access is denied\n\n Thank you,\n Brady\n")
			
main()