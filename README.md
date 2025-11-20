# AI CV Ranking & Personality Prediction System

This project is an **AI-powered desktop application** built with **Python**, **CustomTkinter**, **Machine Learning**, and **Text Mining**.  
It allows organizations or HR teams to:

- Rank candidates based on their CV
- Predict personality traits using logistic regression
- Score CVs using text analysis (skills, soft skills, certifications, achievements)
- Store results and generate rankings for each job role
- Save each CV locally for record-keeping

---

## 🚀 Features

### 🔹 1. Machine Learning Personality Prediction  
- Uses **Logistic Regression (Multinomial)** to predict personality based on:
  - Gender  
  - Age  
  - Five personality traits (sliders in UI)

### 🔹 2. CV Text Analysis  
Automatically scores CVs based on:
- Technical keywords  
- Soft skills  
- Certifications  
- Achievements

### 🔹 3. Modern Dark-Themed GUI (CustomTkinter)  
- Easy to use  
- Scrollable frame for long forms  
- Upload CVs in `.txt` format  
- Auto-save processed CVs in `/cvs/` folder  

### 🔹 4. Candidate Ranking System  
Generates sorted rankings based on:
- Personality Prediction  
- CV Score  
- Combined Weighted Score  

Displayed in a separate window.

---

## 📂 Project Structure

```plaintext
AI-CV-Ranking/
│
├── .idea/                       # PyCharm / IDE config folder
├── .venv/                       # Virtual environment
├── cvs/                         # Auto-saved candidate CV files
├── Snapshots/                   # Test snapshots or GUI images
├── Test Cases/                  # Test cases provided/created
│
├── main.py                      # Main application code (GUI + ML + Scoring)
├── README.md                    # Project documentation
├── Report.pdf                   # Generated project report
├── requirements.txt             # Python dependencies
├── training_dataset.csv         # Dataset used for model training
├── results.csv                  # Auto-generated CSV of candidate results
└── README                       # (If present) notes or additional explanation

🧠 How It Works
1️⃣ Model Training

The application loads training_dataset.csv and converts gender into numeric values.
Then it trains a Logistic Regression classifier:
self.model = linear_model.LogisticRegression(
    multi_class='multinomial',
    solver='newton-cg',
    max_iter=1000
)

2️⃣ Prediction
When the user enters:
Name, age, gender
Personality slider values
CV text & uploaded file
the app predicts:
Personality class
CV Score (0–100)
Overall Combined Score

3️⃣ Data Saving
After every prediction:
CV is saved in /cvs/
Result is appended to results.csv

4️⃣ Ranking
Users can generate job-role-based rankings sorted by Overall Score.

📊 Technologies Used
Python
CustomTkinter (GUI)
Pandas
Scikit-learn
PyResParser (CV Text Extraction)
Machine Learning
NLP Keyword Scoring

👨‍💻 Author
Zohaib Ali
BSCS Student, COMSATS University Sahiwal
Email: zuhyabali03@gmail.com
