'''
Created on Aug 1, 2018
/home/gkimetto/gk-sandbox/PYTHON/src/py_properties.py

@author: gkimetto
Details: """Properties provide a way of customizing access to instance attributes. 
            They are created by putting the property decorator above a method,
            which means when the instance attribute with the same name as the
            method is accessed, the method will be called instead. 
            One common use of a property is to make an attribute read-only."""
'''


class OpenShiftView():
    def __init__(self, session_details):
        self.session_details = session_details
    
    # You can call the property as a read only variable
        
    @property
    def internet_explorer_supported(self):
        return False
    
openshift_view = OpenShiftView(["username", "password","chrome","url"])
print ("Current Windows IE support :")
print (openshift_view.internet_explorer_supported)

# Step1 ::: Let's try to force Support for Windows IE
# 
# print ("Attempt to change support for Windows IE to True :")
# openshift_view.internet_explorer_supported = True



