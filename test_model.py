import joblib
import pandas as pd
import numpy as np
import re

# Load the saved model
model_data = joblib.load('phishing_model.pkl')
model = model_data['model']
vectorizer = model_data['vectorizer']


def extract_features(text):
    """Extract features from email text"""
    url_count = len(re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+])+', text))
    suspicious_keywords = ['urgent', 'verify', 'click', 'update', 'security', 'alert',
                           'suspended', 'limited', 'confirm', 'account', 'password']
    suspicious_count = sum(1 for word in suspicious_keywords if word in text.lower())
    caps_count = sum(1 for word in text.split() if word.isupper() and len(word) > 2)
    exclamation_count = text.count('!')
    has_sensitive = 1 if re.search(r'\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}', text) else 0
    length = len(text)

    return [url_count, suspicious_count, caps_count, exclamation_count, has_sensitive, length]


def predict_email(subject, sender, body):
    """Predict if email is phishing"""
    full_text = subject + ' ' + sender + ' ' + body

    # Get text features
    text_features = vectorizer.transform([full_text])

    # Get numeric features
    numeric_features = np.array([extract_features(full_text)])

    # Combine features
    combined_features = np.hstack([text_features.toarray(), numeric_features])

    # Predict
    prediction = model.predict(combined_features)[0]
    probability = model.predict_proba(combined_features)[0]

    return prediction, probability


# Test your own emails
test_cases = [
    {
        'subject': 'Your account is compromised',
        'sender': 'security@bank-verify.com',
        'body': 'URGENT: Click here to verify your account http://secure-bank.xyz/login or your account will be suspended!'
    },
    {
        'subject': 'Project Meeting',
        'sender': 'john@company.com',
        'body': 'Hi, Please find attached the project report. Let me know if you have any questions.'
    }
]

for i, email in enumerate(test_cases, 1):
    print(f"\nTest Case {i}:")
    print(f"Subject: {email['subject']}")
    pred, prob = predict_email(email['subject'], email['sender'], email['body'])
    print(f"Prediction: {pred}")
    confidence = prob[1] if pred == 'Phishing' else prob[0]
    print(f"Confidence: {confidence:.4f}")