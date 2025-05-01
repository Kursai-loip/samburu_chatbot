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
    # Get matches (case-insensitive substring match)
    matches = df[df['samburu'].str.lower().str.contains(user_input.lower())]

    if not matches.empty:
        # Deduplicate based on Samburu + English + POS + Features
        seen = set()
        response = []

        for _, row in matches.iterrows():
            key = (
                str(row["samburu"]).strip().lower(),
                str(row.get("english", "")).strip().lower(),
                str(row.get("part_of_speech", "")).strip().lower(),
                str(row["inflectionfeatures"]).strip().lower()
            )
            if key not in seen:
                seen.add(key)
                response.append({
                    "samburu": row["samburu"],
                    "transcription": row["transcription"],
                    "pos": row.get("part_of_speech", ""),
                    "inflectionfeatures": row["inflectionfeatures"],
                    "english": row.get("english", "")
                })

        # Optionally return only the first match
        if response:
            return [response[0]]  # <-- comment this line if you want all unique matches

        return [{"error": "No unique match found."}]

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
