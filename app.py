# importing modules
import os
import math
import json
from flask import Flask, request
from flask import Flask, redirect, url_for, request, render_template, jsonify

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

data = pd.read_csv('nasadata.csv')
data = data.rename(columns = {"Area":"country", "Population (Unit 1000 person)":"population","Forest Land (Unit 1000 ha)":"forestland","Forest CO2 emission rate (Tonnes C/ha)":"CO2emission","Burning Rate":"burn"})
data['forestland'] = data['forestland'] * 1000
data['burning_rate'] = (data['burn'] * 100) / data['forestland']
average_rate = data['burning_rate'].mean()
average_rate = round(average_rate,2)
features = ['Year']
x = data[features]
y = data.forestland
indo_model = LinearRegression()
indo_model.fit(x,y)



def predict(year):
    test = np.array([[year]])
    pred_data = indo_model.predict(test)
    pred_data  = pred_data/1000000
    final_pred = round(pred_data[0],2)
    result = {'year': year, 'area': final_pred, 'amount': average_rate}
    return json.dumps(result)


# Create a Flask instance
app = Flask(__name__)
@app.route('/predict', methods=['POST'])
def upload():
    if request.method == 'POST':
        num = request.form['year']
        new_num = int(num)
        return predict(new_num)
    return 'not success'

# Start the web server
@app.route('/', methods=['GET'])
def index():
    # Main page
    return render_template('index.html')
if __name__ == '__main__':
    app.run()
