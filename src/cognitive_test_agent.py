import spacy
import re
import pandas as pd
from collections import Counter

# Load a small NLP model for speed
nlp = spacy.load("en_core_web_sm")

def analyze_verbal_fluency(text):
    """
    Analyzes a verbal fluency test sample for cognitive markers.

    Parameters:
        text (str): The patient's spoken words in a test.

    Returns:
        dict: A dictionary containing analysis results.
    """

    # Preprocess text: Lowercase, remove special characters
    text_clean = re.sub(r'[^a-zA-Z\s]', '', text.lower())
    words = text_clean.split()

    # NLP processing
    doc = nlp(text_clean)

    # Count unique words
    unique_words = set(words)
    unique_word_count = len(unique_words)

    # Detect word repetitions
    word_counts = Counter(words)
    repeated_words = {word: count for word, count in word_counts.items() if count > 1}

    # Measure sentence structure complexity
    sentence_count = len(list(doc.sents))
    avg_sentence_length = len(words) / sentence_count if sentence_count > 0 else 0

    # Generate cognitive markers
    results = {
        "total_words": len(words),
        "unique_word_count": unique_word_count,
        "repeated_words": repeated_words,
        "avg_sentence_length": round(avg_sentence_length, 2)
    }

    return results

# Example Test
if __name__ == "__main__":
    sample_text = "apple banana orange apple grapes lemon banana orange apple"
    analysis = analyze_verbal_fluency(sample_text)
    print("Verbal Fluency Analysis:", analysis)