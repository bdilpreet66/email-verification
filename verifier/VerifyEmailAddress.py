import re
import smtplib
import dns.resolver

# Address used for SMTP MAIL FROM command  
fromAddress = 'corn@bt.com'

# Simple Regex for syntax checking
regex = '^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,})$'


# Email address to verify
def verify_email(add):
	#inputAddress = input('Please enter the emailAddress to verify:')
	inputAddress = add
	addressToVerify = str(inputAddress)

	
	user='unknown'
	domain='unknown'
	code='unknown'
	message='unknown'

	# Syntax check
	match = re.match(regex, addressToVerify)
	if match == None:
		code = 'ValueError'
		message = 'ValueError: Bad Syntax'

	if code != 'ValueError':
		# Get domain for DNS lookup
		splitAddress = addressToVerify.split('@')
		user = str(splitAddress[0])
		domain = str(splitAddress[1])
		print('Domain:', domain)

		if domain=='yahoo.com':
			message = "Unable to comfirm email"
		else:
			# MX record lookup
			records = dns.resolver.query(domain, 'MX')
			mxRecord = records[0].exchange
			mxRecord = str(mxRecord)

			
			# SMTP lib setup (use debug level for full output)
			server = smtplib.SMTP()
			server.set_debuglevel(0)
			
			# SMTP Conversation
			server.connect(mxRecord)
			server.helo(server.local_hostname) ### server.local_hostname(Get local server hostname)
			server.mail(fromAddress)
			code, message = server.rcpt(str(addressToVerify))
			server.quit()

	return {'code':code,'message':message,'domain':domain,'user':user}

#print(f'code = {code}')
#print(f'message = {message}')

# Assume SMTP response 250 is success
#if code == 250:
#	print('Success')
#else:
#	print('Bad')