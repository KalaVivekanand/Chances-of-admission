# importing the necessary dependencies

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS, cross_origin
import pickle

app = Flask(__name__)  # initiating a flask app


@app.route('/', methods=['GET'])  # route to display the home page
@cross_origin()
def homePage():
    return render_template('index.html')


@app.route('/predict', methods=['POST', 'GET'])  # route to show the predictions in the web UI
@cross_origin()
def index():
    if request.method == 'POST':
        try:
            # reading the inputs given by the user
            gre_score = float(request.form['gre_score'])
            toefl_score = float(request.form['toefl_score'])
            university_rating = float(request.form['university_rating'])
            sop = float(request.form['sop'])
            lor = float(request.form['lor'])
            cgpa = float(request.form['cgpa'])
            is_research = request.form['research']
            print('Fine Here')
            if is_research.lower() == 'yes':
                research = 1
            else:
                research = 0
            filename = 'finalized_model.pickle'
            loaded_model = pickle.load(open(filename, 'rb'))  # loading the model file from storage
            print("Second : Fine")
            # predictions using the loaded model file
            prediction = loaded_model.predict(
                [[gre_score, toefl_score, university_rating, sop, lor, cgpa, float(research)]])

            print('Prediction is ', prediction)

            # showing the prediction result in the UI

            return render_template('results.html', prediction=round(100 * float(prediction[0])))
        except Exception as e:
            print('The exception message is : ', e)
            return 'Something is wrong'

    else:
        return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)
