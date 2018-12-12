import win32com.client as win32


outlook = win32.Dispatch("outlook.application")
outlookmapi = outlook.GetNamespace("MAPI")



def getMeetings():
	calendar = outlookmapi.GetDefaultFolder(9)
	appointments = calendar.Items


	for appointment in appointments:
	    #print(appointment.ResponseStatus)
	    #print(appointment.Display(Modal = True))
	    print(appointment.Body)
	    #print(appointment.Duration)
	    print(appointment.startUTC)
	    print(appointment.endUTC)
	    print(appointment.location)
	    print(appointment.Subject)

def newMeeting(address,subject,body,location,startUTC,duration):
	mail = outlook.CreateItem(2)
	mail.Subject = subject
	mail.Body = body  
	#mail.HTMLBody = 'Hi Tim, <br><br>Kindly attend the meeting.'
	mail.Location = location
	mail.Start = startUTC
	mail.Duration = duration
	recipient=address

	mail.MeetingStatus = 1
	mail.Recipients.Add(recipient)
	mail.send()