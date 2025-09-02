from api.models.Models import ProducaoInterna

def findAll():
    return ProducaoInterna.query.all()