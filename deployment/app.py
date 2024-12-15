from flask import Flask, render_template, request, jsonify
from deployment.pipeline.optimization_pipeline import OptimizationPipeline
import numpy as np
app = Flask(__name__)

@app.route("/")
def home_page():
    return render_template("index.html")

@app.route("/predict", methods=["GET","POST"])
def prediction():
    if request.method == "POST":
        product_id = request.form["product_id"]
        product_category_name = request.form["product_category_name"]
        
        freight_price = float(request.form["freight_price"])
        unit_price = float(request.form["unit_price"])
        comp_1 = float(request.form["comp_1"])
        ps1 = float(request.form["ps1"])
        fp1 = float(request.form["fp1"])
        comp_2 = float(request.form["comp_2"])
        ps2 = float(request.form["ps2"])
        fp2 = float(request.form["fp2"])
        comp_3 = float(request.form["comp_3"])
        ps3 = float(request.form["ps3"])
        fp3 = float(request.form["fp3"])
        lag_price = float(request.form["lag_price"])
        year = float(request.form["year"])
        month = float(request.form["month"])

        data = np.array([[product_id, product_category_name, freight_price, unit_price, comp_1, ps1, fp1, comp_2, ps2, fp2, comp_3, ps3, fp3, lag_price, year, month]])
        optimization_pipeline = OptimizationPipeline()
        predicted_sales = optimization_pipeline.predict(data)
    
        return render_template("predict.html", predicted_sales = predicted_sales)
    else:
        return render_template("input.html")
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)