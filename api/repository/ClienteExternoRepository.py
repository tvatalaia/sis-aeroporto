from api.models.Models import ClienteExterno

def findAll():
    return ClienteExterno.query.all()