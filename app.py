from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import pandas as pd

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return render_template('index.html')

# Load your Samburu-English dictionary
import pandas as pd
df = pd.read_excel('data/dictionary.xlsx')

# Basic lookup function
def lookup_word(user_input):
    matches = df[df['samburu'].str.lower().str.contains(user_input.lower())]
    if not matches.empty:
        response = []
        for _, row in matches.iterrows():
            entry = {
                "samburu": row["samburu"],
                "transcription": row["transcription"],
                "pos": row.get("part_of_speech", ""),
                "inflectionfeatures": row["inflectionfeatures"],
                "english": row.get("english", "")
            }
            response.append(entry)
        return response
    return [{"error": "No match found for that word."}]

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.form.get('message')
    if not user_message:
        return jsonify(success=False, error="Empty message."), 400
    
    response_data = lookup_word(user_message)
    return jsonify(success=True, message=response_data)

# if __name__ == '__main__':
    app.run(debug=True)
