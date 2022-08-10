import json
from sp_collection_storage import CollectionStorageProvider


class InMemoryStorageProvider(CollectionStorageProvider):
    def __init__(self):
        self.collections = {}

    def getAll(self, collectionID):
        if collectionID in self.collections:
            return self.collections[collectionID]
        return []

    def addDocument(self, collectionID, id, doc):
        if collectionID in self.collections:
            self.collections[collectionID][id] = doc
        else:
            self.collections[collectionID] = { id: doc }
        return id

    def updateDocument(self, collectionID, id, doc):
        if collectionID in self.collections:
            self.collections[collectionID][id] = doc
        else:
            self.collections[collectionID] = { id: doc }
        return id
    
    def getDocumentByID(self, collectionID, id):
        if collectionID in self.collections:
            if id in self.collections[collectionID]:
                return self.collections[collectionID][id]
        return None

    def findOne(self, collectionID, query):
        if collectionID not in self.collections:
            print('collection not exist: %s' % collectionID)
            return None

        print('Collection [%s] find one: %s' % (collectionID, json.dumps(query)))

        for docID in self.collections[collectionID]:
            match = True
            doc = self.collections[collectionID][docID]
            try:
                for k in query.keys():
                    if k == '_id':
                        if docID != query['_id']:
                            match = False
                            continue
                    elif doc[k] != query[k]:
                        match = False
                        continue
            except Exception as ex:
                print('Exception when compare with:')
                print(doc)
                print(ex)
                match = False
            if match:
                return doc
        return None