import joblib
import re, string
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import nltk

loaded_vectorizer = joblib.load("tfidf_vectorizer.pkl")
loaded_model = joblib.load("best_model.pkl")

nltk.download('stopwords')
nltk.download('wordnet')

stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

def clean_text(text):
    text = text.lower()
    text = re.sub(r'\d+', '', text)
    text = text.translate(str.maketrans('', '', string.punctuation))
    words = text.split()
    words = [word for word in words if word not in stop_words]
    words = [lemmatizer.lemmatize(word) for word in words]
    return ' '.join(words)

def predict_sentiment(text, vectorizer, model):
    clean = clean_text(text)
    X_vec = vectorizer.transform([clean])
    y_pred = model.predict(X_vec)
    if y_pred[0] == 1:
        return "Negatif"
    else:
        return "Positif"


test_text = ""

#sentiment = predict_sentiment(test_text, loaded_vectorizer, loaded_model)

while True:
    user_text = input("Enter review (ketik 'exit' untuk berhenti): ")
    if user_text.lower() == "exit":
        break
    pred = predict_sentiment(user_text, loaded_vectorizer, loaded_model)
    print(f"Sentimen: {pred}\n")

