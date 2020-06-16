# Python code examples for the SmartConnect API
This sample code will show how the SmartConnect web services can be consumed through some simple Python functions.

This example uses the [SmartConnect.com](https://smartconnect.com/ "SmartConnect.com") web services to run predefined integrations in SmartConnect.

### Configuration
You will need to supply some starting details which are included as variables at the start of the file.
```{python}
#Set Variables
CustomerId = 'ebab41e1-dc5a-4dfa-aa05-5c900cb839e8'
APIUrl ='https://smartconnectschedule.azurewebsites.net/API'
email = 'test@eonesolutions.com'
password = 'password'
#Not needed for all endpoints
mapKey = '364fde19-0748-4d10-886f-a95300a506c5'
```
![increment](https://i.imgur.com/xHoRgNT.png)


### Getting Started
* All of the endpoints can be called independently
* Every request will encode the password and request a new token before performing the command
* All error lists come in XML, this sample will format the XML in a readable format.

### Troubleshooting
* Blank response from server? Make sure the API URL is correct and you have access to the MapKey being used.

**Something else isn't working properly**
* Use github's issue reporter on the right
* Send me an email ethan.sorenson@eonesolutions.com (might take a few days)

### Updates
* 1.0.0.0 first release on Python 3.7

***Enjoy!***
