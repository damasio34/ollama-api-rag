import os 
from dotenv import load_dotenv
from flask import Flask, request, jsonify 
from embed import embed 
from query import query 
from get_vector_db import get_vector_db 

#https://hackernoon.com/lang/pt/crie-seu-pr%C3%B3prio-aplicativo-rag,-um-guia-passo-a-passo-para-configurar-o-llm-localmente-usando-ollama-python-e-chromadb
load_dotenv() 

TEMP_FOLDER = os.getenv('TEMP_FOLDER', './_temp') 

os.makedirs(TEMP_FOLDER, exist_ok=True) 
app = Flask(__name__) 

@app.route('/embed', methods=['POST'])
def route_embed(): 
    if 'file' not in request.files: 
        return jsonify({"error": "No file part"}), 400 
    file = request.files['file'] 
    if file.filename == '': 
        return jsonify({"error": "No selected file"}), 400 
    file.save(os.path.join(TEMP_FOLDER, file.filename)) 
    embedded = embed(file) 
    if embedded: 
        return jsonify({"message": "File embedded successfully"}), 200 
    return jsonify({"error": "File embedded unsuccessfully"}), 400 

@app.route('/query', methods=['POST']) 
def route_query(): 
    data = request.get_json() 
    response = query(data.get('query')) 
    if response: 
        return jsonify({"message": response}), 200 
    return jsonify({"error": "Something went wrong"}), 400 

if __name__ == '__main__': 
    app.run(host="0.0.0.0", port=8080, debug=True)