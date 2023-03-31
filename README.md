# PDF Converter with OpenAI GPT-3.5 Integration

This is a web application built with Python and Flask that allows users to upload a PDF file and receive a simplified, humorous explanation of the contents using OpenAI's GPT-3 API. The application uses NLTK to split the PDF text into smaller chunks to stay within the API's maximum token limit, and PyPDF2 to extract the text from the PDF file.

## Prerequisites

To run this application, you will need:

- Python 3.6 or later
- An OpenAI API key

## Installation

1. Clone this repository to your local machine.
2. Install the required packages using pip:

```bash
pip install -r requirements.txt
```

3. Set your OpenAI API key as an environment variable:
```
export OPENAI_API_KEY=your-api-key-here
```

## Frontend
You can find the frontend code for this project at the following link:
[https://github.com/sumitra19jha/PDF-Converter-React-Frontend](https://github.com/sumitra19jha/PDF-Converter-React-Frontend)

Make sure to follow the instructions in the frontend README.md file to set up and run the application.

## Usage
1. Start the Flask server:
```bash
python app.py
```
2. Navigate to frontend(`http://localhost:3000`) in your web browser.
3. Upload a PDF file, and provide a city and country to use in the explanation.
4. Click "Submit" and wait for the GPT-3 API to generate a response.
5. The response will be displayed on the right-hand side of the page, along with page numbers for multi-page PDFs.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
