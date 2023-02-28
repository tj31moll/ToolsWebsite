from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# connect to the database
conn = sqlite3.connect('recipes.db')
c = conn.cursor()

# create table for recipes
c.execute('''CREATE TABLE IF NOT EXISTS recipes
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              name TEXT,
              ingredients TEXT,
              directions TEXT)''')
conn.commit()

@app.route('/')
def home():
    # query all recipes from the database
    c.execute("SELECT * FROM recipes")
    recipes = c.fetchall()
    return render_template('home.html', recipes=recipes)

@app.route('/add_recipe', methods=['GET', 'POST'])
def add_recipe():
    if request.method == 'POST':
        # get recipe data from the form
        name = request.form['name']
        ingredients = request.form['ingredients']
        directions = request.form['directions']
        
        # insert recipe into the database
        c.execute("INSERT INTO recipes (name, ingredients, directions) VALUES (?, ?, ?)",
                  (name, ingredients, directions))
        conn.commit()
        return redirect(url_for('home'))
    
    return render_template('add_recipe.html')

@app.route('/delete_recipe/<int:id>', methods=['POST'])
def delete_recipe(id):
    # delete recipe from the database
    c.execute("DELETE FROM recipes WHERE id=?", (id,))
    conn.commit()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
