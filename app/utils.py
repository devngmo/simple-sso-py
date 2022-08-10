import re   
  
regexEmailAddress = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$' 

def isValidEmailAddress(text):
    return re.search(regexEmailAddress, text)