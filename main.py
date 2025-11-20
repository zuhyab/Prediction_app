import os
import pandas as pd
import customtkinter as ctk
from tkinter import filedialog, messagebox
from sklearn import linear_model
from pyresparser import ResumeParser
import random


# ================================================================
#                     MODEL TRAINING
# ================================================================
class TrainModel:
    def train(self):
        data = pd.read_csv('training_dataset.csv')
        array = data.values
        for i in range(len(array)):
            array[i][0] = 1 if array[i][0].lower() == "male" else 0
        df = pd.DataFrame(array)
        X = df[[0, 1, 2, 3, 4, 5, 6]].values
        y = df[7].values
        self.model = linear_model.LogisticRegression(
            multi_class='multinomial', solver='newton-cg', max_iter=1000)
        self.model.fit(X, y)

    def predict(self, features):
        try:
            features = [int(i) for i in features]
            y_pred = self.model.predict([features])[0]
            return y_pred
        except:
            messagebox.showerror("Error", "Please fill all required fields!")
            return None


# ================================================================
#                     TEXT ANALYSIS / SCORING
# ================================================================
def analyze_text_score(text, job_role):
    """Text mining-based scoring system"""
    keywords = {
        "software engineer": ["python", "java", "c++", "teamwork", "problem solving", "algorithms"],
        "data analyst": ["data", "excel", "statistics", "visualization", "python"],
        "ai engineer": ["machine learning", "deep learning", "neural networks", "ai", "python"]
    }
    soft_skills = ["communication", "leadership", "creativity", "adaptability", "time management"]
    certifications = ["certified", "certificate", "diploma", "training"]
    achievements = ["award", "achievement", "recognition", "project"]

    text = text.lower()
    skill_score = sum(3 for word in keywords.get(job_role, []) if word in text)
    soft_score = sum(2 for word in soft_skills if word in text)
    cert_score = sum(2 for word in certifications if word in text)
    achieve_score = sum(2 for word in achievements if word in text)

    total_score = min((skill_score * 2 + soft_score + cert_score + achieve_score) * 2, 100)
    return round(total_score, 2)


# ================================================================
#                     MAIN APPLICATION
# ================================================================
class PersonalityApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("AI CV Ranking & Personality Prediction System")
        self.geometry("1100x800")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        self.cv_folder = "cvs"
        os.makedirs(self.cv_folder, exist_ok=True)
        self.results_file = "results.csv"
        self.model = TrainModel()
        self.model.train()
        self.cv_path = ""
        self.create_ui()

    def create_ui(self):
        title = ctk.CTkLabel(self, text="AI CV Ranking & Personality Prediction System",
                             font=ctk.CTkFont(size=26, weight="bold"))
        title.pack(pady=15)

        frame = ctk.CTkScrollableFrame(self, width=900, height=680)
        frame.pack(pady=10)

        # -------- Candidate Info --------
        ctk.CTkLabel(frame, text="Candidate Information", font=ctk.CTkFont(size=18, weight="bold")).pack(anchor="w",
                                                                                                         pady=(10, 5))
        self.name_entry = self._make_entry(frame, "Full Name:")
        self.age_entry = self._make_entry(frame, "Age:")

        gender_frame = ctk.CTkFrame(frame)
        gender_frame.pack(fill="x", pady=5)
        ctk.CTkLabel(gender_frame, text="Gender:", width=150, anchor="w").pack(side="left")
        self.gender_var = ctk.StringVar(value="Male")
        ctk.CTkRadioButton(gender_frame, text="Male", variable=self.gender_var, value="Male").pack(side="left", padx=5)
        ctk.CTkRadioButton(gender_frame, text="Female", variable=self.gender_var, value="Female").pack(side="left",
                                                                                                       padx=5)

        # -------- Job Role --------
        job_frame = ctk.CTkFrame(frame)
        job_frame.pack(fill="x", pady=5)
        ctk.CTkLabel(job_frame, text="Job Profile:", width=150, anchor="w").pack(side="left")
        self.job_role = ctk.CTkOptionMenu(job_frame, values=["Software Engineer", "Data Analyst", "AI Engineer"])
        self.job_role.pack(side="left", padx=5)

        # -------- Personality Sliders --------
        ctk.CTkLabel(frame, text="Personality Traits (1–10)", font=ctk.CTkFont(size=18, weight="bold")).pack(anchor="w",
                                                                                                             pady=(20,
                                                                                                                   5))
        self.openness = self._make_slider(frame, "Openness")
        self.neuroticism = self._make_slider(frame, "Neuroticism")
        self.conscientiousness = self._make_slider(frame, "Conscientiousness")
        self.agreeableness = self._make_slider(frame, "Agreeableness")
        self.extraversion = self._make_slider(frame, "Extraversion")

        # -------- CV Info Fields --------
        ctk.CTkLabel(frame, text="CV Details", font=ctk.CTkFont(size=18, weight="bold")).pack(anchor="w", pady=(20, 5))
        self.objective = self._make_text(frame, "Career Objective:")
        self.projects = self._make_text(frame, "Projects:")
        self.skills = self._make_text(frame, "Technical Skills:")
        self.certificates = self._make_text(frame, "Certificates:")
        self.achievements = self._make_text(frame, "Achievements:")

        # -------- Upload CV --------
        upload_frame = ctk.CTkFrame(frame)
        upload_frame.pack(fill="x", pady=10)
        ctk.CTkLabel(upload_frame, text="Upload Text CV (optional):").pack(side="left", padx=5)
        ctk.CTkButton(upload_frame, text="Browse", command=self.open_file).pack(side="left", padx=5)
        self.file_label = ctk.CTkLabel(upload_frame, text="No file selected", text_color="gray")
        self.file_label.pack(side="left", padx=10)

        # -------- Buttons --------
        btn_frame = ctk.CTkFrame(frame)
        btn_frame.pack(pady=15)
        ctk.CTkButton(btn_frame, text="Predict Personality & Save CV", height=40, width=220,
                      command=self.predict_personality).pack(side="left", padx=10)
        ctk.CTkButton(btn_frame, text="View Candidate Rankings", height=40, width=220, command=self.view_rankings).pack(
            side="left", padx=10)

    def _make_entry(self, parent, label):
        frame = ctk.CTkFrame(parent)
        frame.pack(fill="x", pady=5)
        ctk.CTkLabel(frame, text=label, width=150, anchor="w").pack(side="left")
        entry = ctk.CTkEntry(frame, width=300)
        entry.pack(side="left", padx=5)
        return entry

    def _make_slider(self, parent, label):
        frame = ctk.CTkFrame(parent)
        frame.pack(fill="x", pady=5)
        ctk.CTkLabel(frame, text=label, width=250, anchor="w").pack(side="left")
        var = ctk.IntVar(value=random.randint(4, 7))
        ctk.CTkSlider(frame, from_=1, to=10, variable=var).pack(side="left", padx=10, fill="x", expand=True)
        return var

    def _make_text(self, parent, label):
        frame = ctk.CTkFrame(parent)
        frame.pack(fill="x", pady=5)
        ctk.CTkLabel(frame, text=label, width=200, anchor="w").pack(side="top", padx=5)
        text_box = ctk.CTkTextbox(frame, height=80)
        text_box.pack(fill="x", padx=10)
        return text_box

    def open_file(self):
        self.cv_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if self.cv_path:
            self.file_label.configure(text=os.path.basename(self.cv_path), text_color="#4CAF50")

    # ================================================================
    #                  PREDICTION + SAVING
    # ================================================================
    def predict_personality(self):
        name = self.name_entry.get().strip()
        age = self.age_entry.get().strip()
        gender = 1 if self.gender_var.get() == "Male" else 0
        job_role = self.job_role.get().lower()

        if not name or not age:
            messagebox.showerror("Error", "Please enter candidate name and age.")
            return

        traits = [gender, age, self.openness.get(), self.neuroticism.get(),
                  self.conscientiousness.get(), self.agreeableness.get(), self.extraversion.get()]

        # Combine CV info
        text_content = "\n".join([
            self.objective.get("1.0", "end-1c"),
            self.projects.get("1.0", "end-1c"),
            self.skills.get("1.0", "end-1c"),
            self.certificates.get("1.0", "end-1c"),
            self.achievements.get("1.0", "end-1c")
        ])

        # Append uploaded CV
        if self.cv_path:
            with open(self.cv_path, "r", encoding="utf-8") as f:
                text_content += "\n" + f.read()

        # Save CV to folder
        cv_file = os.path.join(self.cv_folder, f"{name}.txt")
        with open(cv_file, "w", encoding="utf-8") as f:
            f.write(text_content)

        # Predictions
        prediction = self.model.predict(traits)
        score = analyze_text_score(text_content, job_role)
        overall = round((score * 0.6) + (self.openness.get() + self.agreeableness.get()) * 4, 2)

        # Save result
        result_data = pd.DataFrame([[name, job_role, prediction, score, overall]],
                                   columns=["Name", "Job Role", "Personality", "CV Score", "Overall Score"])
        if os.path.exists(self.results_file):
            old = pd.read_csv(self.results_file)
            updated = pd.concat([old, result_data], ignore_index=True)
            updated.to_csv(self.results_file, index=False)
        else:
            result_data.to_csv(self.results_file, index=False)

        self.show_result(name, prediction, score, overall)

    def show_result(self, name, personality, score, overall):
        result = ctk.CTkToplevel(self)
        result.title("Prediction Result")
        result.geometry("700x400")
        ctk.CTkLabel(result, text="Candidate Report", font=ctk.CTkFont(size=24, weight="bold")).pack(pady=20)
        ctk.CTkLabel(result, text=f"Name: {name}", font=ctk.CTkFont(size=14)).pack(pady=5)
        ctk.CTkLabel(result, text=f"Predicted Personality: {personality}", text_color="#4CAF50",
                     font=ctk.CTkFont(size=16, weight="bold")).pack(pady=5)
        ctk.CTkLabel(result, text=f"CV Analysis Score: {score}%", text_color="#03A9F4",
                     font=ctk.CTkFont(size=14)).pack(pady=5)
        ctk.CTkLabel(result, text=f"Overall Candidate Score: {overall}%", text_color="#FFB300",
                     font=ctk.CTkFont(size=16, weight="bold")).pack(pady=15)
        ctk.CTkButton(result, text="Close", command=result.destroy).pack(pady=10)

    # ================================================================
    #                  VIEW RANKINGS WINDOW
    # ================================================================
    def view_rankings(self):
        if not os.path.exists(self.results_file):
            messagebox.showinfo("No Data", "No candidates have been analyzed yet.")
            return

        data = pd.read_csv(self.results_file)
        rank = ctk.CTkToplevel(self)
        rank.title("Candidate Rankings")
        rank.geometry("800x500")

        ctk.CTkLabel(rank, text="Candidate Rankings by Job Role", font=ctk.CTkFont(size=22, weight="bold")).pack(
            pady=15)

        tree = ctk.CTkTextbox(rank, width=700, height=400)
        text = ""
        for role in data["Job Role"].unique():
            subset = data[data["Job Role"] == role].sort_values(by="Overall Score", ascending=False)
            text += f"\n🏢 {role.title()}:\n"
            for i, row in subset.iterrows():
                text += f"  - {row['Name']} | Personality: {row['Personality']} | Score: {row['Overall Score']}%\n"
        tree.insert("1.0", text)
        tree.configure(state="disabled")
        tree.pack(pady=10)


# ================================================================
#                        RUN APP
# ================================================================
if __name__ == "__main__":
    app = PersonalityApp()
    app.mainloop()