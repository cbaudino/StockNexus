from flask import render_template, redirect, url_for, flash
from app import db
from app.forms import ProductForm
from app.models import Product

def init_routes(app):
    @app.route('/')
    def index():
        products = Product.query.all()
        return render_template('index.html', products=products)

    @app.route('/add', methods=['GET', 'POST'])
    def add_product():
        form = ProductForm()
        if form.validate_on_submit():
            product = Product(
                name=form.name.data,
                description=form.description.data,
                price=form.price.data,
                supplier=form.supplier.data,
                stock=form.stock.data
            )
            db.session.add(product)
            db.session.commit()
            flash('Product added successfully!', 'success')
            return redirect(url_for('index'))
        return render_template('add_product.html', form=form)

    @app.route('/edit/<int:id>', methods=['GET', 'POST'])
    def edit_product(id):
        product = Product.query.get_or_404(id)
        form = ProductForm()
        if form.validate_on_submit():
            product.name = form.name.data
            product.description = form.description.data
            product.price = form.price.data
            product.supplier = form.supplier.data
            product.stock = form.stock.data
            db.session.commit()
            flash('Product updated successfully!', 'success')
            return redirect(url_for('index'))
        elif request.method == 'GET':
            form.name.data = product.name
            form.description.data = product.description
            form.price.data = product.price
            form.supplier.data = product.supplier
            form.stock.data = product.stock
        return render_template('edit_product.html', form=form)

    @app.route('/delete/<int:id>', methods=['POST'])
    def delete_product(id):
        product = Product.query.get_or_404(id)
        db.session.delete(product)
        db.session.commit()
        flash('Product deleted successfully!', 'success')
        return redirect(url_for('index'))

    @app.route('/search', methods=['POST'])
    def search_product():
        query = request.form.get('query')
        products = Product.query.filter(Product.name.like(f'%{query}%')).all()
        return render_template('index.html', products=products)
