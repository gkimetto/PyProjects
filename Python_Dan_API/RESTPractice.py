import requests


url= 'https://jsonplaceholder.typicode.com/photos'
# #rest_request = requests.get(test_url)
# #print rest_request.status_code()
# 
# r = requests.get('https://github.com/timeline.json')
# print r.status_code
# #'http://jsonplaceholder.typicode.com/posts'

response = requests.get(url)
json_response= response.json()
#print json_response
# Create empty List
list_of_urls=[]
for photos in json_response:
    list_of_urls.append(photos['url'])
    if (photos['url']=='https://via.placeholder.com/600/24f355'):
        print photos['title']
        
    
#    if key=='url':
       #list_of_urls.append(json_response[key])
jsonPayload={'albumId':1, 'title':'Karibuni','url':'https://karibu.nyumbani', 'thumbnailUrl':'https://nowhereman' }

#POST
response = requests.post(url,json=jsonPayload)
print response.json()

#PUT
jsonPayload={'albumId':1, 'title':'Karibuni','url':'https://karibu.nyumbani', 'thumbnailUrl':'https://nowhereman' }

update_url='https://jsonplaceholder.typicode.com/photos/100'
response = requests.put(update_url,json=jsonPayload)
print response.json()

#GET
url_comments='http://jsonplaceholder.typicode.com/comments'
response=requests.get(url_comments)
for comment in response.json():
    print "hello" #comment['email']
    

#DELETE
jsonPayload={"postId": 2,"id": 7,"name": "voluptatum","email": "Dallas@ole.me","body": "maiores sed dolores"}
response = requests.delete(url,json=jsonPayload)
print response.json()


#print (response.json())
print len(list_of_urls)
print len(set(list_of_urls))

#Authentication Insecure

ocp_3_10_url ='https://selt-vm1.css.lab.eng.rdu2.redhat.com:8443/oapi/v1'
ocp_headers = {'Authorization': 'Bearer NCCEbeUrzJON6C0_yqTp1ooxABCB0GMmZadKCKQC8hQ'}

try:
    response=requests.get(ocp_3_10_url, headers=ocp_headers, verify=False)
    print response.json()
except:
    print "An Exception occurred."

response= requests.get(ocp_3_10_url, auth=('admin','redhat'))
print response.json()
    
