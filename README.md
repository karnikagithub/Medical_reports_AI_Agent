# Medical Report Generator

This project is a medical report generation tool powered by LangChain and Google's Generative AI models. It allows users to input medical queries and generate detailed medical reports in PDF format.

## Features

* **Medical Report Generation:** Generates medical reports from user queries.
* **PDF Output:** Converts generated reports into PDF documents.
* **Base64 Encoding:** Encodes PDFs as base64 strings for easy transmission.
* **Flask Frontend:** Provides a simple web interface for user interaction.
* **Dynamic PDF Naming:** Saves PDFs with filenames derived from user input.
* **Error Handling:** Includes error handling for robust performance.
* **Tool based agent:** Uses LangChain tools to perform specific tasks.

## Prerequisites

* Python 3.7+
* Google Cloud API Key
* Environment variables configured (.env file)

## Installation

1.  Clone the repository:

    ```bash
    git clone <repository_url>
    cd medical-report-generator
    ```

2.  Create a virtual environment (recommended):

    ```bash
    python -m venv venv
    source venv/bin/activate  # On macOS/Linux
    venv\Scripts\activate  # On Windows
    ```

3.  Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4.  Configure environment variables:

    * Create a `.env` file in the project root.
    * Add your Google Cloud API key and email credentials:

        ```
        GOOGLE_API_KEY=your_api_key
        EMAIL_FROM=your_email
        EMAIL_PASSWORD=your_password
        SMTP_SERVER=your_smtp_server
        SMTP_PORT=your_smtp_port
        ```

## Usage

1.  Run the Flask application:

    ```bash
    python app.py
    ```

2.  Open your web browser and go to `http://127.0.0.1:5000/`.

3.  Enter your medical query in the text area and click "Generate Report".

4.  A download link for the generated PDF report will be displayed.

## Project Structure

Markdown

# Medical Report Generator

This project is a medical report generation tool powered by LangChain and Google's Generative AI models. It allows users to input medical queries and generate detailed medical reports in PDF format.

## Features

* **Medical Report Generation:** Generates medical reports from user queries.
* **PDF Output:** Converts generated reports into PDF documents.
* **Base64 Encoding:** Encodes PDFs as base64 strings for easy transmission.
* **Flask Frontend:** Provides a simple web interface for user interaction.
* **Dynamic PDF Naming:** Saves PDFs with filenames derived from user input.
* **Error Handling:** Includes error handling for robust performance.
* **Tool based agent:** Uses LangChain tools to perform specific tasks.

## Prerequisites

* Python 3.7+
* Google Cloud API Key
* Environment variables configured (.env file)

## Installation

1.  Clone the repository:

    ```bash
    git clone <repository_url>
    cd medical-report-generator
    ```

2.  Create a virtual environment (recommended):

    ```bash
    python -m venv venv
    source venv/bin/activate  # On macOS/Linux
    venv\Scripts\activate  # On Windows
    ```

3.  Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4.  Configure environment variables:

    * Create a `.env` file in the project root.
    * Add your Google Cloud API key and email credentials:

        ```
        GOOGLE_API_KEY=your_api_key
        EMAIL_FROM=your_email
        EMAIL_PASSWORD=your_password
        SMTP_SERVER=your_smtp_server
        SMTP_PORT=your_smtp_port
        ```

## Usage

1.  Run the Flask application:

    ```bash
    python app.py
    ```

2.  Open your web browser and go to `http://127.0.0.1:5000/`.

3.  Enter your medical query in the text area and click "Generate Report".

4.  A download link for the generated PDF report will be displayed.

## Project Structure

medical-report-generator/
├── agents/
│   └── medical_agent.py
├── chains/
│   └── retrieval_chain.py
│   └── summarization_chain.py
│   └── report_chain.py
├── tools/
│   ├── pubmed_tool.py
│   ├── nih_tool.py
│   ├── who_tool.py
│   ├── web_scraping_tool.py
│   ├── summarization_tool.py
│   ├── report_generation_tool.py
│   └── email_delivery_tool.py
├── output_parsers/
│   └── medical_output_parser.py
├── templates/
│   └── index.html
├── static/
│   └── style.css
|__ app.py
├── requirements.txt
├── .env
├── README.md


* `agents/`: Contains the LangChain agent.
* `chains/`: Contains LangChain chains used by the tools.
* `tools/`: Contains LangChain tools for specific tasks.
* `output_parsers/`: Contains output parsers for structuring LLM responses.
* `templates/`: Contains HTML templates for the Flask application.
* `static/`: Contains static files (CSS, PDFs).
* `app.py`: The Flask application.
* `requirements.txt`: List of Python dependencies.
* `.env`: Environment variable configuration.
* `README.md`: Project documentation.

## Dependencies

* langchain
* langchain-google-genai
* google-generativeai
* python-dotenv
* requests
* beautifulsoup4
* flask
* reportlab
