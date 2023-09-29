from vagasdeestacionamento import app, database
from vagasdeestacionamento.models import Usuario, Vaga

with app.app_context():
   # database.drop_all()
    database.create_all()

# with app.app_context():
#     Usuario.query.all()
#     usuario = Usuario.query.all()
#     print(usuario)
#     usuario2 = Usuario.query.filter_by(username="NovoTeste").first()
#     print(usuario2.senha)

