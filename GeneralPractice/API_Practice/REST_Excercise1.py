import requests

url = 'http://jsonplaceholder.typicode.com/posts'
response = requests.get(url)
print(response.json())


jsonPayload = {'albumId': 1, 'title': 'Legend', 'star': 'will smith','url': 'no.com'}
response = requests.post(url, json=jsonPayload)
print(response.json())

url = 'http://jsonplaceholder.typicode.com/photos/100'
jsonPayload2= {'albumId':1, 'title':'test','url':'nothing.com', 'thumbNailUrl':'nothing.com','id':5001 } # @IgnorePep8

response = requests.put(url, json= jsonPayload2)
print(response.json())

response = requests.delete(url)
print(response.json())

"""Try to log into GitHub without a password """

git_url = 'https://api.github.com/user'
response = requests.get(git_url)
print(response.json())


"""Try to log in with a clear password """

#response = requests.get(git_url, auth =('kimettog', 'QuayM8oN!ght0wl'))
response = requests.get(git_url, headers={'Authorization': 'Bearer 749cd4386b9b71357e041fe42ff3dfab9869a4fe'})  # @IgnorePep8
print("GIT LOGIN:")

print(response.json())

git_json = response.json()
for key in git_json.keys():
    print(key)


resp = git_json['hireable']


print(resp)

"""Exercise:
Check to see if there are duplicate URLs in the Photos"""
photo_url_list = []

photos_url = 'http://jsonplaceholder.typicode.com/photos'
response = requests.get(photos_url)

photo_list = response.json()

# print "Printing the first item"
#
# print photo_list[0]

for photo in photo_list:
    photo_url_list.append(photo['url'])

set_url_list = set(photo_url_list)

print("Number of URLs in the list are : ", len(photo_url_list))
print("Number of unique URLs are: ", len(set_url_list))
#     print key
#     photo_url_list=photo_dict["url"]
#
# print photo_url_list
