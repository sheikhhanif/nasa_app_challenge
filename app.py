# importing modules
import os
import math
import json
from flask import Flask, request
from flask import Flask, redirect, url_for, request, render_template, jsonify
#from flask_restplus import Api, Resource
#from flasgger import Swagger
#from flasgger.utils import swag_from

#from werkzeug.utils import secure_filename
#from flasgger import LazyString, LazyJSONEncoder

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

data = pd.read_csv('nasadata.csv')
data = data.rename(columns = {"Area":"country", "Population (Unit 1000 person)":"population","Forest Land (Unit 1000 ha)":"forestland","Forest CO2 emission rate (Tonnes C/ha)":"CO2emission","Burning Rate":"burn"})
#indo = data.iloc[54:81]
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
    #final_pred = str(pred_data[0])
    final_pred = round(pred_data[0],2)
    #reduce = indo.iloc[0,3] - final_pred
    #years_left = year - 2019
    #per_year_forest = np.around((reduce/years_left), decimals= 2)
    #year_rate = np.around(((per_year_forest*100)/indo.iloc[26,3]), decimals=2)
    #per_tree_cost = 1.5
    #min_tree = 1000
    #number_of_trees = per_year_forest*min_tree
    #total_cost = math.ceil((number_of_trees*per_tree_cost)/1000000)

    #sentence = "Appoximate remaining forest land in " + str(year) + " : " + str(final_pred) + "\n\t\t" + "Total amount of plantations required per year: " + str(per_year_forest) + "\n\t\t\t" + "Total Cost per year" + str(total_cost)
    result = {'year': year, 'area': final_pred, 'amount': average_rate}
    return json.dumps(result)


# Create a Flask instance
app = Flask(__name__)
@app.route('/predict', methods=['POST'])
def upload():
    """
    Serve the inference request
    Pass the image in multipart/form-data to the inference function
    """
    if request.method == 'POST':

      # Get the file from post request
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