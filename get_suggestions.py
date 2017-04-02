# Get destination given a user name 
#no keys
import json
import requests 
import sys
import pyrebase
import re 

with open('Amadeus.json') as data_file:
	data = json.load(data_file)

results = data['data']
num = 0;
destinations = []
for i in results:
	res = i['travelers']
	for j in res:
		name = j['first_name'] + ' ' + j['last_name']
		if name == sys.argv[1]:
			dest = i['reservation']['flight_tickets']
			for k in dest:
				flight_bounds = k['flight_bounds']
				for l in flight_bounds:
					flights = l['flights']
					for m in flights:
						destinations.append(m['destination']['airport'])

print destinations

value = []

for i in destinations:
	response = requests.get('https://api.sandbox.amadeus.com/v1.2/location/{}'.format(i), params=[('apikey', 'amadeus_key')])
	try:
		lat = response.json()['city']['location']['latitude']
        	lng = response.json()['city']['location']['longitude']
	except:
		lat = response.json()['airports'][0]['location']['latitude']
                lng = response.json()['airports'][0]['location']['longitude']

	city = response.json()['airports'][0]['city_name']
	key_string = {'user-key':'zomato_key'}

	#for cuisines around
	url = 'https://developers.zomato.com/api/v2.1/geocode?lat=' + str(lat) + '&lon=' + str(lng)

	response = requests.get(url, headers = key_string)
	ids = response.json()
	cuisines = ids['popularity']['top_cuisines'];
	for c in cuisines:
		value.append(c)

# Get last n purchases using the user name
#------------------------------------------
key_string = [('key','capital_one_key')]
response = requests.get('http://api.reimaginebanking.com/accounts', params=key_string)
ids = response.json()

merchant_ids = []
for i in ids:
	name = i['nickname']
	if name == sys.argv[1]:
		id = i['_id']	
		url = 'http://api.reimaginebanking.com/accounts/{}/purchases'.format(id)
		response = requests.get(url, params=key_string);
		for i in response.json():
			merchant_ids.append(i['merchant_id'])
			

# Get the category tags of the merchants 
categories=[]
restaurants=[]
restaurant_list = set()
sorted_restaurant_list = set()

for i in merchant_ids:
	response = requests.get('http://api.reimaginebanking.com/merchants/{}'.format(i), params=key_string)
	searchterm = response.json()['name']
	restaurant_lat = response.json()['geocode']['lat']
	restaurant_long = response.json()['geocode']['lng']
	key_string_new = {'user-key':'zomato_key'}

	result = response.json()['category']
	for i in result:
		categories.append(i)
	#find the actual place and id using the name tag
	url = 'https://developers.zomato.com/api/v2.1/search?q=' + searchterm + '&lat=' + str(restaurant_lat) + '&lon=' + str(restaurant_long)
	response = requests.get(url, headers = key_string_new)
	ids = response.json()

	res = ids['results_shown']
	cuisinemap = dict()
	if(res == 0):
    		print 'no results'
	else:
   		print ids['restaurants'][0]['restaurant']['id']
    		print ids['restaurants'][0]['restaurant']['name']
    		print ids['restaurants'][0]['restaurant']['cuisines']
    		cuisinesliststring = ids['restaurants'][0]['restaurant']['cuisines']
    
    		cuisinelist = re.split(', ',cuisinesliststring)
    		for i in cuisinelist:
        		if(cuisinemap.has_key(i)):
            			val = cuisinemap[i]
            			cuisinemap[i] = val+1
        		else:
            			cuisinemap[i] = 1

	response = requests.get('https://developers.zomato.com/api/v2.1/cities?q='+city, headers = key_string_new)#params=key_string)
	ids = response.json()

	city_name = ids["location_suggestions"][0]["name"]
	city_id = ids["location_suggestions"][0]["id"]

	cuisineidmap = dict()
	url = 'https://developers.zomato.com/api/v2.1/cuisines?city_id=' + str(city_id)
	response = requests.get(url, headers = key_string_new)
	ids = response.json()
	for i in range(0,len(ids['cuisines'])):
    		cuisinearray = ids['cuisines'][i]['cuisine']
    		cuisineidmap[cuisinearray['cuisine_name']] = cuisinearray['cuisine_id']

	#find corresponding restaurants for the cuisines int hat city
	print cuisinelist
	print cuisines
	restaurantmap = dict()
	for j in cuisines:
    		curcuisineid = cuisineidmap[j]
    		url = 'https://developers.zomato.com/api/v2.1/search?entity_id=' + str(city_id) + '&entity_type=city&cuisines=' + str(curcuisineid)
    		response = requests.get(url, headers = key_string_new)
   	 	ids = response.json()
    		maxrange = min(5,ids['results_found'])
    		for i in range(0,maxrange):
        		restaurantname = ids['restaurants'][i]["restaurant"]["name"]
        		if(j in cuisinelist):
				print '#' + restaurantname
            			restaurant_list.add('# ' + restaurantname)
				if(restaurantname in restaurant_list):
					restaurant_list.remove(restaurantname)
        		else:
            			restaurant_list.add(restaurantname)
        			restaurantaddress = ids['restaurants'][i]["restaurant"]["location"]["address"]
        			restaurantmap[restaurantname] = restaurantaddress
				if(('# '+restaurantname) in restaurant_list):
					restaurant_list.remove(restaurantname)
	print restaurant_list
	sorted_restaurant_list = sorted(restaurant_list)
	#sorted(restaurant_list, key=lambda item: (int(item.partition(' ')[0])
        #                       if item[0].isdigit() else float('inf'), item))

#for i in restaurant_list:	
	#restaurantlist.append(i)


print restaurant_list
config = {
  	"apiKey": "apiKey",
  	"authDomain": "travelpro-c7e1f.firebaseapp.com",
  	"databaseURL": "https://travelpro-c7e1f.firebaseio.com",
  	"storageBucket": "travelpro-c7e1f.appspot.com"
}

response = requests.get("https://travelpro-c7e1f.firebaseio.com/users.json", None);
val = response.json()
for i in val.keys():
	print i
	if val[i]['username'] == sys.argv[1]:
		id = i
		token = val[i]['token']

print token
firebase = pyrebase.initialize_app(config)
db = firebase.database()
data = {"suggestions": sorted_restaurant_list}
results = db.child("users").child(id).update(data);

body = 'Since you are travelling, we thought of making a suggestion !! Do visit {}'.format(list(sorted_restaurant_list)[0])

url='https://fcm.googleapis.com/fcm/send'
myheaders={'Content-Type':'application/json',
           'Authorization':'key=Firebasekey'}

payload = {
	
             "to": token,
		"notification": {
                "body" : body,
                "title" : "TravelPro: We have a suggestion !!"
              }
}

response = requests.post(url,data=json.dumps(payload), headers=myheaders)

'''	
	ids = response.json()
	res = ids['results_shown']
	if(res == 0):
    		print 'no results'
	else:
    		print ids['restaurants'][0]['restaurant']['id']
    		print ids['restaurants'][0]['restaurant']['name']
    		print ids['restaurants'][0]['restaurant']['cuisines']
'''

'''for i in categories:
	print i '''

# Post enquiries using that data

# Notify if the time is afternoon or is 6 ??
