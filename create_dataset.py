import pandas as pd
import random
import re
from datetime import datetime


def generate_phishing_emails(n=500):
    """Generate phishing email samples"""
    phishing_templates = [
        "URGENT: Your account has been compromised. Click here to verify: {url}",
        "Dear customer, we noticed unusual activity. Please update your info: {url}",
        "Congratulations! You won a prize. Claim now: {url}",
        "Security Alert: Your password needs reset. Visit: {url}",
        "Your payment failed. Please update payment method: {url}",
        "Account suspended. Reactivate now: {url}",
        "Exclusive offer! Limited time: {url}",
        "Your bank account requires verification: {url}",
        "IRS Notice: Tax refund pending. Click: {url}",
        "Your Netflix subscription expired. Renew: {url}",
        "PayPal: Your account limited. Resolve: {url}",
        "Amazon: Order confirmation needed. Verify: {url}",
        "Microsoft: Security update required. Download: {url}",
        "Your Apple ID has been locked. Unlock: {url}",
        "FedEx: Package delivery failed. Track: {url}"
    ]

    phishing_keywords = ["urgent", "verify", "click", "update", "security", "alert",
                         "suspended", "limited", "confirm", "account", "password",
                         "bank", "payment", "refund", "prize", "winner", "free",
                         "congratulations", "exclusive", "limited time"]

    emails = []

    for i in range(n):
        template = random.choice(phishing_templates)
        url = f"http://{random.choice(['secure', 'verify', 'update', 'account', 'bank'])}-{random.randint(1000, 9999)}.{random.choice(['xyz', 'top', 'tk', 'ml', 'ga'])}/login"

        # Add random variations
        subject = random.choice(["URGENT", "Security Alert", "Important", "Action Required", "Notice"])
        sender = random.choice(["security@bank.com", "support@paypal.com", "admin@amazon.com",
                                "service@apple.com", "help@microsoft.com", "noreply@irs.gov"])

        # Add obfuscation techniques
        if random.random() > 0.5:
            url = url.replace('http://', 'http://' + ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=3)) + '.')

        body = template.format(url=url)

        # Add random keywords
        num_keywords = random.randint(2, 6)
        selected_keywords = random.sample(phishing_keywords, num_keywords)
        for kw in selected_keywords:
            if random.random() > 0.5:
                body += f" {kw.upper()}!!!"
            else:
                body += f" {kw.capitalize()} "

        # Add sense of urgency
        if random.random() > 0.5:
            body += f" ACT NOW! {random.choice(['24 hours', '48 hours', 'immediately'])}"

        emails.append({
            'email_id': f'phish_{i + 1}',
            'subject': subject,
            'sender': sender,
            'body': body,
            'label': 'Phishing'
        })

    return emails


def generate_safe_emails(n=500):
    """Generate legitimate/safe email samples"""
    safe_templates = [
        "Hi, Here's the report you requested. Let me know if you need changes.",
        "Meeting scheduled for tomorrow at 3 PM. Please confirm your attendance.",
        "Your order #{order_id} has been shipped. Tracking number: {tracking}",
        "Monthly newsletter: Check out our latest updates and features.",
        "Your password was successfully changed. If this wasn't you, contact support.",
        "Payment receipt for your recent transaction of ${amount}.",
        "Welcome to our service! Here's how to get started.",
        "Your subscription has been renewed for another month.",
        "Thank you for your purchase! Your invoice is attached.",
        "Team meeting notes from today's discussion.",
        "Project update: We're ahead of schedule!",
        "Your account balance is ${balance}",
        "New comment on your document: {comment}",
        "Your profile has been updated successfully.",
        "Weekly status report is ready for review."
    ]

    safe_keywords = ["meeting", "report", "update", "newsletter", "receipt", "invoice",
                     "subscription", "purchase", "order", "tracking", "balance", "comment",
                     "review", "document", "profile", "status", "project", "team"]

    emails = []

    for i in range(n):
        template = random.choice(safe_templates)

        # Replace placeholders with realistic values
        template = template.replace('{order_id}', str(random.randint(10000, 99999)))
        template = template.replace('{tracking}', ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=10)))
        template = template.replace('{amount}', str(random.randint(10, 500)))
        template = template.replace('{balance}', str(random.randint(100, 10000)))
        template = template.replace('{comment}',
                                    random.choice(["Looks good!", "Please review", "Approved", "Needs revision"]))

        subject = random.choice(["Project Update", "Meeting Invitation", "Order Confirmation",
                                 "Monthly Report", "Welcome", "Invoice", "Newsletter", "Team Update"])
        sender = random.choice(["john@company.com", "team@work.com", "noreply@service.com",
                                "support@legit.com", "info@business.com", "manager@office.com"])

        # Add professional signature
        body = template
        if random.random() > 0.5:
            body += f"\n\nBest regards,\n{random.choice(['John Doe', 'Sarah Smith', 'Mike Johnson', 'Emily Davis'])}"
            body += f"\n{random.choice(['Manager', 'Team Lead', 'Director', 'Coordinator'])}"

        # Add some safe keywords naturally
        if random.random() > 0.5:
            body += f"\n\nReference: {random.choice(safe_keywords)}-{random.randint(100, 999)}"

        emails.append({
            'email_id': f'safe_{i + 1}',
            'subject': subject,
            'sender': sender,
            'body': body,
            'label': 'Safe'
        })

    return emails


def create_dataset():
    """Create and save the dataset"""
    print("Generating phishing emails...")
    phishing_emails = generate_phishing_emails(500)

    print("Generating safe emails...")
    safe_emails = generate_safe_emails(500)

    # Combine and shuffle
    all_emails = phishing_emails + safe_emails
    random.shuffle(all_emails)

    # Create DataFrame
    df = pd.DataFrame(all_emails)

    # Add some additional features
    df['word_count'] = df['body'].apply(lambda x: len(x.split()))
    df['char_count'] = df['body'].apply(lambda x: len(x))
    df['url_count'] = df['body'].apply(lambda x: len(re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+])+', x)))
    df['has_suspicious_words'] = df['body'].apply(
        lambda x: any(
            word in x.lower() for word in ['urgent', 'verify', 'click', 'update', 'security', 'alert', 'suspended'])
    )

    # Save dataset
    df.to_csv('phishing_emails_dataset.csv', index=False)
    print(f"\nDataset created successfully!")
    print(f"Total emails: {len(df)}")
    print(f"Phishing: {len(df[df['label'] == 'Phishing'])}")
    print(f"Safe: {len(df[df['label'] == 'Safe'])}")
    print("\nDataset saved as 'phishing_emails_dataset.csv'")

    return df


if __name__ == "__main__":
    create_dataset()