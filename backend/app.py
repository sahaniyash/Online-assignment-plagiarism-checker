from flask import Flask, request, jsonify
from flask_cors import CORS
import PyPDF2
import os
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

app = Flask(__name__)
CORS(app, resources={r"/check-plagiarism": {"origins": "*"}})  # Enable CORS

app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def extract_text_from_pdf(pdf_file):
    pdf_text = ''
    try:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            pdf_text += page.extract_text()
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
    return pdf_text

def text_preprocessing(text):
    tokens = word_tokenize(text)
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if word.lower() not in stop_words]
    return tokens

def calculate_similarity(text1, text2):
    tokens1 = text_preprocessing(text1)
    tokens2 = text_preprocessing(text2)

    if not tokens1 or not tokens2:
        return 0.0

    intersection = len(set(tokens1) & set(tokens2))
    union = len(set(tokens1) | set(tokens2))
    similarity = intersection / union
    return similarity

@app.route('/check-plagiarism', methods=['POST'])
def check_plagiarism():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    files = request.files.getlist('file')

    if not files:
        return jsonify({'error': 'No selected files'})

    plagiarism_results = []

    for file1 in files:
        file1.save(os.path.join(app.config['UPLOAD_FOLDER'], file1.filename))
        pdf_path1 = os.path.join(app.config['UPLOAD_FOLDER'], file1.filename)
        text1 = extract_text_from_pdf(pdf_path1)

        results = []
        for file2 in files:
            if file1 == file2:
                continue  # Skip comparing the file to itself

            pdf_path2 = os.path.join(app.config['UPLOAD_FOLDER'], file2.filename)
            if not os.path.exists(pdf_path2):  # Save file2 if not already saved
                file2.save(pdf_path2)

            text2 = extract_text_from_pdf(pdf_path2)

            similarity = calculate_similarity(text1, text2)
            results.append({'file': file2.filename, 'plagiarism': similarity})

        plagiarism_results.append({'file': file1.filename, 'results': results})
        os.remove(pdf_path1)

    # Clean up all remaining files in the upload directory
    for file in files:
        pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        if os.path.exists(pdf_path):
            os.remove(pdf_path)

    response_data = {'plagiarism_results': plagiarism_results}
    return jsonify(response_data), 200, {'Content-Type': 'application/json'}

if __name__ == '__main__':
    app.run(debug=True)
