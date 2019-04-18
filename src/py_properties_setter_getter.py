'''
Created on Aug 1, 2018
/home/gkimetto/gk-sandbox/PYTHON/src/py_properties_setter_getter.py

@author: gkimetto
'''


class OpenShiftView():
    def __init__(self, session_details):
        self.session_details = session_details
    
    # You can call the property as a read only variable
        
    @property
    def internet_explorer_supported(self):
        return False
    
        """ Properties can also be set by defining setter/getter functions.
        The setter function sets the corresponding property's value.
        The getter gets the value.
        To define a setter, you need to use a decorator of the same name as 
        the property, followed by a dot and the setter keyword.
        The same applies to defining getter functions."""


# Step 2 ::: Add a setter to set when to support IE

    @internet_explorer_supported.setter
    def internet_explorer_supported(self, value):
        if value == True:
            
            # Ask for a pwer user password 
            
            #su_password = input("Enter Power User Password : ")
            print ("Enter Power User Password : ")
            su_password = "please"
            if su_password == "please":
                self.internet_explorer_supported = value
                print (openshift_view.internet_explorer_supported)
                value =False
                break
            else:
                raise ValueError("Hacker Alert!!!")
    
openshift_view = OpenShiftView(["username", "password","chrome","url"])
print ("Current Windows IE support :")
print (openshift_view.internet_explorer_supported)

print ("Try to allow IE support this time .... ")

openshift_view.internet_explorer_supported = True
print (openshift_view.internet_explorer_supported)