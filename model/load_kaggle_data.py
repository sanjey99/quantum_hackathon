#!/usr/bin/env python3
"""
Load and preprocess the Kaggle Credit Card Fraud dataset.

This script prepares the data for the DBS Challenge:
1. Loads creditcard.csv
2. Handles class imbalance with SMOTE
3. Scales features
4. Saves processed data for QSVM training
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from imblearn.over_sampling import SMOTE
import os

def load_and_preprocess():
    """Load and preprocess the Kaggle credit card fraud dataset"""
    
    print("=" * 70)
    print("📊 Loading Kaggle Credit Card Fraud Dataset")
    print("=" * 70)
    
    # Load dataset
    df = pd.read_csv('../data/raw/creditcard.csv')
    
    print(f"\n✓ Dataset loaded: {df.shape[0]:,} transactions, {df.shape[1]} features")
    print(f"  Features: {', '.join(df.columns.tolist())}")
    
    # Check fraud rate
    fraud_rate = df['Class'].mean()
    print(f"\n📈 Fraud Distribution:")
    print(f"  Legitimate (0): {(df['Class'] == 0).sum():,} ({1-fraud_rate:.2%})")
    print(f"  Fraud (1):      {(df['Class'] == 1).sum():,} ({fraud_rate:.4%})")
    print(f"  ⚠️  Highly imbalanced dataset! (1:{int(1/fraud_rate)})")
    
    # Separate features and target
    X = df.drop('Class', axis=1)
    y = df['Class']
    
    print(f"\n🔬 Feature Analysis:")
    print(f"  V1-V28: PCA-transformed features (already scaled)")
    print(f"  Time:   Seconds elapsed between transactions")
    print(f"  Amount: Transaction amount")
    
    # Check for missing values
    missing = df.isnull().sum().sum()
    print(f"\n✓ Missing values: {missing}")
    
    # Split data
    print(f"\n🔀 Splitting data (80/20 train/test, stratified)...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, 
        test_size=0.2, 
        stratify=y, 
        random_state=42
    )
    
    print(f"  Training set:   {X_train.shape[0]:,} samples")
    print(f"  Test set:       {X_test.shape[0]:,} samples")
    print(f"  Train fraud %:  {y_train.mean():.4%}")
    print(f"  Test fraud %:   {y_test.mean():.4%}")
    
    # Scale Time and Amount (V1-V28 already scaled from PCA)
    print(f"\n⚙️  Scaling 'Time' and 'Amount' features...")
    scaler = StandardScaler()
    
    # Only scale Time and Amount
    X_train_scaled = X_train.copy()
    X_test_scaled = X_test.copy()
    
    X_train_scaled[['Time', 'Amount']] = scaler.fit_transform(X_train[['Time', 'Amount']])
    X_test_scaled[['Time', 'Amount']] = scaler.transform(X_test[['Time', 'Amount']])
    
    print(f"✓ Time scaled:   Mean={X_train_scaled['Time'].mean():.2f}, Std={X_train_scaled['Time'].std():.2f}")
    print(f"✓ Amount scaled: Mean={X_train_scaled['Amount'].mean():.2f}, Std={X_train_scaled['Amount'].std():.2f}")
    
    # Apply SMOTE to balance training data
    print(f"\n🔄 Applying SMOTE to balance training data...")
    print(f"  Before SMOTE: {y_train.value_counts().to_dict()}")
    
    smote = SMOTE(random_state=42, k_neighbors=5)
    X_train_balanced, y_train_balanced = smote.fit_resample(X_train_scaled, y_train)
    
    print(f"  After SMOTE:  Legitimate={len(y_train_balanced[y_train_balanced==0]):,}, Fraud={len(y_train_balanced[y_train_balanced==1]):,}")
    print(f"  New fraud %:  {y_train_balanced.mean():.2%}")
    
    # Create output directory
    os.makedirs('../data/processed', exist_ok=True)
    
    # Save processed data
    print(f"\n💾 Saving processed data...")
    np.save('../data/processed/X_train_scaled.npy', X_train_balanced.values)
    np.save('../data/processed/X_test_scaled.npy', X_test_scaled.values)
    np.save('../data/processed/y_train_resampled.npy', y_train_balanced.values)
    np.save('../data/processed/y_test.npy', y_test.values)
    
    # Save feature names
    feature_names = X_train_scaled.columns.tolist()
    pd.DataFrame(feature_names, columns=['feature']).to_csv('../data/processed/feature_names.csv', index=False)
    
    print(f"✓ Saved: X_train_scaled.npy ({X_train_balanced.shape})")
    print(f"✓ Saved: X_test_scaled.npy ({X_test_scaled.shape})")
    print(f"✓ Saved: y_train_resampled.npy ({y_train_balanced.shape})")
    print(f"✓ Saved: y_test.npy ({y_test.shape})")
    print(f"✓ Saved: feature_names.csv ({len(feature_names)} features)")
    
    # Summary statistics
    print(f"\n" + "=" * 70)
    print("📊 PREPROCESSING SUMMARY")
    print("=" * 70)
    print(f"Original dataset:      {df.shape[0]:,} transactions, {df.shape[1]-1} features")
    print(f"Training samples:      {X_train_balanced.shape[0]:,} (after SMOTE)")
    print(f"Test samples:          {X_test_scaled.shape[0]:,}")
    print(f"Features:              {X_train_balanced.shape[1]}")
    print(f"Train fraud rate:      {y_train_balanced.mean():.2%} (balanced)")
    print(f"Test fraud rate:       {y_test.mean():.4%} (original distribution)")
    print("=" * 70)
    
    print(f"\n✅ Data preprocessing complete!")
    print(f"\n🚀 Next steps:")
    print(f"   1. Run QSVM feature selection: python qsvm_classifier.py")
    print(f"   2. Train models: python fraud_model_development.py")
    print(f"   3. Run demo: python ../demo/run_challenge_demo.py")
    
    return X_train_balanced, X_test_scaled, y_train_balanced, y_test, feature_names


if __name__ == "__main__":
    load_and_preprocess()
