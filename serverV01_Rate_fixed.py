from flask import Flask, render_template, request, redirect, url_for
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
            db_cursor.execute('SELECT ingredient_name, quantity, unit, value FROM items WHERE item_name = ?', (item_name,))
            item_rows = db_cursor.fetchall()

            print(f"Item Name: {item_name}")
            for row in item_rows:
                ingredient_name, quantity, unit, value = row
                qty = float(quantity) * user_qty
                ingredient_value = qty * float(value)
                print(f"  Ingredient: {ingredient_name}, Qty: {qty}, Unit: {unit}, Value: {ingredient_value}")

                consolidated_results.append((item_name, ingredient_name, format(qty, '.3f'), unit, format(ingredient_value, '.2f')))

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

    consolidated_results = []

    for i, item_name in enumerate(item_names):
        user_qty = user_qtys[i]
        db_cursor.execute('SELECT ingredient_name, quantity, unit, value FROM items WHERE item_name = ?', (item_name,))
        item_rows = db_cursor.fetchall()

        for row in item_rows:
            ingredient_name, quantity, unit, value = row
            qty = float(quantity) * user_qty
            ingredient_value = qty * float(value)

            consolidated_results.append((ingredient_name, format(qty, '.3f'), unit, format(ingredient_value, '.2f')))

    db_connection.close()

    total_value = sum(float(result[3]) for result in consolidated_results)
    return render_template('consolidated_item_details.html', consolidated_results=consolidated_results,total_value = total_value)
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
