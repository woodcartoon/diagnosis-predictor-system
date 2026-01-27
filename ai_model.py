# Import necessary libraries
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

# Load CSV data
def load_data(csv_file):
    try:
        data = pd.read_csv(csv_file)
        return data
    except Exception as e:
        print(f"Error loading data: {e}")

# Preprocess data
def preprocess_data(data):
    # Assuming 'diagnosis' is the target column
    X = data.drop('diagnosis', axis=1)
    y = data['diagnosis']
    
    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Scale data
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)
    
    return X_train, X_test, y_train, y_test

# Train model
def train_model(X_train, y_train):
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    return model

# Evaluate model
def evaluate_model(model, X_test, y_test):
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred)
    return accuracy, report

# Main function
def main():
    csv_file = 'your_data.csv'  # Replace with your CSV file
    data = load_data(csv_file)
    X_train, X_test, y_train, y_test = preprocess_data(data)
    model = train_model(X_train, y_train)
    accuracy, report = evaluate_model(model, X_test, y_test)
    print(f"Model Accuracy: {accuracy:.3f}")
    print("Classification Report:\n", report)

if __name__ == "__main__":
    main()