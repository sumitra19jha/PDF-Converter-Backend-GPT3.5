from io import BytesIO
import os
import tokenize
import PyPDF2
import openai
import nltk
from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

nltk.download('punkt')

def count_tokens(prompt):
    # Convert the prompt to bytes
    prompt_bytes = bytes(prompt, 'utf-8')

    # Use the tokenize module to count the number of tokens
    token_count = 0
    for token in tokenize.tokenize(BytesIO(prompt_bytes).readline):
        if token.type != tokenize.ENDMARKER:
            token_count += 1

    return token_count

def split_prompt(text, max_tokens=1500):
    # Split the text into sentences using NLTK
    sentences = nltk.sent_tokenize(text)

    # Split the sentences into chunks of at most max_tokens
    chunks = []
    current_chunk = []
    current_length = 0
    for sentence in sentences:
        sentence_length = len(sentence.split())
        if current_length + sentence_length <= max_tokens:
            current_chunk.append(sentence)
            current_length += sentence_length
        else:
            chunks.append(current_chunk)
            current_chunk = [sentence]
            current_length = sentence_length
    if current_chunk:
        chunks.append(current_chunk)

    # Join each chunk back into a string
    prompts = []
    for chunk in chunks:
        prompt = ' '.join(chunk)
        prompts.append(prompt)

    return prompts


def extract_paragraphs(text):
    # Split the text into paragraphs
    paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]

    # Join the paragraphs into a single string
    return ' '.join(paragraphs)

@app.route('/convert', methods=['POST'])
def process_pdf():
    # Get the uploaded file from the request
    file = request.files['pdf']

    # Get the city and country parameters from the request
    city = request.form['city']
    country = request.form['country']
    current_page = int(request.form['current_page'])

    # Read the PDF file and extract the text
    pdf_reader = PyPDF2.PdfReader(file)
    page_text = ' '.join(pdf_reader.pages[current_page - 1].extract_text().split())
    
    # Extract paragraphs from the text
    paragraphs = extract_paragraphs(page_text)

    # Make a request to the ChatGPT API
    openai.api_key = os.getenv("OPENAI_API_KEY")
    prompts = split_prompt(paragraphs)
    final_response = ""

    for prompt in prompts:
        final_prompt = "Explain the below pdf content in simpler funny way to an {} sitting in {}. Use country context and decide language yourself. PDF text: {}".format(country, city, prompt)
        
        try:
            response = openai.Completion.create(
                model="text-davinci-003",
                prompt=final_prompt,
                temperature=0.7,
                max_tokens=(4000 - count_tokens(final_prompt)),
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )
            final_response = final_response + response['choices'][0]['text']
        except Exception as e:
            print("OpenAI API error:", str(e))
            return {
                'success': False,
                'error': 'OpenAI API error',
                'message': str(e),
            }

    # Return the message in a JSON response
    if len(final_response) > 0:
        return {
            'success': True,
            'message': "Success",
            'output': final_response,
            "current_page": current_page,
            "total_page": len(pdf_reader.pages),
        }
    else:
        return {
            'success': False,
            'error': 'No responses were received from the OpenAI API',
            'message': "Please try again!",
        }

if __name__ == '__main__':
    app.run(debug=True, port=5000)
