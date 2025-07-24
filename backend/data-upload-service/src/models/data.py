from src.database import db

class Data(db.Model):
    __tablename__ = 'data'
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.String(10), nullable=False)
    hora = db.Column(db.String(5), nullable=False)
    rut = db.Column(db.String(12), nullable=False)

    def __repr__(self):
        return f"<Data {self.fecha} {self.hora} {self.rut}>"