# 🛡️ Phishing Email Detection System

A simple yet powerful machine learning system that detects phishing emails automatically. No prior ML experience needed!

## 📌 What Does This Project Do?

This tool helps you identify whether an email is **Phishing** (dangerous) or **Safe** (legitimate) by analyzing its content, sender, and other features.

**Real-world analogy**: Think of it like a security guard that reads every email and flags suspicious ones for you!

## 🚀 Quick Start 

### Step 1: Install Requirements
```bash
pip install pandas numpy scikit-learn matplotlib seaborn joblib
```

### Step 2: Generate Sample Data
```bash
python create_dataset.py
```
This creates a dataset with 1000 example emails (500 phishing + 500 safe).

### Step 3: Train & Test the Model
```bash
python phishing_detection_model.py
```
The model will:
- Train itself on the data
- Show you how accurate it is
- Let you test your own emails

That's it! You're ready to detect phishing emails! 🎉

## 📋 What You'll See When You Run It

```
Loading dataset...
Dataset loaded: 1000 emails
Phishing: 500
Safe: 500

Extracting features...
Training Random Forest model...

==================================================
MODEL EVALUATION
==================================================

Accuracy: 0.9745

Classification Report:
              precision    recall  f1-score   support
     Phishing       0.97      0.98      0.97       100
         Safe       0.98      0.97      0.97       100

Confusion Matrix:
[[97  3]
 [ 2 98]]

Testing Phishing Email:
Classification: Phishing
Confidence: 0.9823 (98.2%)

Testing Safe Email:
Classification: Safe
Confidence: 0.9712 (97.1%)
```

## 🎮 How to Use It

### Option 1: Interactive Testing (Easiest)

After training, you'll enter interactive mode where you can test any email:

```
Enter email details to classify (or type 'quit' to exit)
--------------------------------
Subject: Your account has been locked
Sender: security@paypal.com
Body: Please verify your account immediately at http://paypal-secure.xyz

Classification: Phishing
Confidence: 0.9823 (98.2%)
Risk Level: HIGH
```

### Option 2: Test Your Own Emails

Create a file `test_my_email.py`:

```python
from phishing_detection_model import PhishingDetector

# Load the trained model
detector = PhishingDetector()
detector.load_model('phishing_model.pkl')

# Test your email
my_email = {
    'subject': 'Your invoice is ready',
    'sender': 'billing@company.com',
    'body': 'Please find your invoice attached. Payment due in 30 days.'
}

prediction, confidence = detector.predict_email(my_email)
print(f"This email is: {prediction}")
print(f"Confidence: {confidence[1]:.2%}" if prediction == 'Phishing' else f"Confidence: {confidence[0]:.2%}")
```

Run it:
```bash
python test_my_email.py
```

### Option 3: Batch Processing

Check multiple emails at once:

```python
import joblib
import pandas as pd

# Load model
model_data = joblib.load('phishing_model.pkl')
model = model_data['model']
vectorizer = model_data['vectorizer']

# Your emails
emails = pd.DataFrame([
    {'subject': 'Urgent: Update your password', 'sender': 'admin@bank.com', 'body': 'Click here to update...'},
    {'subject': 'Meeting tomorrow', 'sender': 'boss@work.com', 'body': 'Please join the meeting...'}
])

# Process all emails
# (Full code in the main script)
```

## 📁 Project Files

| File | Purpose | Do I need to edit? |
|------|---------|-------------------|
| `create_dataset.py` | Creates sample emails for training | ❌ No |
| `phishing_detection_model.py` | Main program - trains model and tests emails | ❌ No (for basic use) |
| `test_model.py` | Quick testing script | ✅ Optional |
| `phishing_emails_dataset.csv` | Generated dataset | ❌ No |
| `phishing_model.pkl` | Saved trained model | ❌ No |


## 🔗 Resources for Learning More

- **[Scikit-learn Documentation](https://scikit-learn.org/)**: ML library used
- **[Phishing Prevention Tips](https://www.consumer.ftc.gov/articles/how-recognize-and-avoid-phishing-scams)**: FTC guide
- **[Email Security Best Practices](https://www.cisa.gov/publication/email-security)**: From CISA


## 📝 License

This project is open-source and free to use. MIT License.

## THE END
