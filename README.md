# 💊 Dawai Samjho — Medicine Label Reader

> **Our app helps Pakistani patients understand their prescribed medicines in simple Urdu and English using Gemma AI.**

Built for **Hacktoberfest Hack Day Faisalabad** · Powered by **Gemma 4** via Google Gemini API

---

## 🔥 What It Does

Most Pakistani patients receive medicines from doctors without understanding:
- What the medicine actually does
- When and how to take it
- What side effects to watch for
- What foods or drinks to avoid

**Dawai Samjho** solves this by letting users:
1. 📸 **Upload a photo** of their medicine box or prescription
2. ✍️ **OR type** the medicine name

Gemma 4 AI reads it and instantly explains everything in simple **Roman Urdu + English**.

---

## 🚀 How to Run

### 1. Clone the repo
```bash
git clone https://github.com/YOUR_USERNAME/dawai-samjho.git
cd dawai-samjho
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Add your API key
```bash
# Copy the example file
copy .env.example .env

# Open .env and replace with your real key
GEMINI_API_KEY=your_actual_key_here
```
Get a free API key at [Google AI Studio](https://aistudio.google.com/)

### 4. Run the app
```bash
streamlit run app.py
```

Open your browser at `http://localhost:8501`

---

## 🤖 How Gemma 4 Is Used

This app uses **`gemma-4-26b-a4b-it`** through the **Google Gemini API**.

Gemma 4 is a **multimodal model** — it can both read text AND understand images. When a user uploads a medicine photo, Gemma reads the label directly from the image and generates a structured explanation.

The model is prompted to act as a friendly medical assistant and respond in a consistent format covering:
- What the medicine is
- Dosage instructions
- Side effects
- Foods to avoid
- When to see a doctor

**Model License:** [Apache 2.0](https://ai.google.dev/gemma/terms)

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| Python | Core language |
| Streamlit | Web UI |
| google-genai | Gemini API client |
| Gemma 4 (gemma-4-26b-a4b-it) | AI model for text + image understanding |
| python-dotenv | Secure API key loading |

---

## 📁 Project Structure

```
dawai-samjho/
├── app.py              # Main Streamlit app
├── requirements.txt    # Python dependencies
├── .env.example        # API key template
├── .gitignore          # Keeps .env safe (never pushed)
└── README.md           # This file
```

---

## ⚠️ Disclaimer

This app is for **general information purposes only**. Always consult your doctor or pharmacist before making any medical decisions. Do not stop or start medicines based solely on this app.

---

## 📜 License

MIT License — see [LICENSE](LICENSE) file.

Gemma 4 model is used under [Apache 2.0](https://ai.google.dev/gemma/terms).
