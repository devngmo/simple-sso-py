def isValidEmailAddress(text:str):
    atIdx = text.index('@')
    return atIdx > 0 and atIdx < len(text)