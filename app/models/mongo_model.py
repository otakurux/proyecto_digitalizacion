from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime
import os

class MongoModel:
    """Clase base para manejo de colecciones MongoDB como 'base de datos'"""

    def __init__(self, collection_name, db_name='umsa_digital'):
        # Conexión a MongoDB (local por defecto, puerto 27017)
        # Se puede cambiar la URI via variable de entorno MONGO_URI
        mongo_uri = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/')
        self.client = MongoClient(mongo_uri)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def _clean_doc(self, doc):
        """Elimina el campo _id de MongoDB para que sea serializable a JSON"""
        if doc and '_id' in doc:
            doc.pop('_id')
        return doc

    def _clean_list(self, docs):
        """Limpia _id de una lista de documentos"""
        return [self._clean_doc(doc) for doc in docs]

    def get_all(self):
        """Obtener todos los documentos de la colección"""
        return self._clean_list(list(self.collection.find({}, {'_id': 0})))

    def get_by_id(self, item_id):
        """Buscar documento por ID (campo 'id' personalizado)"""
        doc = self.collection.find_one({'id': item_id}, {'_id': 0})
        return self._clean_doc(doc)

    def get_by_field(self, field, value):
        """Buscar documentos por cualquier campo"""
        return self._clean_list(list(self.collection.find({field: value}, {'_id': 0})))

    def create(self, item):
        """Insertar nuevo documento"""
        item['created_at'] = datetime.now().isoformat()
        result = self.collection.insert_one(item)
        # Retornar sin _id
        return self._clean_doc(item)

    def update(self, item_id, updates):
        """Actualizar documento por ID"""
        updates['updated_at'] = datetime.now().isoformat()
        result = self.collection.update_one(
            {'id': item_id},
            {'$set': updates}
        )
        if result.matched_count > 0:
            return self.get_by_id(item_id)
        return None

    def delete(self, item_id):
        """Eliminar documento por ID"""
        result = self.collection.delete_one({'id': item_id})
        return result.deleted_count > 0

    def count(self):
        """Contar documentos en la colección"""
        return self.collection.count_documents({})

    def drop_collection(self):
        """Eliminar toda la colección (uso con precaución)"""
        self.collection.drop()
