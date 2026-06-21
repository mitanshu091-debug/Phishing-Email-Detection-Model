import pandas as pd
import numpy as np
import re
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
import joblib
import warnings

warnings.filterwarnings('ignore')


class PhishingDetector:
    def __init__(self):
        self.model = None
        self.vectorizer = None
        self.pipeline = None

    def extract_features(self, df):
        """Extract additional features from email content"""
        # Count URLs
        df['url_count'] = df['body'].apply(
            lambda x: len(re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+])+', x))
        )

        # Count suspicious keywords
        suspicious_keywords = ['urgent', 'verify', 'click', 'update', 'security', 'alert',
                               'suspended', 'limited', 'confirm', 'account', 'password',
                               'bank', 'payment', 'refund', 'prize', 'winner', 'free']

        df['suspicious_count'] = df['body'].apply(
            lambda x: sum(1 for word in suspicious_keywords if word in x.lower())
        )

        # Check for all caps words
        df['caps_count'] = df['body'].apply(
            lambda x: sum(1 for word in x.split() if word.isupper() and len(word) > 2)
        )

        # Count exclamation marks
        df['exclamation_count'] = df['body'].apply(lambda x: x.count('!'))

        # Check for sensitive info (numbers that look like credit card/phone)
        df['sensitive_info'] = df['body'].apply(
            lambda x: 1 if re.search(r'\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}', x) else 0
        )

        # Email length
        df['length'] = df['body'].apply(lambda x: len(x))

        return df

    def create_combined_features(self, df):
        """Combine text and numeric features"""
        # Extract text features using TF-IDF
        text_features = df['subject'] + ' ' + df['sender'] + ' ' + df['body']

        # Extract numeric features
        numeric_features = df[['url_count', 'suspicious_count', 'caps_count',
                               'exclamation_count', 'sensitive_info', 'length']]

        return text_features, numeric_features

    def train(self, df):
        """Train the phishing detection model"""
        print("Extracting features...")
        df = self.extract_features(df)

        # Prepare features
        X_text, X_numeric = self.create_combined_features(df)
        y = df['label']

        # Split data
        X_text_train, X_text_test, X_numeric_train, X_numeric_test, y_train, y_test = train_test_split(
            X_text, X_numeric, y, test_size=0.2, random_state=42, stratify=y
        )

        # Create TF-IDF vectorizer
        self.vectorizer = TfidfVectorizer(
            max_features=1000,
            stop_words='english',
            ngram_range=(1, 2),
            min_df=2
        )

        # Transform text data
        X_text_train_tfidf = self.vectorizer.fit_transform(X_text_train)
        X_text_test_tfidf = self.vectorizer.transform(X_text_test)

        # Convert numeric features to dense arrays
        X_numeric_train = np.array(X_numeric_train)
        X_numeric_test = np.array(X_numeric_test)

        # Combine features
        X_train = np.hstack([X_text_train_tfidf.toarray(), X_numeric_train])
        X_test = np.hstack([X_text_test_tfidf.toarray(), X_numeric_test])

        # Train model
        print("Training Random Forest model...")
        self.model = RandomForestClassifier(
            n_estimators=100,
            max_depth=15,
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=42,
            class_weight='balanced'
        )

        self.model.fit(X_train, y_train)

        # Make predictions
        y_pred = self.model.predict(X_test)

        # Evaluate
        print("\n" + "=" * 50)
        print("MODEL EVALUATION")
        print("=" * 50)
        print(f"\nAccuracy: {accuracy_score(y_test, y_pred):.4f}")
        print(f"\nClassification Report:")
        print(classification_report(y_test, y_pred))

        # Confusion Matrix
        cm = confusion_matrix(y_test, y_pred)
        self.plot_confusion_matrix(cm)

        # Feature importance
        self.plot_feature_importance(X_text_train_tfidf, X_numeric_train)

        return y_test, y_pred

    def plot_confusion_matrix(self, cm):
        """Plot confusion matrix"""
        plt.figure(figsize=(8, 6))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                    xticklabels=['Safe', 'Phishing'],
                    yticklabels=['Safe', 'Phishing'])
        plt.title('Confusion Matrix')
        plt.ylabel('Actual')
        plt.xlabel('Predicted')
        plt.show()

        # Print detailed confusion matrix info
        tn, fp, fn, tp = cm.ravel()
        print(f"\nConfusion Matrix Details:")
        print(f"True Negatives: {tn} (Correctly identified as Safe)")
        print(f"False Positives: {fp} (Misclassified as Phishing)")
        print(f"False Negatives: {fn} (Misclassified as Safe)")
        print(f"True Positives: {tp} (Correctly identified as Phishing)")

    def plot_feature_importance(self, text_features, numeric_features):
        """Plot feature importance"""
        if hasattr(self.model, 'feature_importances_'):
            # Get feature importances
            importances = self.model.feature_importances_

            # Separate text and numeric importances
            text_importance = importances[:text_features.shape[1]]
            numeric_importance = importances[text_features.shape[1]:]

            # Create summary
            plt.figure(figsize=(10, 6))

            # Get top text features
            feature_names = self.vectorizer.get_feature_names_out()
            top_text_indices = np.argsort(text_importance)[-10:]
            top_text_features = [feature_names[i] for i in top_text_indices]
            top_text_importance = [text_importance[i] for i in top_text_indices]

            # Get numeric features
            numeric_names = ['url_count', 'suspicious_count', 'caps_count',
                             'exclamation_count', 'sensitive_info', 'length']

            # Combine top features
            all_features = list(top_text_features) + numeric_names
            all_importance = list(top_text_importance) + list(numeric_importance)

            # Sort by importance
            sorted_indices = np.argsort(all_importance)[::-1]
            sorted_features = [all_features[i] for i in sorted_indices]
            sorted_importance = [all_importance[i] for i in sorted_indices]

            plt.barh(sorted_features, sorted_importance)
            plt.xlabel('Feature Importance')
            plt.title('Top 15 Most Important Features')
            plt.tight_layout()
            plt.show()

    def predict_email(self, email_data):
        """Predict if a single email is phishing or safe"""
        # Create dataframe for single email
        df = pd.DataFrame([email_data])

        # Extract features
        df = self.extract_features(df)

        # Prepare features
        X_text = df['subject'] + ' ' + df['sender'] + ' ' + df['body']
        X_numeric = df[['url_count', 'suspicious_count', 'caps_count',
                        'exclamation_count', 'sensitive_info', 'length']]

        # Transform text
        X_text_tfidf = self.vectorizer.transform(X_text)
        X_numeric = np.array(X_numeric)

        # Combine features
        X = np.hstack([X_text_tfidf.toarray(), X_numeric])

        # Predict
        prediction = self.model.predict(X)[0]
        probability = self.model.predict_proba(X)[0]

        return prediction, probability

    def save_model(self, filename='phishing_model.pkl'):
        """Save the trained model and vectorizer"""
        model_data = {
            'model': self.model,
            'vectorizer': self.vectorizer
        }
        joblib.dump(model_data, filename)
        print(f"\nModel saved as '{filename}'")

    def load_model(self, filename='phishing_model.pkl'):
        """Load a trained model"""
        model_data = joblib.load(filename)
        self.model = model_data['model']
        self.vectorizer = model_data['vectorizer']
        print(f"Model loaded from '{filename}'")


def main():
    # Load dataset
    print("Loading dataset...")
    try:
        df = pd.read_csv('phishing_emails_dataset.csv')
        print(f"Dataset loaded: {len(df)} emails")
        print(f"Phishing: {len(df[df['label'] == 'Phishing'])}")
        print(f"Safe: {len(df[df['label'] == 'Safe'])}")
    except FileNotFoundError:
        print("Dataset not found. Please run create_dataset.py first.")
        return

    # Create and train model
    detector = PhishingDetector()
    y_test, y_pred = detector.train(df)

    # Save model
    detector.save_model()

    # Test with example emails
    print("\n" + "=" * 50)
    print("TESTING WITH EXAMPLE EMAILS")
    print("=" * 50)

    # Example phishing email
    phishing_email = {
        'subject': 'URGENT: Your Account Will Be Suspended!',
        'sender': 'security@bank-secure.com',
        'body': 'Dear Customer, Your account has been compromised. Please verify your information immediately at http://secure-bank-verify.xyz/login to prevent suspension. ACT NOW!'
    }

    # Example safe email
    safe_email = {
        'subject': 'Weekly Team Meeting',
        'sender': 'manager@company.com',
        'body': 'Hi team, Please join our weekly meeting tomorrow at 3 PM. We\'ll discuss project updates and next steps. Let me know if you have any questions. Best, John'
    }

    print("\nTesting Phishing Email:")
    prediction, prob = detector.predict_email(phishing_email)
    print(f"Classification: {prediction}")
    print(f"Confidence: {prob[1] if prediction == 'Phishing' else prob[0]:.4f}")

    print("\nTesting Safe Email:")
    prediction, prob = detector.predict_email(safe_email)
    print(f"Classification: {prediction}")
    print(f"Confidence: {prob[1] if prediction == 'Phishing' else prob[0]:.4f}")

    # Interactive testing
    print("\n" + "=" * 50)
    print("INTERACTIVE EMAIL TESTING")
    print("=" * 50)
    print("Enter email details to classify (or type 'quit' to exit)")

    while True:
        print("\n" + "-" * 30)
        subject = input("Subject: ")
        if subject.lower() == 'quit':
            break
        sender = input("Sender: ")
        body = input("Body: ")

        test_email = {
            'subject': subject,
            'sender': sender,
            'body': body
        }

        prediction, prob = detector.predict_email(test_email)
        confidence = prob[1] if prediction == 'Phishing' else prob[0]

        print(f"\nClassification: {prediction}")
        print(f"Confidence: {confidence:.4f} ({confidence * 100:.1f}%)")
        print("Risk Level: " + ("HIGH" if prediction == 'Phishing' else "LOW"))


if __name__ == "__main__":
    main()