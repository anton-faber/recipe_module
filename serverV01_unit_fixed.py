from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    db_connection = sqlite3.connect('items.db')
    db_cursor = db_connection.cursor()

    db_cursor.execute('SELECT DISTINCT item_name FROM items')
    item_names = db_cursor.fetchall()

    if request.method == 'POST':
        user_qtys = list(map(float, request.form.getlist('user_qtys[]')))
        consolidated_results = []

        for i, item_name in enumerate(item_names):
            user_qty = user_qtys[i]
            db_cursor.execute('SELECT ingredient_name, quantity FROM items WHERE item_name = ?', (item_name[0],))
            item_rows = db_cursor.fetchall()

            for row in item_rows:
                ingredient_name, quantity = row
                qty = float(quantity) * user_qty
                consolidated_results.append((item_name[0], ingredient_name, qty))

        consolidated_results = [
            (item_name, ingredient_name, format(qty, '.3f'))
            for item_name, ingredient_name, qty in consolidated_results
        ]

        db_connection.close()
        return render_template('consolidated_item_details.html', consolidated_results=consolidated_results)

    db_connection.close()
    return render_template('index.html', item_names=item_names)

@app.route('/get_consolidated_ingredients', methods=['POST'])
def get_consolidated_ingredients():
    db_connection = sqlite3.connect('items.db')
    db_cursor = db_connection.cursor()

    item_names = request.form.getlist('item_names[]')
    user_qtys = list(map(float, request.form.getlist('user_qtys[]')))

    ingredient_totals = {}
    unit_associations = {}  # New dictionary to store units associated with ingredient names

    for i, item_name in enumerate(item_names):
        user_qty = user_qtys[i]
        db_cursor.execute('SELECT ingredient_name, quantity, unit FROM items WHERE item_name = ?', (item_name,))
        item_rows = db_cursor.fetchall()

        for row in item_rows:
            ingredient_name, quantity, unit = row
            qty = float(quantity) * user_qty

            if ingredient_name in ingredient_totals:
                ingredient_totals[ingredient_name] += qty
            else:
                ingredient_totals[ingredient_name] = qty

            if ingredient_name not in unit_associations:
                unit_associations[ingredient_name] = unit

    aggregated_results = [
        (ing, format(qty, '.3f'), unit_associations[ing])
        for ing, qty in ingredient_totals.items()
    ]
    db_connection.close()
    return render_template('consolidated_item_details.html', aggregated_results=aggregated_results) 

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
