import re
import pandas as pd
import unidecode
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, WhitespaceTokenizer
from nltk.stem import WordNetLemmatizer
from autocorrect import Speller
from bs4 import BeautifulSoup
import nltk
import contraction_map as CONTRACTION_MAP

# Download necessary NLTK resources
nltk.download('stopwords')
nltk.download('wordnet')

# Global configurations
STOPLIST = set(stopwords.words('english'))
SPELL = Speller(lang='en')
LEMMATIZER = WordNetLemmatizer()
TOKENIZER = WhitespaceTokenizer()

### Preprocessing Utilities Functions
def remove_newlines_tabs(text):
    """Remove newlines, tabs, and unnecessary slashes."""
    return text.replace('\\n', ' ').replace('\n', ' ').replace('\t', ' ').replace('\\', ' ').replace('. com', '.com')

def strip_html_tags(text):
    """Remove HTML tags using BeautifulSoup."""
    soup = BeautifulSoup(text, "html.parser")
    return soup.get_text(separator=" ")

def remove_links(text):
    """Remove URLs and domain names."""
    text = re.sub(r'http\S+', '', text)
    return re.sub(r"\ [A-Za-z]*\.com", " ", text)

def remove_whitespace(text):
    """Remove extra whitespace and handle special cases."""
    text = re.sub(r'\s+', ' ', text)
    return text.replace('?', ' ? ').replace(')', ') ')

def accented_characters_removal(text):
    """Convert accented characters to their ASCII equivalents."""
    return unidecode.unidecode(text)

def lower_casing_text(text):
    """Convert text to lowercase."""
    return text.lower()

def reducing_incorrect_character_repeatation(text):
    """Reduce repeated characters and punctuations."""
    text = re.sub(r"([A-Za-z])\1{1,}", r"\1\1", text)
    return re.sub(r'([.,/#!$%^&*?;:{}=_`~()+-])\1{1,}', r'\1', text)

def expand_contractions(text):
    """Expand contracted forms in the text."""
    tokens = text.split(' ')
    return ' '.join([CONTRACTION_MAP.get(word, word) for word in tokens])

def removing_special_characters(text):
    """Remove special characters while retaining important punctuation."""
    return re.sub(r"[^a-zA-Z0-9:$-,%.?!]+", ' ', text)

def removing_stopwords(text):
    """Remove stopwords from the text."""
    return ' '.join([word for word in word_tokenize(text) if word.lower() not in STOPLIST])

def spelling_correction(text):
    """Correct spelling using Autocorrect."""
    return SPELL(text)

def lemmatization(text):
    """Perform lemmatization on tokens."""
    return ' '.join([LEMMATIZER.lemmatize(token, 'v') for token in TOKENIZER.tokenize(text)])

### Main Preprocessing Pipeline
def text_preprocessing(
    text, 
    accented_chars=True, 
    contractions=True, 
    lemma=True, 
    extra_whitespace=True, 
    newlines_tabs=True, 
    repeatition=True,
    lowercase=True, 
    punctuations=True, 
    mis_spell=True,
    remove_html=True, 
    links=True,  
    special_chars=True, 
    stop_words=False,
    contraction_map={},
    **kwargs
):
    """Perform text preprocessing based on the provided options."""
    if newlines_tabs:
        text = remove_newlines_tabs(text)
    if remove_html:
        text = strip_html_tags(text)
    if links:
        text = remove_links(text)
    if extra_whitespace:
        text = remove_whitespace(text)
    if accented_chars:
        text = accented_characters_removal(text)
    if lowercase:
        text = lower_casing_text(text)
    if repeatition:
        text = reducing_incorrect_character_repeatation(text)
    if contractions:
        text = expand_contractions(text)
    if punctuations:
        text = removing_special_characters(text)
    if stop_words:
        text = removing_stopwords(text)
    if mis_spell:
        text = spelling_correction(text)
    if lemma:
        text = lemmatization(text)
    return text

### Preprocessing Function Mapping
PREPROCESSING_FUNCTIONS = {
    "remove_newlines_tabs": remove_newlines_tabs,
    "strip_html_tags": strip_html_tags,
    "remove_links": remove_links,
    "remove_whitespace": remove_whitespace,
    "accented_characters_removal": accented_characters_removal,
    "lower_casing_text": lower_casing_text,
    "reducing_incorrect_character_repeatation": reducing_incorrect_character_repeatation,
    "expand_contractions": lambda text: expand_contractions(text),
    "removing_special_characters": removing_special_characters,
    "removing_stopwords": removing_stopwords,
    "spelling_correction": spelling_correction,
    "lemmatization": lemmatization,
}

def apply_preprocessing(text, options):
    """Dynamically apply selected preprocessing steps."""
    for option, enabled in options.items():
        if enabled and option in PREPROCESSING_FUNCTIONS:
            text = PREPROCESSING_FUNCTIONS[option](text)
    return text