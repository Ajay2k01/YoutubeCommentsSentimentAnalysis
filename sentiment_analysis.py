import re
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.models import Sequential, load_model
from joblib import dump, load
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer

# Define the text cleaning regex
TEXT_CLEANING_RE = "@\S+|https?:\S+|http?:\S|[^A-Za-z0-9]+"

# Define the sentiment classes
POSITIVE = "POSITIVE"
NEGATIVE = "NEGATIVE"
NEUTRAL = "NEUTRAL"
SENTIMENT_THRESHOLDS = (0.4, 0.7)

# Load the pre-trained sentiment analysis model and tokenizer
KERAS_MODEL = "model.h5"
TOKENIZER_MODEL = "tokenizer.pkl"

model = load_model(KERAS_MODEL)
tokenizer = load(TOKENIZER_MODEL)

# Define the text preprocessing function
def preprocess(text, stem=False):
    text = re.sub(TEXT_CLEANING_RE, ' ', str(text).lower()).strip()
    tokens = []
    for token in text.split():
        if token not in stop_words:
            if stem:
                tokens.append(stemmer.stem(token))
            else:
                tokens.append(token)
    return " ".join(tokens)

# Download NLTK resources (stop words and stemmer)
import nltk
nltk.download('stopwords')

# Set up stop words and stemmer
stop_words = set(stopwords.words("english"))
stemmer = SnowballStemmer("english")

def analyze_sentiment_batch(comments):
    preprocessed_comments = [preprocess(comment) for comment in comments]
    
    # Tokenize and pad the sequences for the entire batch
    sequences = tokenizer.texts_to_sequences(preprocessed_comments)
    padded_sequences = pad_sequences(sequences, maxlen=300)
    
    # Make predictions for the entire batch
    predictions = model.predict(padded_sequences)

    # Classify sentiments based on prediction probabilities
    sentiments = []
    for prediction in predictions:
        if prediction < SENTIMENT_THRESHOLDS[0]:
            sentiment = NEGATIVE
        elif prediction > SENTIMENT_THRESHOLDS[1]:
            sentiment = POSITIVE
        else:
            sentiment = NEUTRAL
        sentiments.append(sentiment)

    return sentiments



