#!/usr/bin/env python3
"""
Quantum Support Vector Machine (QSVM) Implementation
for DBS Fraud Detection Challenge

This module implements QSVM using:
- ZZ-FeatureMap for quantum encoding
- Quantum kernel computation
- Classical SVM optimization
- Feature selection capabilities
"""

import numpy as np
from typing import List, Tuple, Optional
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
import warnings
warnings.filterwarnings('ignore')

# Try to import Qiskit
try:
    from qiskit import QuantumCircuit
    from qiskit.circuit import ParameterVector
    from qiskit.circuit.library import ZZFeatureMap, PauliFeatureMap
    from qiskit_aer import AerSimulator
    from qiskit.primitives import Sampler
    from qiskit_machine_learning.kernels import FidelityQuantumKernel
    QISKIT_AVAILABLE = True
except ImportError:
    print("Warning: Qiskit not available. Install with: pip install qiskit qiskit-aer qiskit-machine-learning")
    QISKIT_AVAILABLE = False


class ZZFeatureMapEncoder:
    """
    ZZ-FeatureMap encoder for quantum states.
    
    This encoding uses parametrized rotation and entangling gates
    to represent classical features in quantum Hilbert space.
    
    Mathematical formulation:
    U(x) = H⊗n · U_Φ(x) · H⊗n
    where U_Φ(x) contains Z rotations and ZZ entangling gates
    """
    
    def __init__(self, n_features: int, reps: int = 2, entanglement: str = 'full'):
        """
        Initialize ZZ-FeatureMap encoder.
        
        Args:
            n_features: Number of features (qubits)
            reps: Number of repetitions of the feature map circuit
            entanglement: Entanglement pattern ('full', 'linear', 'circular')
        """
        self.n_features = n_features
        self.reps = reps
        self.entanglement = entanglement
        
        if QISKIT_AVAILABLE:
            self.feature_map = ZZFeatureMap(
                feature_dimension=n_features,
                reps=reps,
                entanglement=entanglement
            )
        else:
            raise ImportError("Qiskit is required for ZZ-FeatureMap encoding")
    
    def encode(self, x: np.ndarray) -> QuantumCircuit:
        """
        Encode classical data into quantum state.
        
        Args:
            x: Classical feature vector (shape: n_features)
            
        Returns:
            Quantum circuit with encoded data
        """
        return self.feature_map.bind_parameters(x)
    
    def get_circuit(self) -> QuantumCircuit:
        """Get the parametric feature map circuit"""
        return self.feature_map


class QuantumKernelComputer:
    """
    Compute quantum kernels between data samples.
    
    The quantum kernel is defined as:
    K(x_i, x_j) = |⟨φ(x_i)|φ(x_j)⟩|²
    
    where φ(x) = U(x)|0⟩ is the quantum state after encoding.
    """
    
    def __init__(self, feature_map: ZZFeatureMap, backend=None):
        """
        Initialize quantum kernel computer.
        
        Args:
            feature_map: ZZ-FeatureMap for encoding
            backend: Quantum backend (simulator or real device)
        """
        self.feature_map = feature_map
        
        if backend is None:
            self.backend = AerSimulator()
        else:
            self.backend = backend
        
        # Create quantum kernel using Qiskit ML
        if QISKIT_AVAILABLE:
            self.quantum_kernel = FidelityQuantumKernel(feature_map=feature_map)
    
    def compute_kernel_matrix(self, X1: np.ndarray, X2: Optional[np.ndarray] = None) -> np.ndarray:
        """
        Compute kernel matrix K where K[i,j] = K(x_i, x_j).
        
        Args:
            X1: First dataset (shape: n_samples_1, n_features)
            X2: Second dataset (shape: n_samples_2, n_features)
                If None, compute K(X1, X1)
        
        Returns:
            Kernel matrix (shape: n_samples_1, n_samples_2)
        """
        if X2 is None:
            X2 = X1
        
        # Compute quantum kernel matrix
        kernel_matrix = self.quantum_kernel.evaluate(X1, X2)
        return kernel_matrix


class QSVM:
    """
    Quantum Support Vector Machine for fraud detection.
    
    Uses quantum kernels to implicitly work in high-dimensional
    Hilbert space for better feature representation.
    """
    
    def __init__(
        self,
        n_features: int,
        reps: int = 2,
        entanglement: str = 'full',
        C: float = 1.0,
        backend=None
    ):
        """
        Initialize QSVM.
        
        Args:
            n_features: Number of features (qubits)
            reps: Number of repetitions in ZZ-FeatureMap
            entanglement: Entanglement pattern
            C: SVM regularization parameter
            backend: Quantum backend
        """
        self.n_features = n_features
        self.C = C
        
        # Create ZZ-FeatureMap encoder
        self.encoder = ZZFeatureMapEncoder(n_features, reps, entanglement)
        
        # Create quantum kernel computer
        self.kernel_computer = QuantumKernelComputer(
            self.encoder.feature_map,
            backend
        )
        
        # Classical SVM with precomputed quantum kernel
        self.svm = SVC(kernel='precomputed', C=C, probability=True)
        
        self.X_train = None
        self.is_trained = False
    
    def fit(self, X_train: np.ndarray, y_train: np.ndarray):
        """
        Train QSVM on training data.
        
        Args:
            X_train: Training features (shape: n_samples, n_features)
            y_train: Training labels (shape: n_samples)
        """
        print(f"Computing quantum kernel matrix for {len(X_train)} training samples...")
        
        # Compute kernel matrix for training data
        K_train = self.kernel_computer.compute_kernel_matrix(X_train)
        
        print("Training classical SVM with quantum kernel...")
        # Train SVM with precomputed kernel
        self.svm.fit(K_train, y_train)
        
        # Store training data for prediction
        self.X_train = X_train
        self.is_trained = True
        
        print("✓ QSVM training complete")
    
    def predict(self, X_test: np.ndarray) -> np.ndarray:
        """
        Predict labels for test data.
        
        Args:
            X_test: Test features (shape: n_samples, n_features)
            
        Returns:
            Predicted labels (shape: n_samples)
        """
        if not self.is_trained:
            raise ValueError("Model must be trained before prediction")
        
        # Compute kernel matrix between test and training data
        K_test = self.kernel_computer.compute_kernel_matrix(X_test, self.X_train)
        
        # Predict using SVM
        return self.svm.predict(K_test)
    
    def predict_proba(self, X_test: np.ndarray) -> np.ndarray:
        """
        Predict class probabilities for test data.
        
        Args:
            X_test: Test features (shape: n_samples, n_features)
            
        Returns:
            Class probabilities (shape: n_samples, 2)
        """
        if not self.is_trained:
            raise ValueError("Model must be trained before prediction")
        
        # Compute kernel matrix between test and training data
        K_test = self.kernel_computer.compute_kernel_matrix(X_test, self.X_train)
        
        # Predict probabilities using SVM
        return self.svm.predict_proba(K_test)
    
    def score(self, X_test: np.ndarray, y_test: np.ndarray) -> float:
        """
        Compute accuracy on test data.
        
        Args:
            X_test: Test features
            y_test: True test labels
            
        Returns:
            Accuracy score
        """
        y_pred = self.predict(X_test)
        return accuracy_score(y_test, y_pred)


class QuantumFeatureSelector:
    """
    Quantum-enhanced feature selection using quantum kernels.
    
    Goal: Find minimal feature subset z ∈ {0,1}^d that maximizes
    classification accuracy while minimizing |z|.
    """
    
    def __init__(
        self,
        n_features: int,
        C: float = 1.0,
        max_features: int = None
    ):
        """
        Initialize quantum feature selector.
        
        Args:
            n_features: Total number of features
            C: SVM regularization parameter
            max_features: Maximum number of features to select
        """
        self.n_features = n_features
        self.C = C
        self.max_features = max_features or min(n_features, 8)  # NISQ constraint
        self.selected_features = None
        self.qsvm = None
    
    def select_features_greedy(
        self,
        X_train: np.ndarray,
        y_train: np.ndarray,
        X_val: np.ndarray,
        y_val: np.ndarray
    ) -> List[int]:
        """
        Greedy forward feature selection using quantum kernels.
        
        Args:
            X_train: Training features
            y_train: Training labels
            X_val: Validation features
            y_val: Validation labels
            
        Returns:
            List of selected feature indices
        """
        selected = []
        remaining = list(range(self.n_features))
        best_score = 0.0
        
        print(f"Starting quantum feature selection (max {self.max_features} features)...")
        
        for i in range(self.max_features):
            best_feature = None
            current_best_score = best_score
            
            for feature in remaining:
                # Try adding this feature
                trial_features = selected + [feature]
                
                # Extract selected features
                X_train_subset = X_train[:, trial_features]
                X_val_subset = X_val[:, trial_features]
                
                # Train QSVM with this feature subset
                qsvm = QSVM(n_features=len(trial_features), C=self.C)
                qsvm.fit(X_train_subset, y_train)
                
                # Evaluate on validation set
                score = qsvm.score(X_val_subset, y_val)
                
                print(f"  Feature {feature}: score = {score:.4f}")
                
                if score > current_best_score:
                    current_best_score = score
                    best_feature = feature
            
            if best_feature is not None:
                selected.append(best_feature)
                remaining.remove(best_feature)
                best_score = current_best_score
                print(f"✓ Selected feature {best_feature} (score: {best_score:.4f})")
            else:
                print("No improvement, stopping feature selection")
                break
        
        self.selected_features = selected
        return selected
    
    def fit(
        self,
        X_train: np.ndarray,
        y_train: np.ndarray,
        selected_features: Optional[List[int]] = None
    ):
        """
        Train QSVM with selected features.
        
        Args:
            X_train: Training features
            y_train: Training labels
            selected_features: Feature indices to use (if None, use previously selected)
        """
        if selected_features is not None:
            self.selected_features = selected_features
        
        if self.selected_features is None:
            raise ValueError("No features selected. Run select_features_greedy first.")
        
        # Extract selected features
        X_train_subset = X_train[:, self.selected_features]
        
        # Train QSVM
        self.qsvm = QSVM(n_features=len(self.selected_features), C=self.C)
        self.qsvm.fit(X_train_subset, y_train)
    
    def predict(self, X_test: np.ndarray) -> np.ndarray:
        """Predict using QSVM with selected features"""
        if self.qsvm is None:
            raise ValueError("Model not trained. Call fit() first.")
        
        X_test_subset = X_test[:, self.selected_features]
        return self.qsvm.predict(X_test_subset)
    
    def predict_proba(self, X_test: np.ndarray) -> np.ndarray:
        """Predict probabilities using QSVM with selected features"""
        if self.qsvm is None:
            raise ValueError("Model not trained. Call fit() first.")
        
        X_test_subset = X_test[:, self.selected_features]
        return self.qsvm.predict_proba(X_test_subset)


# Example usage and testing
if __name__ == "__main__":
    print("=" * 70)
    print("QSVM Classifier - DBS Fraud Detection Challenge")
    print("=" * 70)
    
    if not QISKIT_AVAILABLE:
        print("\n❌ Qiskit not available. Please install:")
        print("pip install qiskit qiskit-aer qiskit-machine-learning")
    else:
        # Create synthetic fraud data for testing
        np.random.seed(42)
        n_samples = 100
        n_features = 4
        
        # Generate synthetic data
        X_train = np.random.randn(n_samples, n_features)
        y_train = (X_train[:, 0] + X_train[:, 1] > 0).astype(int)
        
        X_test = np.random.randn(20, n_features)
        y_test = (X_test[:, 0] + X_test[:, 1] > 0).astype(int)
        
        print(f"\n📊 Test Data: {n_samples} training samples, {len(X_test)} test samples")
        print(f"   Features: {n_features}, Fraud rate: {y_train.mean():.2%}")
        
        # Test QSVM
        print("\n🔬 Testing QSVM...")
        qsvm = QSVM(n_features=n_features, reps=2)
        qsvm.fit(X_train, y_train)
        
        accuracy = qsvm.score(X_test, y_test)
        print(f"\n✓ QSVM Accuracy: {accuracy:.4f}")
        
        print("\n" + "=" * 70)
        print("✓ QSVM implementation ready for challenge!")
        print("=" * 70)
