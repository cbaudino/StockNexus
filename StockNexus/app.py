"""
Este módulo define la aplicación Flask para StockNexus.
"""

from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, Product
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

with app.app_context():
    db.create_all()

@app.before_first_request
def create_tables():
    """
    Crea las tablas de la base de datos antes de la primera solicitud.
    """
    db.create_all()

@app.route('/')
def index():
    """
    Ruta principal que muestra el catálogo de productos.
    """
    products = Product.query.all()
    return render_template('index.html', products=products)

@app.route('/add', methods=['GET', 'POST'])
def add_product():
    """
    Ruta para agregar un nuevo producto al catálogo.
    """
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = request.form['price']
        supplier = request.form['supplier']
        stock = request.form['stock']
        new_product = Product(name=name, description=description, price=price, supplier=supplier, stock=stock)
        db.session.add(new_product)
        db.session.commit()
        flash('Product added successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('add_product.html')

@app.route('/edit/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    """
    Ruta para editar un producto existente en el catálogo.
    """
    product = Product.query.get_or_404(product_id)
    if request.method == 'POST':
        product.name = request.form['name']
        product.description = request.form['description']
        product.price = request.form['price']
        product.supplier = request.form['supplier']
        product.stock = request.form['stock']
        db.session.commit()
        flash('Product updated successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('edit_product.html', product=product)

@app.route('/delete/<int:product_id>', methods=['POST'])
def delete_product(product_id):
    """
    Ruta para eliminar un producto del catálogo.
    """
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    flash('Product deleted successfully!', 'success')
    return redirect(url_for('index'))

@app.route('/search', methods=['GET', 'POST'])
def search_product():
    """
    Ruta para buscar productos en el catálogo.
    """
    if request.method == 'POST':
        query = request.form['query']
        products = Product.query.filter(
            (Product.name.like(f'%{query}%')) |
            (Product.description.like(f'%{query}%'))
        ).all()
        return render_template('search_product.html', products=products)
    return render_template('search_product.html')

if __name__ == '__main__':
    app.run(debug=True)
