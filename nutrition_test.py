from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from typing import List, Optional, Union
import pandas as pd

excel_file = r"C:\Users\shamb\OneDrive\Documents\Ashoka University UG\Second Sem\OCaml\.vscode\.vscode\nutrition.xlsx"
excel_file_recipes = r"C:\Users\shamb\Downloads\dishes_nutrition_per_100g.xlsx"
excel_file_units = r"C:\Users\shamb\Downloads\units.xlsx"

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

def serving(x, y):
    y = (float) (y)
    return (x * y)

def multiply(x, y, i):
    return x [i] * y [i]

@app.get("/format", response_class=HTMLResponse)
async def show_form(request: Request):
    return templates.TemplateResponse("format_copy.html", {"request": request})

@app.post("/format", response_class=HTMLResponse)
async def format(
    request: Request,
    recipe: Optional[str] = Form(None),
    serving_size: Union[int, None, str] = Form(None),
    ingredient: Optional[List[str]] = Form(None),
    unit: Optional[List[str]] = Form(None),
    quantity: Optional[List[int]] = Form(None),
):
        recipe = recipe.strip() if recipe else ""
        serving_size = serving_size if serving_size else ""
        ingredient = ingredient or []
        unit = unit or []
        quantity = quantity or []

        calorie = 0
        total_fat = 0
        saturated_fat = 0
        cholesterol = 0
        sodium = 0
        carbs = 0
        fiber = 0
        sugar = 0
        protein = 0
        vitamin_a = 0
        vitamin_c = 0
        calcium = 0
        iron = 0

        df = pd.read_excel(excel_file)
        df2 = pd.read_excel(excel_file_units)

        if recipe:
            return RedirectResponse(url="/searchrecipe", status_code=303)

        elif any(ingredient):
            serving_weight = []
            serving_weight_updated = []
            calorie_list = []
            total_fat_list = []
            saturated_fat_list = []
            cholesterol_list = []
            sodium_list = []
            carbs_list = []
            fiber_list = []
            sugar_list = []
            protein_list = []
            vitamin_a_list = []
            vitamin_c_list = []
            calcium_list = []
            iron_list = []

            for i in range(len(ingredient)):
                for j in range(len(df)):
                    if ingredient[i] == df.at[j, 'Food Name; name']:
                        serving_weight.append(float(df.at[j, 'Dish Weight (g)']))
                        calorie_list.append(float(df.at[j, 'Energy; enerc']))
                        total_fat_list.append(float(df.at[j, 'Total Fat; fatce']))
                        saturated_fat_list.append(float(df.at[j, 'Saturated Fatty acids; fasat']))
                        cholesterol_list.append(float(df.at[j, 'Cholesterol; cholc']))
                        sodium_list.append(float(df.at[j, 'Sodium (Na); na']))
                        carbs_list.append(float(df.at[j, 'Carbohydrate; choavldf']))
                        fiber_list.append(float(df.at[j, 'Dietary Fiber; fibtg']))
                        sugar_list.append(float(df.at[j, 'Free Sugars; fsugar']))
                        protein_list.append(float(df.at[j, 'Protein; protcnt']))
                        vitamin_a_list.append(float(df.at[j, 'Vitamin A; vita']))
                        vitamin_c_list.append(float(df.at[j, 'Ascorbic acids (C); vitc']))
                        calcium_list.append(float(df.at[j, 'Calcium (Ca); ca']))
                        iron_list.append(float(df.at[j, 'Iron (Fe); fe']))

            for i in range(len(unit)):
                for j in range(len(df2)):
                    if str(unit[i]) == df2.at[j, 'unit']:
                        factor = float(df2.at[j, 'value'])
                        q_val = float(quantity[i]) if quantity[i] else 0.0
                        if i < len(serving_weight) and serving_weight[i] != 0:
                            value = (factor * q_val) / serving_weight[i]
                            serving_weight_updated.append(value)
                        else:
                            serving_weight_updated.append(0.0)
                        break

            for i in range(len(serving_weight_updated)):
                calorie += calorie_list[i] * serving_weight_updated[i]
                total_fat += total_fat_list[i] * serving_weight_updated[i]
                saturated_fat += saturated_fat_list[i] * serving_weight_updated[i]
                cholesterol += cholesterol_list[i] * serving_weight_updated[i]
                sodium += sodium_list[i] * serving_weight_updated[i]
                carbs += carbs_list[i] * serving_weight_updated[i]
                fiber += fiber_list[i] * serving_weight_updated[i]
                sugar += sugar_list[i] * serving_weight_updated[i]
                protein += protein_list[i] * serving_weight_updated[i]
                vitamin_a += vitamin_a_list[i] * serving_weight_updated[i]
                vitamin_c += vitamin_c_list[i] * serving_weight_updated[i]
                calcium += calcium_list[i] * serving_weight_updated[i]
                iron += iron_list[i] * serving_weight_updated[i]

                params = {
                "rec": recipe,
                "cal": calorie,
                "tf": total_fat,
                "size": serving_size,
                "sf": saturated_fat,
                "chol": cholesterol,
                "sod": sodium,
                "c": carbs,
                "f": fiber,
                "sug": sugar,
                "pro": protein,
                "vita": vitamin_a,
                "vitc": vitamin_c,
                "calc": calcium,
                "i": iron,
            }

            return RedirectResponse(url=f"/result2?{'&'.join([f'{k}={v}' for k, v in params.items()])}", status_code=303)
        
        if not recipe and not any(ingredient):
            return templates.TemplateResponse("format_copy.html", {
                "request": request,
                "error_message": "Please enter either a recipe or at least one ingredient."
            })

        if any(ingredient) and (not all(quantity) or not all(unit)):
            return templates.TemplateResponse("format_copy.html", {
                "request": request,
                "error_message": "Please fill quantity and unit for all ingredients."
            })
        
        if any(ingredient) and (not all(serving_size)):
            return templates.TemplateResponse("format_copy.html", {
                "request": request,
                "error_message": "Please enter serving size for the recipe."
            })

        return templates.TemplateResponse("format_copy.html", {"request": request})

@app.get("/result2", response_class=HTMLResponse, name="result2")
async def result2(request: Request, cal: float, tf: float, sf: float, chol: float, sod: float, c: float, f: float, sug: float, pro: float, vita: float, vitc: float, calc: float, i: float):
    return templates.TemplateResponse("result2.html", {"request": request, "calorie": cal, "total_fat": tf, "saturated_fat": sf, "cholesterol": chol, "sodium": sod, "carbs": c, "fiber": f, "sugar": sug, "protein": pro, "vitamin_a":vita, "vitamin_c": vitc, "calcium": calc, "iron": i})

@app.post("/searchrecipe")
async def searchrecipe(request: Request, recipe: str = Form(...), serving_size: str = Form(...)):
    df1 = pd.read_excel(excel_file_recipes)

    def recipe_finder(x, y, df):
        return float(df.at[x, y])

    for i in range(len(df1)):
        if recipe == df1.at[i, 'Food Name; name']:
            calorie = recipe_finder(i, 'Energy; enerc', df1)
            total_fat = recipe_finder(i, 'Total Fat; fatce', df1)
            saturated_fat = recipe_finder(i, 'Saturated Fatty acids; fasat', df1)
            cholesterol = recipe_finder(i, 'Cholesterol; cholc', df1)
            sodium = recipe_finder(i, 'Sodium (Na); na', df1)
            carbs = recipe_finder(i, 'Carbohydrate; choavldf', df1)
            fiber = recipe_finder(i, 'Dietary Fiber; fibtg', df1)
            sugar = recipe_finder(i, 'Free Sugars; fsugar', df1)
            protein = recipe_finder(i, 'Protein; protcnt', df1)
            vitamin_a = recipe_finder(i, 'Vitamin A; vita', df1)
            vitamin_c = recipe_finder(i, 'Ascorbic acids (C); vitc', df1)
            calcium = recipe_finder(i, 'Calcium (Ca); ca', df1)
            iron = recipe_finder(i, 'Iron (Fe); fe', df1)

            calorie = serving(calorie, serving_size)
            total_fat = serving(total_fat, serving_size)
            saturated_fat = serving(saturated_fat, serving_size)
            cholesterol = serving(cholesterol, serving_size)
            sodium = serving(sodium, serving_size)
            carbs = serving(carbs, serving_size)
            fiber = serving(fiber, serving_size)
            sugar = serving(sugar, serving_size)
            protein = serving(protein, serving_size)
            vitamin_a = serving(vitamin_a, serving_size)
            vitamin_c = serving(vitamin_c, serving_size)
            calcium = serving(calcium, serving_size)
            iron = serving(iron, serving_size)

            params = {
                "rec": recipe,
                "cal": calorie,
                "tf": total_fat,
                "size": serving_size,
                "sf": saturated_fat,
                "chol": cholesterol,
                "sod": sodium,
                "c": carbs,
                "f": fiber,
                "sug": sugar,
                "pro": protein,
                "vita": vitamin_a,
                "vitc": vitamin_c,
                "calc": calcium,
                "i": iron,
            }
            return RedirectResponse(url=f"/result3?{'&'.join([f'{k}={v}' for k, v in params.items()])}", status_code=303)

    # fallback to form if no match found
    return templates.TemplateResponse("format2.html", {"request": request})

@app.get("/result3", response_class=HTMLResponse)
async def result3(request: Request,
                  rec: str, cal: str, tf: str, size: str, sf: str, chol: str, sod: str,
                  c: str, f: str, sug: str, pro: str, vita: str, vitc: str, calc: str, i: str):

    return templates.TemplateResponse("result3.html", {
        "request": request,
        "recipe": rec,
        "calorie": cal,
        "serving_size": size,
        "total_fat": tf,
        "saturated_fat": sf,
        "cholesterol": chol,
        "sodium": sod,
        "carbs": c,
        "fiber": f,
        "sugar": sug,
        "protein": pro,
        "vitamin_a": vita,
        "vitamin_c": vitc,
        "calcium": calc,
        "iron": i
    })
