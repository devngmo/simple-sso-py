import sys
import os
import colorama
from colorama import Fore

colorama.init()

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))


from ..sp_in_memory_storage import InMemoryStorageProvider

storage = InMemoryStorageProvider()

storage.addDocument('docs', 1, {'name': 'doc 1', 'year': 2000})
storage.addDocument('docs', 2, {'name': 'doc 2', 'year': 2020})

doc1 = storage.getDocumentByID('docs', 1)
assert doc1 != None
assert doc1['name'] == 'doc 1'

doc2 = storage.getDocumentByID('docs', 2)
assert doc2 != None
assert doc2['name'] == 'doc 2'

doc1 = storage.findOne('docs', {'year': 2000})
assert doc1 != None
assert doc1['name'] == 'doc 1'

doc2 = storage.findOne('docs', {'year': 2020})
assert doc2 != None
assert doc2['name'] == 'doc 2'

print(Fore.GREEN + '[In Memory Storage Provider] passed all Tests')