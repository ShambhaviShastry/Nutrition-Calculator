from flask import Flask, render_template, request, redirect, url_for
import pandas as pd

excel_file = r"C:\Users\shamb\OneDrive\Documents\Ashoka University UG\Second Sem\OCaml\.vscode\.vscode\nutrition.xlsx"
excel_file_recipes = r"C:\Users\shamb\Downloads\dishes_nutrition_per_100g.xlsx"
excel_file_units = r"C:\Users\shamb\Downloads\units.xlsx"

app = Flask (__name__)

def serving(x, y):
    y = (float) (y)
    return (x * y)

def multiply(x, y, i):
    return x [i] * y [i]

@app.route("/choice", methods = ["GET", "POST"])
def choice():
    return render_template('first.html')

@app.route("/format", methods = ["GET", "POST"])
def format():

    if request.method == "POST":

        recipe = request.form.get('recipe', '').strip()                      #special kind of dictionary
        serving_size = request.form.get('serving_size','').strip()

        ingredient = request.form.getlist ('ingredient')
        unit = request.form.getlist('unit')
        quantity = request.form.getlist ('quantity')

        calorie = 0
        total_fat = 0

        df = pd.read_excel(excel_file)
        df1 = pd.read_excel(excel_file_recipes)
        df2 = pd.read_excel(excel_file_units)

        if recipe:
            
            def recipe_finder(x, y, df):
                return (float)(df.at[x, y])
            
            for i in range (len (df1)):
                if (recipe == (df1.at[i, 'Food Name; name'])):
                    calorie = recipe_finder(i, 'Energy; enerc', df1)
                    total_fat = recipe_finder(i, 'Total Fat; fatce', df1)
                    break
            
            calorie = serving (calorie, serving_size)
            total_fat = serving (total_fat, serving_size)

            return redirect (url_for('result3', rec = recipe, cal = calorie, tf = total_fat, size = serving_size))

        elif any(ingredient):

            serving_weight = []
            serving_weight_updated = []
            calorie_list = []
            total_fat_list = []

            if ingredient != None:
                for i in range (len(ingredient)):
                    for j in range (len(df)):
                        if (ingredient[i] == (df.at[j, 'Food Name; name'])):
                            serving_weight.append((float)(df.at[j, 'Dish Weight (g)']))
                            calorie_list.append((float)(df.at[j, 'Energy; enerc']))
                            total_fat_list.append((float)(df.at[j, 'Total Fat; fatce']))

                for i in range (len(unit)):                                                               # len (unit) = 2, i = 0, i = 1
                    for j in range (len(df2)):                                                            # len (df2) = 
                        if ((str)(unit[i]) == (df2.at[j, 'unit'])):                                       # true, true
                            factor = (float) (df2.at[j, 'value'])                                         # factor = 5, 240
                            value = ((factor * ((float) (quantity [i]))) / serving_weight[i])             # value = 5*1, 240*1
                            serving_weight_updated.append (value)                                         # serving_weight [0] = 5 / 4770, 240 / 13930
                            break


            for i in range (len(serving_weight_updated)):
                calorie = calorie + (calorie_list[i] * serving_weight_updated [i])
                total_fat = total_fat + (total_fat_list [i] * serving_weight_updated [i]) 

            return redirect(url_for('result2', cal = calorie, tf = total_fat))
    else:                                                     #when it is a GET request
        return render_template('format_copy.html')


@app.route("/result2")
def result2():
    #rec = request.args.get("rec")
    cal = request.args.get("cal")
    tf = request.args.get("tf")

    return render_template('result2.html',calorie = cal, total_fat = tf)

@app.route("/searchrecipe", methods = ['GET', 'POST'])
def searchrecipe():
    if request.method == "POST":
        recipe = request.form ['recipe']
        serving_size = request.form ['serving_size']

        def recipe_finder(x, y, df):
            return (float)(df.at[x, y])

        df1 = pd.read_excel(excel_file_recipes)
        for i in range (len (df1)):
            if (recipe == (df1.at[i, 'Food Name; name'])):
                calorie = recipe_finder(i, 'Energy; enerc', df1)
                total_fat = recipe_finder(i, 'Total Fat; fatce', df1)
                break
        
        calorie = serving (calorie, serving_size)
        total_fat = serving (total_fat, serving_size)

        return redirect (url_for('result3', rec = recipe, cal = calorie, tf = total_fat, size = serving_size))
    else:
        return render_template('format2.html')

@app.route("/result3")
def result3():
    rec = request.args.get("rec")
    cal = request.args.get("cal")
    tf = request.args.get("tf")
    size = request.args.get("size")
    return render_template('result3.html', recipe = rec, calorie = cal, serving_size = size, total_fat = tf)

if __name__ == "__main__":                      #why do we do this?
    app.run(debug=True)                         #runs the debugger, such that we see all the errors on the screen itself