from flask import Flask, request, jsonify
from flask_cors import CORS
import PyPDF2
from io import BytesIO
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

nltk.download('stopwords')
nltk.download('punkt')
nltk.download('punkt_tab')

app = Flask(__name__)
CORS(app, resources={r"/check-plagiarism": {"origins": "*"}})  # Enable CORS

@app.after_request
def set_referrer_policy(response):
    response.headers["Referrer-Policy"] = "no-referrer-when-downgrade"
    return response

def extract_text_from_pdf(pdf_file):
    """Extract text from a PDF file."""
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
    """Preprocess text by tokenizing and removing stopwords."""
    tokens = word_tokenize(text)
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if word.lower() not in stop_words]
    return tokens

def calculate_similarity(text1, text2):
    """Calculate Jaccard similarity between two texts."""
    tokens1 = text_preprocessing(text1)
    tokens2 = text_preprocessing(text2)

    if not tokens1 or not tokens2:
        return 0.0

    intersection = len(set(tokens1) & set(tokens2))
    union = len(set(tokens1) | set(tokens2))
    similarity = intersection / union
    return similarity

def process_files(files):
    """Process and compare all uploaded files."""
    file_contents = {file.filename: extract_text_from_pdf(BytesIO(file.read())) for file in files}
    results = []

    for filename1, text1 in file_contents.items():
        file_results = []
        for filename2, text2 in file_contents.items():
            if filename1 != filename2:  # Skip self-comparison
                similarity = calculate_similarity(text1, text2)
                file_results.append({'file': filename2, 'plagiarism': round(similarity * 100, 2)})
        results.append({'file': filename1, 'results': file_results})
    return results

@app.route('/check-plagiarism', methods=['POST'])
def check_plagiarism():
    """API endpoint for checking plagiarism."""
    if 'file' not in request.files:
        return jsonify({'error': 'No file part provided'}), 400

    files = request.files.getlist('file')

    if not files:
        return jsonify({'error': 'No selected files'}), 400

    # Process files and calculate plagiarism
    plagiarism_results = process_files(files)

    return jsonify({'plagiarism_results': plagiarism_results}), 200

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
