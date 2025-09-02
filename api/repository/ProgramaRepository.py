from api.models.Models import Programa

def findAll():
    return Programa.query.all()