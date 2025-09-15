from flask import Flask, render_template, request, jsonify
from text_processor import MedicalTextProcessor
from ai_helper import AIHelper
import os

app = Flask(__name__)

# Initialize AI Helper and Medical Text Processor
API_KEY = os.getenv("GEMINI_API_KEY")
ai_helper = AIHelper(API_KEY) if API_KEY else None
processor = MedicalTextProcessor()
# Assumes 'medical_vocabulary.txt' is in the same directory
processor.load_corpus_from_txt('medical_vocabulary.txt')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check_spelling', methods=['POST'])
def check_spelling():
    data = request.get_json()
    word = data.get('word', '')
    if not word:
        return jsonify({'error': 'No word provided.'}), 400

    # Get suggestions and check if the word is known
    suggestions = processor.get_suggestions(word.lower()) #
    is_known = processor.is_known(word) #
    
    # Get the unambiguous correction for the word
    autocorrection = processor.get_unambiguous_correction(word.lower()) #
    
    return jsonify({
        'suggestions': suggestions,
        'is_known': is_known,
        'autocorrection': autocorrection
    })

@app.route('/analyze', methods=['POST'])
def analyze():
    if not ai_helper or not ai_helper.is_ready(): #
        return jsonify({'error': 'AI Assistant is not available. Please set the GEMINI_API_KEY environment variable.'}), 503
    
    data = request.get_json()
    text = data.get('text', '')
    if not text:
        return jsonify({'error': 'No text provided.'}), 400

    result = ai_helper.analyze_text(text) #
    
    return jsonify({'result': result})

if __name__ == '__main__':
    if not API_KEY:
        print("Warning: GEMINI_API_KEY environment variable not found. AI features will be disabled.")
    app.run(debug=True)