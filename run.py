from flask import Flask, redirect, render_template, request
import pickle

dict_outlet_size = {"medium": 1, "small": 2, "high": 0}
dict_item_fat = {"low_fat": 0, "regular_fat": 1}
dict_location = {"tier1":0, "tier2": 1,"tier3": 2}
dict_outlet_type = {"Supermarket_Type1":1,"Supermarket_Type2":2,"Supermarket_Type3":3, "Grocery_Store": 0}
dict_Item_Type = {"dairy": 4,"soft_drinks": 14,"meat": 10,"Fruits_and_vegetables": 6,"household":9,"baking_goods": 0,"snack_foods": 13,'frozen_foods': 5,"breakfast": 2,"health_and_hygiene": 8,"hard_drinks": 7,"canned": 3,"breads": 1,"starchy_foods": 15,"others": 11,"seafood": 12}
dict_Outlet_Identifier = {"OUT049":9,"OUT018":3,"OUT010":0,"OUT013": 1,"OUT027": 5,"OUT045":7,"OUT017": 2,"OUT046": 8,"OUT035": 6,"OUT019":4}


model = pickle.load(open("Store Sales Prediction.pkl", "rb"))
scaler = pickle.load(open("Standarscaler.pkl", "rb"))

app = Flask(__name__)
@app.route("/", methods = ["POST", "GET"])
def home():
    return render_template("index.html", value = 0, data = [])

@app.route("/predict", methods = ["POST", "GET"])
def predict():
    try:
        if request.method == "POST":
            feature = request.form
            print(feature)
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

            return render_template("index.html", value =value, data = data)
    except:
        return redirect("/")

if __name__ == "__main__":
    app.run(debug= True)