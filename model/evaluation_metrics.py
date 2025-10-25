#!/usr/bin/env python3
"""
Comprehensive Evaluation Metrics for DBS Fraud Detection Challenge

Implements all required metrics:
- Confusion Matrix (TP, TN, FP, FN)
- F1 Score
- Precision and Recall (TPR)
- AUC-ROC (Area Under ROC Curve)
- AUC-PR (Area Under Precision-Recall Curve)
"""

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import (
    confusion_matrix,
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_curve,
    auc,
    precision_recall_curve,
    roc_auc_score,
    average_precision_score,
    classification_report
)
from typing import Dict, Tuple, Optional
import pandas as pd


class FraudDetectionMetrics:
    """
    Complete metrics suite for fraud detection evaluation.
    
    Implements all metrics specified in the DBS challenge:
    - Confusion Matrix components (TP, TN, FP, FN)
    - F1 Score = 2 * (Precision * Recall) / (Precision + Recall)
    - Precision = TP / (TP + FP)
    - Recall (TPR) = TP / (TP + FN)
    - AUC-ROC: Area under TPR vs FPR curve
    - AUC-PR: Area under Precision vs Recall curve
    """
    
    def __init__(self):
        self.results = {}
    
    def compute_confusion_matrix_components(
        self,
        y_true: np.ndarray,
        y_pred: np.ndarray
    ) -> Dict[str, int]:
        """
        Compute confusion matrix components.
        
        Returns:
            Dictionary with TP, TN, FP, FN counts
        """
        cm = confusion_matrix(y_true, y_pred)
        
        # For binary classification:
        # [[TN, FP],
        #  [FN, TP]]
        tn, fp, fn, tp = cm.ravel()
        
        return {
            'TP': int(tp),  # True Positives
            'TN': int(tn),  # True Negatives
            'FP': int(fp),  # False Positives
            'FN': int(fn)   # False Negatives
        }
    
    def compute_all_metrics(
        self,
        y_true: np.ndarray,
        y_pred: np.ndarray,
        y_prob: Optional[np.ndarray] = None
    ) -> Dict[str, float]:
        """
        Compute all evaluation metrics.
        
        Args:
            y_true: True labels (0 or 1)
            y_pred: Predicted labels (0 or 1)
            y_prob: Predicted probabilities for positive class (optional)
            
        Returns:
            Dictionary containing all metrics
        """
        # Confusion matrix components
        cm_components = self.compute_confusion_matrix_components(y_true, y_pred)
        tp, tn, fp, fn = cm_components['TP'], cm_components['TN'], cm_components['FP'], cm_components['FN']
        
        # Basic metrics
        metrics = {
            'TP': tp,
            'TN': tn,
            'FP': fp,
            'FN': fn,
            'accuracy': accuracy_score(y_true, y_pred),
            'precision': precision_score(y_true, y_pred, zero_division=0),
            'recall': recall_score(y_true, y_pred, zero_division=0),  # Same as TPR
            'f1_score': f1_score(y_true, y_pred, zero_division=0)
        }
        
        # TPR and FPR (for manual verification)
        metrics['TPR'] = tp / (tp + fn) if (tp + fn) > 0 else 0  # True Positive Rate
        metrics['FPR'] = fp / (fp + tn) if (fp + tn) > 0 else 0  # False Positive Rate
        
        # AUC metrics (require probability scores)
        if y_prob is not None:
            try:
                metrics['AUC_ROC'] = roc_auc_score(y_true, y_prob)
                metrics['AUC_PR'] = average_precision_score(y_true, y_prob)
            except ValueError as e:
                print(f"Warning: Could not compute AUC metrics: {e}")
                metrics['AUC_ROC'] = 0.0
                metrics['AUC_PR'] = 0.0
        
        self.results = metrics
        return metrics
    
    def print_metrics(self, metrics: Dict[str, float], model_name: str = "Model"):
        """
        Print metrics in a formatted table.
        
        Args:
            metrics: Dictionary of computed metrics
            model_name: Name of the model
        """
        print("\n" + "=" * 70)
        print(f"📊 {model_name} Performance Metrics")
        print("=" * 70)
        
        # Confusion Matrix
        print("\n🔢 Confusion Matrix Components:")
        print(f"   True Positives (TP):  {metrics.get('TP', 'N/A'):>6}")
        print(f"   True Negatives (TN):  {metrics.get('TN', 'N/A'):>6}")
        print(f"   False Positives (FP): {metrics.get('FP', 'N/A'):>6}")
        print(f"   False Negatives (FN): {metrics.get('FN', 'N/A'):>6}")
        
        # Classification Metrics
        print("\n📈 Classification Metrics:")
        print(f"   Accuracy:   {metrics.get('accuracy', 0):.4f}")
        print(f"   Precision:  {metrics.get('precision', 0):.4f}")
        print(f"   Recall/TPR: {metrics.get('recall', 0):.4f}")
        print(f"   F1 Score:   {metrics.get('f1_score', 0):.4f}")
        
        # AUC Metrics
        if 'AUC_ROC' in metrics:
            print("\n🎯 AUC Metrics:")
            print(f"   AUC-ROC:    {metrics['AUC_ROC']:.4f}")
            print(f"   AUC-PR:     {metrics['AUC_PR']:.4f}")
        
        print("=" * 70 + "\n")
    
    def plot_confusion_matrix(
        self,
        y_true: np.ndarray,
        y_pred: np.ndarray,
        title: str = "Confusion Matrix",
        save_path: Optional[str] = None
    ):
        """
        Plot confusion matrix heatmap.
        
        Args:
            y_true: True labels
            y_pred: Predicted labels
            title: Plot title
            save_path: Path to save figure (optional)
        """
        cm = confusion_matrix(y_true, y_pred)
        
        plt.figure(figsize=(8, 6))
        sns.heatmap(
            cm,
            annot=True,
            fmt='d',
            cmap='Blues',
            xticklabels=['Legitimate (0)', 'Fraud (1)'],
            yticklabels=['Legitimate (0)', 'Fraud (1)']
        )
        plt.title(title, fontsize=14, fontweight='bold')
        plt.ylabel('True Label', fontsize=12)
        plt.xlabel('Predicted Label', fontsize=12)
        
        # Add text annotations for TP, TN, FP, FN
        tn, fp, fn, tp = cm.ravel()
        plt.text(0.5, -0.15, f'TN={tn}', ha='center', transform=plt.gca().transAxes, fontsize=10)
        plt.text(1.5, -0.15, f'FP={fp}', ha='center', transform=plt.gca().transAxes, fontsize=10)
        plt.text(0.5, 1.15, f'FN={fn}', ha='center', transform=plt.gca().transAxes, fontsize=10)
        plt.text(1.5, 1.15, f'TP={tp}', ha='center', transform=plt.gca().transAxes, fontsize=10)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        plt.show()
    
    def plot_roc_curve(
        self,
        y_true: np.ndarray,
        y_prob: np.ndarray,
        title: str = "ROC Curve",
        save_path: Optional[str] = None
    ):
        """
        Plot ROC (Receiver Operating Characteristic) curve.
        
        ROC curve plots TPR (True Positive Rate) vs FPR (False Positive Rate)
        at various threshold settings.
        
        Args:
            y_true: True labels
            y_prob: Predicted probabilities for positive class
            title: Plot title
            save_path: Path to save figure (optional)
        """
        fpr, tpr, thresholds = roc_curve(y_true, y_prob)
        roc_auc = auc(fpr, tpr)
        
        plt.figure(figsize=(8, 6))
        plt.plot(
            fpr, tpr,
            color='darkorange',
            lw=2,
            label=f'ROC curve (AUC = {roc_auc:.4f})'
        )
        plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--', label='Random Classifier')
        
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('False Positive Rate (FPR)', fontsize=12)
        plt.ylabel('True Positive Rate (TPR)', fontsize=12)
        plt.title(title, fontsize=14, fontweight='bold')
        plt.legend(loc="lower right", fontsize=10)
        plt.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        plt.show()
        
        return roc_auc
    
    def plot_precision_recall_curve(
        self,
        y_true: np.ndarray,
        y_prob: np.ndarray,
        title: str = "Precision-Recall Curve",
        save_path: Optional[str] = None
    ):
        """
        Plot Precision-Recall curve.
        
        PR curve is better for imbalanced datasets (like fraud detection)
        where positive class is rare.
        
        Args:
            y_true: True labels
            y_prob: Predicted probabilities for positive class
            title: Plot title
            save_path: Path to save figure (optional)
        """
        precision, recall, thresholds = precision_recall_curve(y_true, y_prob)
        pr_auc = auc(recall, precision)
        avg_precision = average_precision_score(y_true, y_prob)
        
        plt.figure(figsize=(8, 6))
        plt.plot(
            recall, precision,
            color='darkorange',
            lw=2,
            label=f'PR curve (AUC = {pr_auc:.4f}, AP = {avg_precision:.4f})'
        )
        
        # Baseline (random classifier would have precision = fraction of positive samples)
        baseline = y_true.sum() / len(y_true)
        plt.axhline(y=baseline, color='navy', linestyle='--', lw=2, label=f'Baseline (P={baseline:.4f})')
        
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('Recall (TPR)', fontsize=12)
        plt.ylabel('Precision', fontsize=12)
        plt.title(title, fontsize=14, fontweight='bold')
        plt.legend(loc="lower left", fontsize=10)
        plt.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        plt.show()
        
        return pr_auc
    
    def plot_all_metrics(
        self,
        y_true: np.ndarray,
        y_pred: np.ndarray,
        y_prob: Optional[np.ndarray] = None,
        model_name: str = "Model",
        save_dir: Optional[str] = None
    ):
        """
        Generate all visualization plots.
        
        Args:
            y_true: True labels
            y_pred: Predicted labels
            y_prob: Predicted probabilities (optional)
            model_name: Name of the model
            save_dir: Directory to save plots (optional)
        """
        # Confusion Matrix
        save_path_cm = f"{save_dir}/{model_name}_confusion_matrix.png" if save_dir else None
        self.plot_confusion_matrix(y_true, y_pred, f"{model_name} - Confusion Matrix", save_path_cm)
        
        # ROC and PR curves (if probabilities available)
        if y_prob is not None:
            save_path_roc = f"{save_dir}/{model_name}_roc_curve.png" if save_dir else None
            self.plot_roc_curve(y_true, y_prob, f"{model_name} - ROC Curve", save_path_roc)
            
            save_path_pr = f"{save_dir}/{model_name}_pr_curve.png" if save_dir else None
            self.plot_precision_recall_curve(y_true, y_prob, f"{model_name} - Precision-Recall Curve", save_path_pr)
    
    def compare_models(
        self,
        results_dict: Dict[str, Dict[str, float]],
        save_path: Optional[str] = None
    ):
        """
        Compare multiple models side by side.
        
        Args:
            results_dict: Dictionary mapping model names to their metrics
            save_path: Path to save comparison plot (optional)
        """
        df = pd.DataFrame(results_dict).T
        
        # Select key metrics for comparison
        key_metrics = ['accuracy', 'precision', 'recall', 'f1_score']
        if 'AUC_ROC' in df.columns:
            key_metrics.extend(['AUC_ROC', 'AUC_PR'])
        
        df_plot = df[key_metrics]
        
        # Create comparison plot
        fig, ax = plt.subplots(figsize=(12, 6))
        df_plot.plot(kind='bar', ax=ax, width=0.8)
        
        ax.set_title('Model Performance Comparison', fontsize=14, fontweight='bold')
        ax.set_xlabel('Model', fontsize=12)
        ax.set_ylabel('Score', fontsize=12)
        ax.set_ylim([0, 1.1])
        ax.legend(title='Metrics', bbox_to_anchor=(1.05, 1), loc='upper left')
        ax.grid(True, alpha=0.3, axis='y')
        
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        plt.show()
        
        # Print comparison table
        print("\n" + "=" * 100)
        print("📊 Model Comparison Summary")
        print("=" * 100)
        print(df_plot.to_string())
        print("=" * 100 + "\n")


# Example usage and testing
if __name__ == "__main__":
    print("=" * 70)
    print("Evaluation Metrics Module - DBS Fraud Detection Challenge")
    print("=" * 70)
    
    # Create synthetic test data
    np.random.seed(42)
    n_samples = 1000
    
    # Simulate imbalanced fraud dataset (99% legitimate, 1% fraud)
    y_true = np.random.choice([0, 1], size=n_samples, p=[0.99, 0.01])
    
    # Simulate predictions (with some errors)
    y_prob = np.random.rand(n_samples)
    y_prob[y_true == 1] += 0.3  # Boost fraud probabilities
    y_prob = np.clip(y_prob, 0, 1)
    y_pred = (y_prob > 0.5).astype(int)
    
    print(f"\n📊 Test Data: {n_samples} samples")
    print(f"   True fraud rate: {y_true.mean():.2%}")
    print(f"   Predicted fraud rate: {y_pred.mean():.2%}")
    
    # Compute all metrics
    evaluator = FraudDetectionMetrics()
    metrics = evaluator.compute_all_metrics(y_true, y_pred, y_prob)
    evaluator.print_metrics(metrics, "Test Model")
    
    # Generate plots
    print("\n📈 Generating visualization plots...")
    evaluator.plot_all_metrics(y_true, y_pred, y_prob, "Test Model")
    
    print("\n" + "=" * 70)
    print("✓ Evaluation metrics module ready for challenge!")
    print("=" * 70)
