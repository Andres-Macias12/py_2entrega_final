from flask import Flask, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'unasecretasegura123!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///articulos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modelo de Artículo
class Articulo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    contenido = db.Column(db.Text, nullable=False)

# Definición del formulario
class ArticuloForm(FlaskForm):
    titulo = StringField('Título', validators=[DataRequired()])
    contenido = TextAreaField('Contenido', validators=[DataRequired()])
    submit = SubmitField('Enviar')

@app.route('/')
def index():
    articulos = Articulo.query.all()
    return render_template('index.html', articulos=articulos)

@app.route('/articulo/nuevo', methods=['GET', 'POST'])
def crear_articulo():
    form = ArticuloForm()
    if form.validate_on_submit():
        nuevo_articulo = Articulo(titulo=form.titulo.data, contenido=form.contenido.data)
        db.session.add(nuevo_articulo)
        db.session.commit()
        flash('Artículo creado con éxito!', 'success')
        return redirect(url_for('index'))
    return render_template('create.html', form=form)

@app.route('/articulo/editar/<int:id>', methods=['GET', 'POST'])
def actualizar_articulo(id):
    articulo = Articulo.query.get_or_404(id)
    form = ArticuloForm(obj=articulo)
    if form.validate_on_submit():
        articulo.titulo = form.titulo.data
        articulo.contenido = form.contenido.data
        db.session.commit()
        flash('Artículo actualizado con éxito!', 'success')
        return redirect(url_for('index'))
    return render_template('update.html', form=form)

@app.route('/articulo/eliminar/<int:id>', methods=['POST'])
def eliminar_articulo(id):
    articulo = Articulo.query.get_or_404(id)
    db.session.delete(articulo)
    db.session.commit()
    flash('Artículo eliminado con éxito!', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():  # Establecer contexto de aplicación
        db.create_all()  # Crea la base de datos y tablas si no existen
    app.run(debug=True)
