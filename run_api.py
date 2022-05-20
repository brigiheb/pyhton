from flask import Flask
from flask import request
import api_functions
import json
app = Flask(__name__)


@app.route("/result", methods=['POST'])
def get_documents_64():
    request_data = request.get_json()
    file_path = request_data['file_path']
    upload_path = "C:/Users/user/Desktop/hedhy tekhdem/"
    conn = api_functions.connection()
    result = ""
    skills = ""
    if conn is not None:
        COLUMNS_DB = api_functions.get_keys("test", conn)
        text = api_functions.extract_text_from_pdf(upload_path + file_path)
        skills = api_functions.extract_skills(text, COLUMNS_DB)
        result = api_functions.jaccard_similarity(COLUMNS_DB, skills)
        print(skills)
        result =(str(result)+' %')
        print(result)
    json_data = {"result": result, "skills": list(skills)}
    return json_data


if __name__ == '__main__':
    app.run()
