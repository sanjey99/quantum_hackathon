#!/usr/bin/env python3
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from imblearn.over_sampling import SMOTE
import os
import joblib

# Set style for visualizations
plt.style.use('seaborn')
sns.set_palette("husl")

# Display settings for pandas
pd.set_option('display.max_columns', None)
pd.set_option('display.float_format', lambda x: '%.3f' % x)

def load_fraud_dataset(filepath='../data/transactions.csv'):
    try:
        df = pd.read_csv(filepath)
        print(f"Dataset loaded successfully with shape: {df.shape}")
        return df
    except FileNotFoundError:
        print("Dataset not found. Using synthetic data for demonstration.")
        # Create synthetic data
        n_samples = 10000
        np.random.seed(42)
        
        # Generate synthetic transaction data
        data = {
            'transaction_id': range(n_samples),
            'timestamp': pd.date_range(start='2025-01-01', periods=n_samples, freq='H'),
            'amount': np.random.exponential(100, n_samples),
            'merchant_id': np.random.randint(1, 1000, n_samples),
            'customer_id': np.random.randint(1, 5000, n_samples),
            'merchant_category': np.random.choice(['retail', 'online', 'travel', 'entertainment'], n_samples),
            'fraud': np.random.choice([0, 1], n_samples, p=[0.99, 0.01])  # 1% fraud rate
        }
        
        df = pd.DataFrame(data)
        print(f"Synthetic dataset created with shape: {df.shape}")
        return df

def analyze_dataset(df):
    """Perform basic analysis of the dataset"""
    print("Dataset Info:")
    print("-" * 50)
    print(df.info())

    print("\nMissing Values:")
    print("-" * 50)
    print(df.isnull().sum())

    print("\nBasic Statistics:")
    print("-" * 50)
    print(df.describe())

    # Class distribution
    print("\nFraud Distribution:")
    print("-" * 50)
    fraud_dist = df['fraud'].value_counts(normalize=True)
    print(fraud_dist)

    # Calculate imbalance ratio
    imbalance_ratio = fraud_dist[0] / fraud_dist[1]
    print(f"\nImbalance ratio (non-fraud:fraud): {imbalance_ratio:.2f}:1")

def visualize_patterns(df):
    """Create visualizations of key patterns in the data"""
    # Set up the plotting area
    plt.figure(figsize=(15, 10))

    # 1. Amount Distribution by Fraud Status
    plt.subplot(2, 2, 1)
    sns.boxplot(x='fraud', y='amount', data=df)
    plt.title('Transaction Amount Distribution by Fraud Status')
    plt.xlabel('Fraud (0=No, 1=Yes)')
    plt.ylabel('Amount')

    # 2. Fraud Rate by Merchant Category
    plt.subplot(2, 2, 2)
    fraud_by_category = df.groupby('merchant_category')['fraud'].mean()
    fraud_by_category.plot(kind='bar')
    plt.title('Fraud Rate by Merchant Category')
    plt.xlabel('Merchant Category')
    plt.ylabel('Fraud Rate')

    # 3. Transaction Volume by Hour
    plt.subplot(2, 2, 3)
    df['hour'] = pd.to_datetime(df['timestamp']).dt.hour
    hourly_volume = df.groupby('hour')['transaction_id'].count()
    hourly_volume.plot(kind='line')
    plt.title('Transaction Volume by Hour')
    plt.xlabel('Hour of Day')
    plt.ylabel('Number of Transactions')

    # 4. Amount Distribution (Log Scale)
    plt.subplot(2, 2, 4)
    sns.histplot(data=df, x='amount', hue='fraud', bins=50, log_scale=True)
    plt.title('Amount Distribution by Fraud Status (Log Scale)')
    plt.xlabel('Amount (Log Scale)')
    plt.ylabel('Count')

    plt.tight_layout()
    plt.show()

    # Print key findings
    print("Key Findings:")
    print("-" * 50)
    print(f"1. Average transaction amount: ${df['amount'].mean():.2f}")
    print(f"2. Fraud transaction average: ${df[df['fraud']==1]['amount'].mean():.2f}")
    print(f"3. Non-fraud transaction average: ${df[df['fraud']==0]['amount'].mean():.2f}")
    print(f"4. Most common merchant category: {df['merchant_category'].mode()[0]}")
    print(f"5. Peak transaction hour: {hourly_volume.idxmax()}")

def engineer_features(df):
    """Perform feature engineering on the dataset"""
    # Create copy to avoid modifying original
    df_processed = df.copy()
    
    # 1. Time-based features
    df_processed['timestamp'] = pd.to_datetime(df_processed['timestamp'])
    df_processed['hour'] = df_processed['timestamp'].dt.hour
    df_processed['day_of_week'] = df_processed['timestamp'].dt.dayofweek
    df_processed['is_weekend'] = df_processed['day_of_week'].isin([5, 6]).astype(int)
    
    # 2. Amount-based features
    df_processed['amount_log'] = np.log1p(df_processed['amount'])
    
    # 3. Transaction frequency features
    customer_tx_counts = df_processed.groupby('customer_id')['transaction_id'].count()
    merchant_tx_counts = df_processed.groupby('merchant_id')['transaction_id'].count()
    
    df_processed['customer_tx_count'] = df_processed['customer_id'].map(customer_tx_counts)
    df_processed['merchant_tx_count'] = df_processed['merchant_id'].map(merchant_tx_counts)
    
    # 4. Encode categorical variables
    le = LabelEncoder()
    df_processed['merchant_category_encoded'] = le.fit_transform(df_processed['merchant_category'])
    
    # 5. Drop original columns we don't need
    columns_to_drop = ['transaction_id', 'timestamp', 'merchant_category']
    df_processed = df_processed.drop(columns=columns_to_drop)
    
    return df_processed

def prepare_data(df_processed):
    """Prepare data for modeling"""
    # Split features and target
    X = df_processed.drop('fraud', axis=1)
    y = df_processed['fraud']

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # Handle class imbalance using SMOTE
    smote = SMOTE(random_state=42)
    X_train_resampled, y_train_resampled = smote.fit_resample(X_train, y_train)

    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train_resampled)
    X_test_scaled = scaler.transform(X_test)

    print("\nDataset shapes:")
    print(f"Training set (after SMOTE): {X_train_scaled.shape}")
    print(f"Testing set: {X_test_scaled.shape}")
    print(f"\nClass distribution in training set (after SMOTE):")
    print(pd.Series(y_train_resampled).value_counts(normalize=True))

    return X_train_scaled, X_test_scaled, y_train_resampled, y_test, X.columns, scaler

def save_processed_data(X_train_scaled, X_test_scaled, y_train_resampled, y_test, feature_names, scaler):
    """Save processed datasets for later use"""
    # Create processed data directory if it doesn't exist
    processed_dir = '../data/processed'
    os.makedirs(processed_dir, exist_ok=True)

    # Save processed datasets
    np.save(f'{processed_dir}/X_train_scaled.npy', X_train_scaled)
    np.save(f'{processed_dir}/X_test_scaled.npy', X_test_scaled)
    np.save(f'{processed_dir}/y_train_resampled.npy', y_train_resampled)
    np.save(f'{processed_dir}/y_test.npy', y_test)

    # Save feature names for reference
    pd.Series(feature_names).to_csv(f'{processed_dir}/feature_names.csv', index=False)

    # Save scaler for future use
    joblib.dump(scaler, f'{processed_dir}/scaler.joblib')

    print("Processed data saved successfully!")
    print(f"Files saved in: {processed_dir}")
    print("\nSaved files:")
    print(os.listdir(processed_dir))

def main():
    # Load data
    df = load_fraud_dataset()
    
    # Analyze data
    analyze_dataset(df)
    
    # Visualize patterns
    visualize_patterns(df)
    
    # Process and prepare data
    df_processed = engineer_features(df)
    X_train_scaled, X_test_scaled, y_train_resampled, y_test, feature_names, scaler = prepare_data(df_processed)
    
    # Save processed data
    save_processed_data(X_train_scaled, X_test_scaled, y_train_resampled, y_test, feature_names, scaler)

if __name__ == "__main__":
    main()