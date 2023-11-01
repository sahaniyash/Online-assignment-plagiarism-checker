from flask import Flask, request, jsonify
from flask_cors import CORS
import PyPDF2
import os
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

app = Flask(__name__)
CORS(app, resources={r"/check-plagiarism":{"origins": "*"}})  # Enable CORS

app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def extract_text_from_pdf(pdf_file):
    pdf_text = ''
    try:
        pdf_reader = PyPDF2.PdfFileReader(pdf_file)
        for page_num in range(pdf_reader.getNumPages()):
            page = pdf_reader.getPage(page_num)
            pdf_text += page.extractText()
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

            file2.save(os.path.join(app.config['UPLOAD_FOLDER'], file2.filename))
            pdf_path2 = os.path.join(app.config['UPLOAD_FOLDER'], file2.filename)
            text2 = extract_text_from_pdf(pdf_path2)

            similarity = calculate_similarity(text1, text2)
            results.append({'file': file2.filename, 'plagiarism': similarity})

            os.remove(pdf_path2)

        plagiarism_results.append({'file': file1.filename, 'results': results})
        os.remove(pdf_path1)

    response_data = {'plagiarism_results': plagiarism_results}
    return jsonify(response_data), 200, {'Content-Type': 'application/json'}

if __name__ == '__main__':
    app.run(debug=True)
