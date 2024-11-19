# Text Preprocessing Tool

A web-based application that allows users to preprocess text data from CSV files dynamically. The tool provides various preprocessing options, including cleaning, normalization, noise reduction, and token-level adjustments, tailored for Natural Language Processing (NLP) tasks.

## Features

- **Dynamic File Upload**: Upload a CSV file and select the desired column for preprocessing.
- **Preprocessing Options**:
  - **Preliminary Cleaning**: Remove newlines, tabs, HTML tags, and links.
  - **Text Structure Normalization**: Expand contractions and remove extra whitespace.
  - **Text Simplification**: Remove stopwords and convert text to lowercase.
  - **Noise Reduction**: Remove special characters and accented characters.
  - **Context Refinement**: Correct spelling and reduce character repetition.
  - **Token and Word-Level Adjustments**: Apply lemmatization to normalize words.
- **Preview and Pagination**:
  - View the first 5 rows of the CSV data simultaneously with navigation controls.
  - Updated dynamically after each preprocessing step.
- **Group-Specific Processing**: Apply preprocessing steps by groups for better control.
- **Download Processed Data**: Save the cleaned and preprocessed file locally.

## Getting Started

### Prerequisites

- Python 3.9 or later
- Node.js (optional for development tools)
- Basic understanding of Flask and JavaScript (for development purposes)

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/vbchivu/textPreprocess
   cd textPreprocess
   
2. Set up Python environment:
   ```bash
   python3 -m venv env
   source env/bin/activate    # On Windows, use `env\Scripts\activate`
   
3. Run the Flask backend:
   ```bash
   python backend.py

4. Access the frontend: Open client.html in a browser.

### Preprocessing Steps
1. Preliminary Cleaning
    - Remove Newlines and Tabs: Cleans up unnecessary formatting.
    - Remove HTML Tags: Removes HTML elements using BeautifulSoup.
    - Remove Links: Removes URLs and domain names.
2. Text Structure Normalization
    - Remove Whitespace: Eliminates extra spaces for consistency.
    - Expand Contractions: Converts contractions into their full forms.
3. Text Simplification
    - Remove Stopwords: Removes non-essential words for NLP tasks.
    - Convert to Lowercase: Standardizes text by lowering all characters.
4. Noise Reduction
    - Remove Special Characters: Retains only alphanumeric characters and select punctuation.
    - Remove Accented Characters: Converts accented characters to their ASCII equivalents.
5. Context Refinement
    - Correct Spelling: Fixes spelling errors.
    - Reduce Character Repetition: Limits repeated characters (e.g., "coooool" → "cool").
6. Token and Word-Level Adjustments
    - Lemmatization: Converts words to their base forms (e.g., "running" → "run").

### Contributions
Feel free to contribute by submitting issues or pull requests. For significant changes, please open an issue first to discuss your ideas.
