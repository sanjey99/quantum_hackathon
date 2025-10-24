#!/usr/bin/env python
import sys
import json
import numpy as np
import joblib
from sklearn.preprocessing import StandardScaler

def load_models():
    """
    Load the trained model and scaler
    """
    model_path = 'model/saved_models/random_forest_model.joblib'
    scaler_path = 'data/processed/scaler.joblib'
    
    try:
        model = joblib.load(model_path)
        scaler = joblib.load(scaler_path)
        return model, scaler
    except Exception as e:
        print(f"Error loading models: {str(e)}", file=sys.stderr)
        sys.exit(1)

def preprocess_transaction(transaction, scaler):
    """
    Preprocess a single transaction
    """
    # Extract features in the correct order
    features = [
        float(transaction['amount']),
        int(transaction['hour']),
        int(transaction['day_of_week']),
        int(transaction['is_weekend']),
        float(transaction['amount_log']),
        int(transaction['customer_tx_count']),
        int(transaction['merchant_tx_count']),
        int(transaction['merchant_category_encoded'])
    ]
    
    # Scale features
    features_scaled = scaler.transform(np.array(features).reshape(1, -1))
    return features_scaled

def predict_fraud(transaction_data):
    """
    Predict fraud probability for transactions
    """
    # Load models
    model, scaler = load_models()
    
    # Process single transaction or batch
    if isinstance(transaction_data, dict):
        transaction_data = [transaction_data]
    
    results = []
    for transaction in transaction_data:
        # Preprocess
        features = preprocess_transaction(transaction, scaler)
        
        # Predict
        prob = model.predict_proba(features)[0][1]
        is_fraud = prob > 0.5
        
        # Format result
        result = {
            'transaction_id': transaction.get('transaction_id', 'unknown'),
            'is_fraud': bool(is_fraud),
            'fraud_probability': float(prob)
        }
        results.append(result)
    
    return results

if __name__ == '__main__':
    try:
        # Read input from stdin
        input_data = json.load(sys.stdin)
        
        # Make prediction
        results = predict_fraud(input_data)
        
        # Output results as JSON
        print(json.dumps(results))
        
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)