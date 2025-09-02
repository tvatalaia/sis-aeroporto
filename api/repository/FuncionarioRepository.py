from api.models.Models import Funcionario

def findAll():
    return Funcionario.query.all()