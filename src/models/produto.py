import uuid
from flask import session
from src.common.database import Database


class Produto(object):
    def __init__(self, nome, descricao, email, telefone, cep, imagem, _id=None):
        self.nome = nome
        self.descricao = descricao
        self.email = email
        self.telefone = telefone
        self.cep = cep
        self.imagem = imagem
        self._id = uuid.uuid4().hex if _id is None else _id

    def save_to_mongo(self):
        Database.insert(collection="produtos3", data=self.json())

    def json(self):
        return {
            "_id": self._id,
            "nome": self.nome,
            "descricao": self.descricao,
            "email": self.email,
            "telefone": self.telefone,
            "cep": self.cep,
            "imagem": self.imagem,
        }
