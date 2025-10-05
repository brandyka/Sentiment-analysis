# Script untuk investigasi kenapa model classes jadi [1,2]

import os
import joblib
from datetime import datetime
import pandas as pd

print("🕵️ INVESTIGASI: Kenapa Model Classes Jadi [1,2]?")
print("="*60)

# 1. Cek file timestamps
files_to_check = [
    "tfidf_vectorizer.pkl", 
    "best_model.pkl",
    "app.py"  # atau main backend file
]

print("\n📅 1. TIMESTAMP FILES:")
for file in files_to_check:
    if os.path.exists(file):
        timestamp = os.path.getmtime(file)
        date_modified = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
        size = os.path.getsize(file)
        print(f"   {file}: {date_modified} ({size} bytes)")
    else:
        print(f"   {file}: ❌ Not found")

# 2. Load dan inspect model
print("\n🔬 2. MODEL INSPECTION:")
try:
    model = joblib.load("best_model.pkl")
    vectorizer = joblib.load("tfidf_vectorizer.pkl")
    
    print(f"   Model type: {type(model)}")
    print(f"   Model classes: {model.classes_}")
    print(f"   Vectorizer type: {type(vectorizer)}")
    
    if hasattr(model, 'get_params'):
        params = model.get_params()
        print(f"   Random state: {params.get('random_state', 'Not set')}")
        print(f"   Class weight: {params.get('class_weight', 'None')}")

except Exception as e:
    print(f"   ❌ Error loading model: {e}")

# 3. Cek apakah ada backup files
print("\n💾 3. BACKUP FILES CHECK:")
backup_patterns = [
    "*.pkl.bak", "backup_*.pkl", "*_old.pkl", 
    "model_*.pkl", "*_backup.pkl"
]

import glob
found_backups = []
for pattern in backup_patterns:
    found_backups.extend(glob.glob(pattern))

if found_backups:
    print("   📦 Found backup files:")
    for backup in found_backups:
        timestamp = os.path.getmtime(backup)
        date_modified = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
        print(f"      {backup}: {date_modified}")
else:
    print("   ❌ No backup files found")

# 4. Cek training script kalau ada
print("\n📝 4. TRAINING SCRIPT CHECK:")
training_files = ["train.py", "training.py", "model_training.py", "train_model.py"]
for file in training_files:
    if os.path.exists(file):
        print(f"   ✅ Found: {file}")
        # Cek isi file untuk label mapping
        try:
            with open(file, 'r') as f:
                content = f.read()
                if 'label' in content.lower():
                    print(f"      - Contains 'label' references")
                if any(pattern in content for pattern in ['map()', 'mapping', 'replace()']):
                    print(f"      - Contains mapping/transformation code")
                if '1.*2' in content or '2.*1' in content:
                    print(f"      - ⚠️  Might have 1,2 label references")
        except:
            pass
    else:
        print(f"   ❌ Not found: {file}")

# 5. Cek data source
print("\n📊 5. DATA SOURCE CHECK:")
data_files = [
    "data.csv", "dataset.csv", "training_data.csv", 
    "sentiment_data.csv", "reviews.csv"
]

for file in data_files:
    if os.path.exists(file):
        print(f"   ✅ Found: {file}")
        try:
            # Peek at first few rows
            df = pd.read_csv(file, nrows=5)
            print(f"      Columns: {list(df.columns)}")
            
            # Check for label column
            label_cols = [col for col in df.columns if 'label' in col.lower() or 'sentiment' in col.lower()]
            if label_cols:
                for col in label_cols:
                    unique_vals = df[col].unique()
                    print(f"      {col} values: {unique_vals}")
                    
        except Exception as e:
            print(f"      ❌ Error reading: {e}")

# 6. Cek database untuk clues
print("\n🗃️  6. DATABASE CLUES:")
try:
    import mysql.connector
    db = mysql.connector.connect(
        host="localhost", user="root", 
        password="qwertyuiop", database="sentiment_db"
    )
    cursor = db.cursor()
    
    # Cek semua nilai prediction yang pernah ada
    cursor.execute("SELECT DISTINCT prediction FROM sentiment_results ORDER BY prediction")
    predictions = [row[0] for row in cursor.fetchall()]
    print(f"   Unique predictions in DB: {predictions}")
    
    # Cek kapan pertama kali muncul prediction = 2
    cursor.execute("""
        SELECT MIN(created_at) as first_time, COUNT(*) as count 
        FROM sentiment_results 
        WHERE prediction = 2
    """)
    result = cursor.fetchone()
    if result and result[0]:
        print(f"   First prediction=2: {result[0]} (total: {result[1]})")
    
    db.close()
    
except Exception as e:
    print(f"   ❌ Database error: {e}")

print("\n💡 KESIMPULAN:")
print("Kemungkinan penyebab model classes berubah:")
print("1. 📊 Dataset training menggunakan label 1,2 bukan 0,1")
print("2. 🔄 Model di-retrain dengan data yang berbeda")  
print("3. 📁 File model ter-overwrite dengan model lain")
print("4. ⚠️  Scikit-learn version mismatch (1.6.1 -> 1.7.2)")
print("5. 🐛 Bug di preprocessing yang map label salah")
print("\n🔧 Solusi sudah disediakan di script sebelumnya!")