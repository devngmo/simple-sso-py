import re, os
  
regexEmailAddress = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$' 

def isValidEmailAddress(text):
    return re.search(regexEmailAddress, text)

def getEnvBool(key, defaultValue):
    if key in os.environ:
        v = ('%s' % os.environ[key]).lower()
        return v == '1' or v == 'true'
    return defaultValue

def getEnvValue(key, defaultValue):
    if key in os.environ:
        return os.environ[key]
    return defaultValue
