import requests
import bs4
import paho.mqtt.client as mqtt

# getting data from the google news webpage.
response = requests.get('https://news.google.com/covid19/map?hl=es-419&mid=%2Fm%2F01btyw&gl=US&ceid=US%3Aes-419') 
# parsing request object into a lxml file so data is readable
soup = bs4.BeautifulSoup(response.text, 'lxml') 
# selecting from the proper webpage class the actual number of covid cases in Jalisco.
data = soup.select('.UvMayb')
# defining an array where the class values are to be stored: cases and deceases
values = [] 
# looping through the object created to get just the covid cases from the class. 
# The class itself has two different values: cases and deceases
for i in data: 
    # extracting just the text saved in the class. Ignoring any other data saved on it
	values.append(str(i.text)) 
# loading the first index of the array, which is the covid cases number
cases = values [0] 
# loading the second index of the array, which is the covid deceases number
deceases = values [1]

#cases = "30,589"
#deceases = "3,677"

print(cases)
print(deceases)

###### MQTT ######

def on_connect(client, userdata, flags, rc):
	if rc == 0:
		print("Client connected to broker")
		global connected
		connected = True
	else:
		print("Connection failed ", rc)

broker = "io.adafruit.com" # IP address or server name for the broker
user = "elotroadrian"
password = "aio_uEDb20xFl5FlwQQXl1NFbdwAoeOU"
client = mqtt.Client("Covid")
client.username_pw_set(user,password=password)
client.on_connect = on_connect # using callback function to manage the connection
client.connect(broker)
client.loop_start() # this loop will process the callback functions.
client.publish("elotroadrian/feeds/covidcases",cases)
client.loop_stop()
client.loop_start() # this loop will process the callback functions.
client.publish("elotroadrian/feeds/coviddemease",deceases)
client.loop_stop()

