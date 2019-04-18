class RedShirt():

   def __init__(self):
     self.clean=True
   def make_dirty(self):
     self.clean=False
     return self.clean
   def make_clean(self):
     self.clean=True
     return self.clean
