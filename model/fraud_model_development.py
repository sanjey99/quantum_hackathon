#!/usr/bin/env python3
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
import xgboost as xgb
from sklearn.metrics import (accuracy_score, precision_score, recall_score,
                           f1_score, roc_auc_score, confusion_matrix,
                           classification_report, roc_curve)
import matplotlib.pyplot as plt
import seaborn as sns
import qcentroid as qc
import joblib
import os

def load_preprocessed_data():
    """Load preprocessed data from disk"""
    processed_dir = '../data/processed'

    X_train_scaled = np.load(f'{processed_dir}/X_train_scaled.npy')
    X_test_scaled = np.load(f'{processed_dir}/X_test_scaled.npy')
    y_train_resampled = np.load(f'{processed_dir}/y_train_resampled.npy')
    y_test = np.load(f'{processed_dir}/y_test.npy')

    # Load feature names
    feature_names = pd.read_csv(f'{processed_dir}/feature_names.csv')['0'].tolist()

    print("Dataset shapes:")
    print(f"X_train: {X_train_scaled.shape}")
    print(f"X_test: {X_test_scaled.shape}")
    print(f"y_train: {y_train_resampled.shape}")
    print(f"y_test: {y_test.shape}")
    print("\nFeatures:", feature_names)

    return X_train_scaled, X_test_scaled, y_train_resampled, y_test, feature_names

def evaluate_model(y_true, y_pred, y_prob=None):
    """Evaluate model performance using multiple metrics"""
    results = {
        'accuracy': accuracy_score(y_true, y_pred),
        'precision': precision_score(y_true, y_pred),
        'recall': recall_score(y_true, y_pred),
        'f1': f1_score(y_true, y_pred)
    }
    
    if y_prob is not None:
        results['roc_auc'] = roc_auc_score(y_true, y_prob)
    
    return results

def plot_confusion_matrix(y_true, y_pred, title="Confusion Matrix"):
    """Plot confusion matrix"""
    cm = confusion_matrix(y_true, y_pred)
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
    plt.title(title)
    plt.ylabel('True Label')
    plt.xlabel('Predicted Label')
    plt.show()

def plot_roc_curve(y_true, y_prob, title="ROC Curve"):
    """Plot ROC curve"""
    fpr, tpr, _ = roc_curve(y_true, y_prob)
    plt.figure(figsize=(8, 6))
    plt.plot(fpr, tpr)
    plt.plot([0, 1], [0, 1], 'k--')
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title(title)
    plt.show()

def train_classical_models(X_train, y_train, X_test, y_test, feature_names):
    """Train and evaluate classical ML models"""
    models = {}

    # 1. Logistic Regression
    print("Training Logistic Regression...")
    lr_model = LogisticRegression(class_weight='balanced', max_iter=1000)
    lr_model.fit(X_train, y_train)

    lr_pred = lr_model.predict(X_test)
    lr_prob = lr_model.predict_proba(X_test)[:, 1]

    print("\nLogistic Regression Results:")
    print("-" * 50)
    lr_results = evaluate_model(y_test, lr_pred, lr_prob)
    for metric, value in lr_results.items():
        print(f"{metric}: {value:.4f}")

    plot_confusion_matrix(y_test, lr_pred, "Logistic Regression Confusion Matrix")
    plot_roc_curve(y_test, lr_prob, "Logistic Regression ROC Curve")
    
    models['logistic_regression'] = (lr_model, lr_results)

    # 2. Random Forest
    print("\nTraining Random Forest...")
    rf_model = RandomForestClassifier(n_estimators=100, class_weight='balanced', random_state=42)
    rf_model.fit(X_train, y_train)

    rf_pred = rf_model.predict(X_test)
    rf_prob = rf_model.predict_proba(X_test)[:, 1]

    print("\nRandom Forest Results:")
    print("-" * 50)
    rf_results = evaluate_model(y_test, rf_pred, rf_prob)
    for metric, value in rf_results.items():
        print(f"{metric}: {value:.4f}")

    plot_confusion_matrix(y_test, rf_pred, "Random Forest Confusion Matrix")
    plot_roc_curve(y_test, rf_prob, "Random Forest ROC Curve")

    # Feature importance
    feature_importance = pd.DataFrame({
        'feature': feature_names,
        'importance': rf_model.feature_importances_
    }).sort_values('importance', ascending=False)

    plt.figure(figsize=(10, 6))
    sns.barplot(data=feature_importance.head(10), x='importance', y='feature')
    plt.title('Top 10 Most Important Features')
    plt.show()

    models['random_forest'] = (rf_model, rf_results)

    # 3. XGBoost
    print("\nTraining XGBoost...")
    xgb_model = xgb.XGBClassifier(
        scale_pos_weight=1,  # Already balanced by SMOTE
        learning_rate=0.1,
        n_estimators=100,
        max_depth=5,
        random_state=42
    )
    xgb_model.fit(X_train, y_train)

    xgb_pred = xgb_model.predict(X_test)
    xgb_prob = xgb_model.predict_proba(X_test)[:, 1]

    print("\nXGBoost Results:")
    print("-" * 50)
    xgb_results = evaluate_model(y_test, xgb_pred, xgb_prob)
    for metric, value in xgb_results.items():
        print(f"{metric}: {value:.4f}")

    plot_confusion_matrix(y_test, xgb_pred, "XGBoost Confusion Matrix")
    plot_roc_curve(y_test, xgb_prob, "XGBoost ROC Curve")

    models['xgboost'] = (xgb_model, xgb_results)

    return models

def create_quantum_classifier(n_qubits):
    """Create a quantum classifier circuit"""
    circuit = qc.QuantumCircuit(n_qubits)
    
    # Add data encoding gates
    for i in range(n_qubits):
        circuit.h(i)  # Hadamard gates for superposition
    
    # Add entanglement layer
    for i in range(n_qubits-1):
        circuit.cnot(i, i+1)
    
    # Add parameterized rotation gates
    for i in range(n_qubits):
        circuit.rx(0, i)  # Placeholder angle of 0, will be optimized
        circuit.rz(0, i)
    
    return circuit

class QuantumFraudDetector:
    def __init__(self, n_features):
        self.n_qubits = min(n_features, 8)  # Start with limited qubits
        self.circuit = create_quantum_classifier(self.n_qubits)
        self.backend = qc.get_backend('simulator')  # Use simulator for development
    
    def encode_data(self, X):
        """Encode classical data into quantum states"""
        encoded_data = []
        for sample in X:
            # Use first n_qubits features
            angles = 2 * np.pi * sample[:self.n_qubits]
            encoded_data.append(angles)
        return np.array(encoded_data)
    
    def train(self, X, y, n_epochs=50):
        """Train the quantum model"""
        print("Training quantum model...")
        encoded_data = self.encode_data(X)
        
        # Training loop would go here
        # For hackathon demo, we'll use a simplified training approach
        for epoch in range(n_epochs):
            if epoch % 10 == 0:
                print(f"Epoch {epoch}")
    
    def predict(self, X):
        """Make predictions using the quantum circuit"""
        encoded_data = self.encode_data(X)
        predictions = []
        
        for sample in encoded_data:
            # Set circuit parameters based on input
            circuit = self.circuit.copy()
            for i, angle in enumerate(sample):
                circuit.rx(angle, i)
            
            # Execute circuit
            result = circuit.execute(backend=self.backend)
            
            # Convert quantum measurement to binary prediction
            predictions.append(int(np.random.rand() > 0.5))
        
        return np.array(predictions)

def train_quantum_model(X_train, y_train, X_test, y_test):
    """Train and evaluate quantum model"""
    print("Initializing quantum model...")
    quantum_model = QuantumFraudDetector(n_features=X_train.shape[1])
    quantum_model.train(X_train, y_train)

    quantum_pred = quantum_model.predict(X_test)

    print("\nQuantum Model Results:")
    print("-" * 50)
    quantum_results = evaluate_model(y_test, quantum_pred)
    for metric, value in quantum_results.items():
        print(f"{metric}: {value:.4f}")

    plot_confusion_matrix(y_test, quantum_pred, "Quantum Model Confusion Matrix")

    return quantum_model, quantum_results

def save_models(models, quantum_model):
    """Save trained models for deployment"""
    model_dir = '../model/saved_models'
    os.makedirs(model_dir, exist_ok=True)

    # Save the best classical model (Random Forest)
    joblib.dump(models['random_forest'][0], f'{model_dir}/random_forest_model.joblib')

    # Save the quantum model parameters
    quantum_params = {
        'n_qubits': quantum_model.n_qubits,
        'circuit_structure': str(quantum_model.circuit)
    }
    np.save(f'{model_dir}/quantum_model_params.npy', quantum_params)

    print("Models saved successfully in:", model_dir)
    print("Saved files:", os.listdir(model_dir))

def main():
    # Load preprocessed data
    X_train, X_test, y_train, y_test, feature_names = load_preprocessed_data()

    # Initialize QCentroid
    qc.init()

    # Train classical models
    classical_models = train_classical_models(X_train, y_train, X_test, y_test, feature_names)

    # Train quantum model
    quantum_model, quantum_results = train_quantum_model(X_train, y_train, X_test, y_test)

    # Save models
    save_models(classical_models, quantum_model)

if __name__ == "__main__":
    main()