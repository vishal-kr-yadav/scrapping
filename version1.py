from flask import Flask
from flask import jsonify
from flask_jsonpify import jsonpify


from scrapping_of_ethereum import ethereum
app=Flask(__name__)

@app.route('/GET/ethereum',methods=['GET'])
def getethereum():

    return ethereum().to_json(orient='records')



if __name__ == '__main__':
    app.run(debug=True)