#!/usr/bin/env python3
"""
DBS Fraud Detection Challenge - Complete Demo Script

This script demonstrates the full quantum-enhanced fraud detection pipeline:
1. Load and preprocess data
2. Apply quantum feature selection
3. Train QSVM model
4. Train classical baseline models
5. Compare performance metrics
6. Generate visualizations

Usage:
    python demo/run_challenge_demo.py --dataset data/processed/X_train_scaled.npy
"""

import sys
import os
import argparse
import numpy as np
import pandas as pd
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from model.qsvm_classifier import QSVM, QuantumFeatureSelector
from model.evaluation_metrics import FraudDetectionMetrics
from model.qcentroid_config import get_qcentroid_client

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
import xgboost as xgb


def load_data(data_dir='../data/processed'):
    """Load preprocessed fraud detection data"""
    print("=" * 70)
    print("📂 Loading Data")
    print("=" * 70)
    
    try:
        X_train = np.load(f'{data_dir}/X_train_scaled.npy')
        X_test = np.load(f'{data_dir}/X_test_scaled.npy')
        y_train = np.load(f'{data_dir}/y_train_resampled.npy')
        y_test = np.load(f'{data_dir}/y_test.npy')
        
        print(f"✓ Training set: {X_train.shape[0]} samples, {X_train.shape[1]} features")
        print(f"✓ Test set: {X_test.shape[0]} samples")
        print(f"✓ Training fraud rate: {y_train.mean():.2%}")
        print(f"✓ Test fraud rate: {y_test.mean():.2%}")
        
        return X_train, X_test, y_train, y_test
    
    except FileNotFoundError:
        print("⚠️  Preprocessed data not found. Creating synthetic data...")
        return create_synthetic_data()


def create_synthetic_data():
    """Create synthetic fraud data for demonstration"""
    np.random.seed(42)
    
    n_train = 1000
    n_test = 200
    n_features = 10
    
    # Generate synthetic features
    X_train = np.random.randn(n_train, n_features)
    X_test = np.random.randn(n_test, n_features)
    
    # Create fraud labels (1% fraud rate)
    # Fraud depends on combinations of features
    fraud_score_train = X_train[:, 0] + 0.5 * X_train[:, 1] - 0.3 * X_train[:, 2]
    fraud_score_test = X_test[:, 0] + 0.5 * X_test[:, 1] - 0.3 * X_test[:, 2]
    
    y_train = (fraud_score_train > 1.5).astype(int)
    y_test = (fraud_score_test > 1.5).astype(int)
    
    # Ensure at least 1% fraud
    if y_train.mean() < 0.01:
        fraud_indices = np.where(fraud_score_train > np.percentile(fraud_score_train, 99))[0]
        y_train[fraud_indices] = 1
    
    if y_test.mean() < 0.01:
        fraud_indices = np.where(fraud_score_test > np.percentile(fraud_score_test, 99))[0]
        y_test[fraud_indices] = 1
    
    print(f"✓ Created synthetic training set: {X_train.shape[0]} samples, {X_train.shape[1]} features")
    print(f"✓ Created synthetic test set: {X_test.shape[0]} samples")
    print(f"✓ Training fraud rate: {y_train.mean():.2%}")
    print(f"✓ Test fraud rate: {y_test.mean():.2%}")
    
    return X_train, X_test, y_train, y_test


def train_classical_baselines(X_train, y_train, X_test, y_test):
    """Train classical baseline models for comparison"""
    print("\n" + "=" * 70)
    print("🔬 Training Classical Baseline Models")
    print("=" * 70)
    
    models = {}
    evaluator = FraudDetectionMetrics()
    
    # 1. Logistic Regression
    print("\n[1/4] Training Logistic Regression...")
    lr = LogisticRegression(class_weight='balanced', max_iter=1000, random_state=42)
    lr.fit(X_train, y_train)
    lr_pred = lr.predict(X_test)
    lr_prob = lr.predict_proba(X_test)[:, 1]
    lr_metrics = evaluator.compute_all_metrics(y_test, lr_pred, lr_prob)
    models['Logistic Regression'] = (lr, lr_metrics, lr_prob)
    evaluator.print_metrics(lr_metrics, "Logistic Regression")
    
    # 2. Random Forest
    print("\n[2/4] Training Random Forest...")
    rf = RandomForestClassifier(n_estimators=100, class_weight='balanced', random_state=42)
    rf.fit(X_train, y_train)
    rf_pred = rf.predict(X_test)
    rf_prob = rf.predict_proba(X_test)[:, 1]
    rf_metrics = evaluator.compute_all_metrics(y_test, rf_pred, rf_prob)
    models['Random Forest'] = (rf, rf_metrics, rf_prob)
    evaluator.print_metrics(rf_metrics, "Random Forest")
    
    # 3. Classical SVM (RBF kernel)
    print("\n[3/4] Training Classical SVM (RBF)...")
    svm = SVC(kernel='rbf', probability=True, class_weight='balanced', random_state=42)
    svm.fit(X_train, y_train)
    svm_pred = svm.predict(X_test)
    svm_prob = svm.predict_proba(X_test)[:, 1]
    svm_metrics = evaluator.compute_all_metrics(y_test, svm_pred, svm_prob)
    models['Classical SVM'] = (svm, svm_metrics, svm_prob)
    evaluator.print_metrics(svm_metrics, "Classical SVM (RBF)")
    
    # 4. XGBoost
    print("\n[4/4] Training XGBoost...")
    xgb_model = xgb.XGBClassifier(
        scale_pos_weight=len(y_train[y_train==0]) / len(y_train[y_train==1]),
        learning_rate=0.1,
        n_estimators=100,
        max_depth=5,
        random_state=42
    )
    xgb_model.fit(X_train, y_train)
    xgb_pred = xgb_model.predict(X_test)
    xgb_prob = xgb_model.predict_proba(X_test)[:, 1]
    xgb_metrics = evaluator.compute_all_metrics(y_test, xgb_pred, xgb_prob)
    models['XGBoost'] = (xgb_model, xgb_metrics, xgb_prob)
    evaluator.print_metrics(xgb_metrics, "XGBoost")
    
    return models


def train_quantum_model(X_train, y_train, X_test, y_test, n_features=4):
    """Train QSVM model with quantum feature selection"""
    print("\n" + "=" * 70)
    print("⚛️  Training Quantum Support Vector Machine")
    print("=" * 70)
    
    # Limit to small number of features for NISQ devices
    print(f"\n🔬 Using first {n_features} features for quantum model (NISQ constraint)")
    X_train_quantum = X_train[:, :n_features]
    X_test_quantum = X_test[:, :n_features]
    
    # Initialize and train QSVM
    print("\n[1/2] Initializing QSVM with ZZ-FeatureMap...")
    qsvm = QSVM(n_features=n_features, reps=2, entanglement='full', C=1.0)
    
    print("[2/2] Training QSVM (this may take a few minutes)...")
    qsvm.fit(X_train_quantum, y_train)
    
    # Evaluate
    print("\n📊 Evaluating QSVM...")
    qsvm_pred = qsvm.predict(X_test_quantum)
    qsvm_prob = qsvm.predict_proba(X_test_quantum)[:, 1]
    
    evaluator = FraudDetectionMetrics()
    qsvm_metrics = evaluator.compute_all_metrics(y_test, qsvm_pred, qsvm_prob)
    evaluator.print_metrics(qsvm_metrics, "QSVM")
    
    return qsvm, qsvm_metrics, qsvm_prob


def compare_all_models(classical_models, qsvm_metrics, y_test, save_dir='./results'):
    """Compare all models and generate comparison plots"""
    print("\n" + "=" * 70)
    print("📊 Model Comparison")
    print("=" * 70)
    
    # Compile all metrics
    all_metrics = {}
    for name, (model, metrics, prob) in classical_models.items():
        all_metrics[name] = metrics
    all_metrics['QSVM'] = qsvm_metrics
    
    # Create comparison
    evaluator = FraudDetectionMetrics()
    
    # Ensure output directory exists
    os.makedirs(save_dir, exist_ok=True)
    
    evaluator.compare_models(all_metrics, save_path=f'{save_dir}/model_comparison.png')
    
    # Summary table
    print("\n📋 Performance Summary:")
    print("-" * 70)
    df = pd.DataFrame(all_metrics).T
    key_cols = ['f1_score', 'precision', 'recall', 'AUC_ROC', 'AUC_PR']
    print(df[key_cols].to_string())
    print("-" * 70)


def main():
    parser = argparse.ArgumentParser(description='DBS Fraud Detection Challenge Demo')
    parser.add_argument('--data-dir', default='../data/processed', help='Path to preprocessed data')
    parser.add_argument('--n-features', type=int, default=4, help='Number of features for QSVM')
    parser.add_argument('--output-dir', default='./results', help='Output directory for results')
    args = parser.parse_args()
    
    print("\n" + "=" * 70)
    print("🚀 DBS FRAUD DETECTION CHALLENGE - QUANTUM ML DEMO")
    print("=" * 70)
    print("\nThis demo showcases quantum-enhanced fraud detection using:")
    print("  • ZZ-FeatureMap quantum encoding")
    print("  • Quantum kernel SVM (QSVM)")
    print("  • Comparison with classical ML baselines")
    print("  • Comprehensive performance metrics (AUC-ROC, AUC-PR, F1)")
    
    # Check quantum backend
    print("\n⚛️  Checking quantum backend...")
    client = get_qcentroid_client()
    if client.is_available():
        info = client.get_backend_info()
        print(f"✓ Quantum backend: {info['type']}")
        print(f"✓ Max qubits: {info['max_qubits']}")
    else:
        print("⚠️  Quantum backend not available. Install qiskit:")
        print("   pip install qiskit qiskit-aer qiskit-machine-learning")
        return
    
    # Load data
    X_train, X_test, y_train, y_test = load_data(args.data_dir)
    
    # Train classical models
    classical_models = train_classical_baselines(X_train, y_train, X_test, y_test)
    
    # Train quantum model
    qsvm, qsvm_metrics, qsvm_prob = train_quantum_model(
        X_train, y_train, X_test, y_test,
        n_features=args.n_features
    )
    
    # Compare all models
    compare_all_models(classical_models, qsvm_metrics, y_test, save_dir=args.output_dir)
    
    print("\n" + "=" * 70)
    print("✅ DEMO COMPLETE!")
    print("=" * 70)
    print(f"\n📁 Results saved to: {args.output_dir}")
    print("\n🎯 Next Steps:")
    print("   1. Review the performance comparison")
    print("   2. Experiment with different feature selections")
    print("   3. Try real Kaggle datasets")
    print("   4. Submit to QCentroid challenge API")
    print("\n" + "=" * 70)


if __name__ == "__main__":
    main()
