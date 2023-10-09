from flask import Flask, render_template, request, redirect, url_for
from collections import defaultdict  # Import defaultdict from collections module
import sqlite3

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_qtys = list(map(float, request.form.getlist('user_qtys[]')))
        item_names = request.form.getlist('item_names[]')
        consolidated_results = []

        db_connection = sqlite3.connect('items.db')
        db_cursor = db_connection.cursor()

        for i, item_name in enumerate(item_names):
            user_qty = user_qtys[i]
            db_cursor.execute('SELECT ingredient_name, quantity, unit, value, category FROM items WHERE item_name = ?', (item_name,))
            item_rows = db_cursor.fetchall()

            print(f"Item Name: {item_name}")
            for row in item_rows:
                ingredient_name, quantity, unit, value, category = row
                qty = float(quantity) * user_qty
                ingredient_value = qty * float(value)
                print(f"  Ingredient: {ingredient_name}, Qty: {qty}, Unit: {unit}, Value: {ingredient_value}, category: {category}")

                consolidated_results.append((item_name, ingredient_name, format(qty, '.3f'), unit, format(ingredient_value, '.2f'), category))

        db_connection.close()
        return render_template('consolidated_item_details.html', consolidated_results=consolidated_results)

    db_connection = sqlite3.connect('items.db')
    db_cursor = db_connection.cursor()

    db_cursor.execute('SELECT DISTINCT item_name FROM items')
    item_names = db_cursor.fetchall()
    db_connection.close()

    return render_template('index.html', item_names=item_names)


@app.route('/get_consolidated_ingredients', methods=['POST'])
def get_consolidated_ingredients():
    db_connection = sqlite3.connect('items.db')
    db_cursor = db_connection.cursor()

    item_names = request.form.getlist('item_names[]')
    user_qtys = list(map(float, request.form.getlist('user_qtys[]')))

    # Create dictionaries to store category and unit information for each ingredient
    ingredient_categories = {}
    ingredient_units = {}

    consolidated_results = defaultdict(lambda: {'qty': 0, 'value': 0, 'category': '', 'unit': ''})

    for i, item_name in enumerate(item_names):
        user_qty = user_qtys[i]
        db_cursor.execute('SELECT ingredient_name, quantity, unit, value, category FROM items WHERE item_name = ?', (item_name,))
        item_rows = db_cursor.fetchall()

        for row in item_rows:
            ingredient_name, quantity, unit, value, category = row
            qty = float(quantity) * user_qty
            ingredient_value = qty * float(value)

            # Update the consolidated_results dictionary for the ingredient
            consolidated_results[ingredient_name]['qty'] += qty
            consolidated_results[ingredient_name]['value'] += ingredient_value

            # Store the category and unit information for the ingredient
            ingredient_categories[ingredient_name] = category
            ingredient_units[ingredient_name] = unit

    db_connection.close()

    # Convert the consolidated_results dictionary to a list for rendering in the template
    consolidated_results_list = [
        (ingredient_name, format(data['qty'], '.3f'), data['unit'], format(data['value'], '.2f'), ingredient_categories[ingredient_name])
        for ingredient_name, data in consolidated_results.items()
    ]

    total_value = sum(data['value'] for data in consolidated_results.values())

    return render_template('consolidated_item_details.html', consolidated_results=consolidated_results_list, total_value=total_value)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
