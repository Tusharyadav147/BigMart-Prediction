from flask import Flask, redirect, render_template, request
import sqlite3
import pickle

connection = sqlite3.connect("datastore.db", check_same_thread=False)
cursor = connection.cursor()

dict_outlet_size = {"medium": 1, "small": 2, "high": 0}
dict_item_fat = {"low_fat": 0, "regular_fat": 1}
dict_location = {"tier1":0, "tier2": 1,"tier3": 2}
dict_outlet_type = {"Supermarket_Type1":1,"Supermarket_Type2":2,"Supermarket_Type3":3, "Grocery_Store": 0}
dict_Item_Type = {"dairy": 4,"soft_drinks": 14,"meat": 10,"Fruits_and_vegetables": 6,"household":9,"baking_goods": 0,"snack_foods": 13,'frozen_foods': 5,"breakfast": 2,"health_and_hygiene": 8,"hard_drinks": 7,"canned": 3,"breads": 1,"starchy_foods": 15,"others": 11,"seafood": 12}
dict_Outlet_Identifier = {"OUT049":9,"OUT018":3,"OUT010":0,"OUT013": 1,"OUT027": 5,"OUT045":7,"OUT017": 2,"OUT046": 8,"OUT035": 6,"OUT019":4}


model = pickle.load(open("BigMart Prediction Model.pkl", "rb"))
scaler = pickle.load(open("Standarscaler.pkl", "rb"))

app = Flask(__name__)
@app.route("/", methods = ["POST", "GET"])
def home():
    return render_template("login.html")

@app.route("/index", methods = ["POST", "GET"])
def index():
    return render_template("index.html")

@app.route("/loginresult", methods = ["POST", "GET"])
def login():
    try:
        if request.method == "POST":
            details = request.form
            email = details["email"]
            password = details["password"]
            print(email)
            print(password)
            if email == "admin147@master.com" and password == "Admin4u$":
                return render_template("index.html")
            else:
                return redirect("/")
    except:
        return redirect("/")

@app.route("/predict", methods = ["POST", "GET"])
def predict():
    try:
        if request.method == "POST":
            cursor = connection.cursor()

            feature = request.form
            Item_Identifier = feature["Item_Identifier"]
            Item_Weight = float(feature["Item_weight"])
            Item_Fat_Content = dict_item_fat[feature["Item_Fat_Content"]]
            Item_Visibility = float(feature["Item_Visibility"])
            Item_Type = dict_Item_Type[feature["Item_Type"]]
            Item_MRP = float(feature["Item_MRP"])
            Outlet_Identifier = dict_Outlet_Identifier[feature["Outlet_Identifier"]]
            Outlet_Establishment_Year = float(feature["Outlet_Establishment_Year"])
            Outlet_Size = dict_outlet_size[feature["Outlet_Size"]]
            Outlet_Location_Type = dict_location[feature["Outlet_Location_Type"]]
            Outlet_Type = dict_outlet_type[feature["Outlet_Type"]]
    
            data = []
            for i in request.form.values():
                data.append(i)
                
            scaled = scaler.transform([[Item_Weight,Item_Fat_Content,Item_Visibility,Item_Type,Item_MRP,Outlet_Identifier,Outlet_Establishment_Year,Outlet_Size,Outlet_Location_Type,Outlet_Type]])
            value = model.predict(scaled)[0]

            cursor.execute('INSERT INTO BigMartData values(?,?,?,?,?,?,?,?,?,?,?,?)',(Item_Identifier,Item_Weight, feature["Item_Fat_Content"] , Item_Visibility, feature["Item_Type"], Item_MRP, feature["Outlet_Identifier"], Outlet_Establishment_Year,feature["Outlet_Size"], feature["Outlet_Location_Type"], feature["Outlet_Type"], float(value)))
            connection.commit()
            for i in cursor.execute("SELECT * FROM BigMartData"):
                print(i)
            cursor.close()

            return render_template("result.html", value =value, data = data)
    except Exception as e:
        print(e)
        return redirect("/")

@app.route("/table", methods = ["POST", "GET"])
def table():
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM BigMartData")
        r = cursor.fetchall()
        cursor.close()
        return render_template("table.html", value = r,)
    except:
        return redirect("/")

if __name__ == "__main__":
    app.run(debug= True)