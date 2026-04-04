import joblib
import re, string, mysql.connector
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import nltk
from flask import Flask, render_template, request, jsonify
from wordcloud import WordCloud
from datetime import datetime
import os

app = Flask(__name__)

#-----DB connect-----
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="qwertyuiop",
    database="sentiment_db"
)
cursor = db.cursor()

#-----Loaded model and vectorizer----
loaded_vectorizer = joblib.load("tfidf_vectorizer.pkl")
loaded_model = joblib.load("best_model.pkl")

#------NLTK setup-------
nltk.download('stopwords')
nltk.download('wordnet')
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

# -------- Text Cleaner --------
def clean_text(text):
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(r'\d+', '', text)  # hapus angka
    text = re.sub(r"http\S+", "", text)  # hapus link
    text = text.translate(str.maketrans("", "", string.punctuation))  # hapus tanda baca
    words = text.split()
    words = [word for word in words if word not in stop_words]
    words = [lemmatizer.lemmatize(word) for word in words]
    return " ".join(words)

# -------- Sentiment Predictor --------
def predict_sentiment(text, vectorizer, model):
    clean = clean_text(text)
    X_vec = vectorizer.transform([clean])
    y_pred = model.predict(X_vec)
    return int(y_pred[0])   # 1 = negative, 2 = positif

# -------- Home --------
@app.route("/")
def home():
    return render_template("index.html")

# -------- Dashboard --------
@app.route("/dashboard")
def dashboard():
    mode = request.args.get("mode", "overall")  # default overall

    # --- filter ---
    if mode == "today":
        filter_total = "WHERE DATE(created_at) = CURDATE()"
        filter_pred = "AND DATE(created_at) = CURDATE()"
    else:
        filter_total = ""
        filter_pred = ""

    # --- Total ---
    cursor.execute(f"SELECT COUNT(*) FROM sentiment_results {filter_total}")
    total_reviews = cursor.fetchone()[0] or 0

    # --- Positive ---
    cursor.execute(f"SELECT COUNT(*) FROM sentiment_results WHERE prediction = 2 {filter_pred}")
    positive_count = cursor.fetchone()[0] or 0

    # --- Negative ---
    cursor.execute(f"SELECT COUNT(*) FROM sentiment_results WHERE prediction = 1 {filter_pred}")
    negative_count = cursor.fetchone()[0] or 0

    # --- Percentage ---
    positive_percentage = round((positive_count / total_reviews) * 100, 1) if total_reviews > 0 else 0
    negative_percentage = round((negative_count / total_reviews) * 100, 1) if total_reviews > 0 else 0

    # --- Recent reviews ---
    cursor.execute(f"""
        SELECT text_input, prediction, created_at 
        FROM sentiment_results 
        {filter_total}
        ORDER BY created_at DESC 
        LIMIT 5
    """)
    rows = cursor.fetchall()
    recent_reviews = []
    for r in rows:
        created_at = r[2]
        if isinstance(created_at, str):
            created_at = datetime.strptime(created_at, "%Y-%m-%d %H:%M:%S")
        recent_reviews.append({
            "text": r[0],
            "prediction": r[1],
            "time": created_at.strftime("%Y-%m-%d %H:%M:%S")
        })

    # --- Trend data ---
    if mode == "today":
        cursor.execute("""
            SELECT HOUR(created_at),
                   SUM(CASE WHEN prediction = 2 THEN 2 ELSE 1 END) as positive,
                   SUM(CASE WHEN prediction = 1 THEN 2 ELSE 1 END) as negative,
                   ROUND(AVG(prediction) * 100, 2) as sentiment_score
            FROM sentiment_results
            WHERE DATE(created_at) = CURDATE()
            GROUP BY HOUR(created_at)
            ORDER BY HOUR(created_at)
        """)
        trend_rows = cursor.fetchall()
        trend_labels = [f"{int(r[0])}:00" for r in trend_rows]
    else:
        cursor.execute("""
            SELECT DATE(created_at),
                   SUM(CASE WHEN prediction = 2 THEN 2 ELSE 1 END) as positive,
                   SUM(CASE WHEN prediction = 1 THEN 2 ELSE 1 END) as negative,
                   ROUND(AVG(prediction) * 100, 2) as sentiment_score
            FROM sentiment_results
            GROUP BY DATE(created_at)
            ORDER BY DATE(created_at) DESC
            LIMIT 7
        """)
        trend_rows = cursor.fetchall()
        trend_labels = [str(r[0]) for r in trend_rows[::-1]]

    trend_positive = [r[1] for r in trend_rows[::-1]]
    trend_negative = [r[2] for r in trend_rows[::-1]]
    trend_score = [float(r[3]) for r in trend_rows[::-1]]

    # --- Word Cloud Data ---
    cursor.execute(f"SELECT text_input, prediction FROM sentiment_results {filter_total}")
    texts = cursor.fetchall()
    pos_text = " ".join([clean_text(t[0]) for t in texts if t[1] == 2])
    neg_text = " ".join([clean_text(t[0]) for t in texts if t[1] == 1])

    if pos_text.strip():
        wc_pos = WordCloud(width=500, height=300, background_color="white", colormap="Greens").generate(pos_text)
        wc_pos.to_file(os.path.join("static", "wordcloud_positive.png"))

    if neg_text.strip():
        wc_neg = WordCloud(width=500, height=300, background_color="white", colormap="Reds").generate(neg_text)
        wc_neg.to_file(os.path.join("static", "wordcloud_negative.png"))

    today = datetime.now().strftime("%Y-%m-%d")

    return render_template(
        "dashboard.html",
        mode=mode,
        total_reviews=total_reviews,
        positive_count=positive_count,
        negative_count=negative_count,
        positive_percentage=positive_percentage,
        negative_percentage=negative_percentage,
        recent_reviews=recent_reviews,
        trend_labels=trend_labels,
        trend_positive=trend_positive,
        trend_negative=trend_negative,
        trend_score=trend_score,
        today=today,
        wordcloud_pos="wordcloud_positive.png",
        wordcloud_neg="wordcloud_negative.png"
    )

# -------- API Predict --------
@app.route("/api/predict", methods=["POST"])
def api_predict():
    data = request.get_json(silent=True) or request.form
    text = data.get("text", "") if data else ""
    if not text or not text.strip():
        return jsonify({"error": "text is required"}), 400
    
    # Pred Model
    pred = predict_sentiment(text, loaded_vectorizer, loaded_model)

    # Datetime
    created_at = datetime.now()

    # save to db
    sql = "INSERT INTO sentiment_results (text_input, prediction, created_at) VALUES (%s, %s, %s)"
    val = (text, pred, created_at)
    cursor.execute(sql, val)
    db.commit()

    return jsonify({
        "text": text,
        "message": "Terimakasih atas review anda",
        "created_at": created_at.strftime("%Y-%m-%d %H:%M:%S")
    })

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
