import requests, json, smtplib, ssl

#dnsfuzzer API
url = "https://dns-fuzzer.p.rapidapi.com/fuzz-domain/"

d = input("Enter domain: ")
payload = "domain={}".format(d)
headers = {
    'content-type': "application/x-www-form-urlencoded",
    'x-rapidapi-host': "dns-fuzzer.p.rapidapi.com",
    'x-rapidapi-key': "Put in your rapidapi key here"
    }

response = requests.request("POST", url, data=payload, headers=headers)


#write to json file
jsonFile = open("data.json", "w")
jsonFile.write(response.text)
jsonFile.close()


jsonFile = open("data.json", "r")
values = json.load(jsonFile)

whitelist = ['hailbytes.com', 'hailbyte.com'] #put in your whitelist here
fuzzed_domains = []
for i in values:
	fuzzed_domains.append(i['domain'])
	
print(fuzzed_domains)

#live domain checker
live_domains = []
for d in fuzzed_domains:
	try:
		website = 'http://'+d 
		get = requests.get(website, verify=False, allow_redirects=False, timeout=5)
		if get.status_code == 200:
			live_domains.append(d)
	except requests.exceptions.RequestException as e:
		continue
		
print(live_domains)

phish_domains = [item for item in live_domains if item not in whitelist]
phish_domains = ' | ' .join(phish_domains)
print(phish_domains)

#send email 
port = 465  # For SSL
smtp_server = "smtp.gmail.com"
sender_email = "youremail@gmail.com"
receiver_email = "youremail@gmail.com"
password = "yourpassword"
message = phish_domains

context = ssl.create_default_context()
with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
	server.login(sender_email, password)
	server.sendmail(sender_email, receiver_email, message)
