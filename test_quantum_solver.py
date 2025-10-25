#!/usr/bin/env python3
"""
Quick test of quantum solver components
Verifies all imports and basic functionality
"""

import sys
from pathlib import Path

print("=" * 70)
print("QUANTUM SOLVER - QUICK TEST")
print("=" * 70)
print()

# Test 1: Basic imports
print("[1/5] Testing basic imports...")
try:
    import numpy as np
    import sklearn
    print("✓ NumPy and scikit-learn imported")
except ImportError as e:
    print(f"✗ Error: {e}")
    sys.exit(1)

# Test 2: Qiskit imports
print("\n[2/5] Testing Qiskit imports...")
try:
    import qiskit
    print(f"✓ Qiskit version: {qiskit.__version__}")
    
    # Try importing quantum components
    try:
        from qiskit import QuantumCircuit
    except ImportError:
        from qiskit.circuit import QuantumCircuit
    print("✓ QuantumCircuit imported")
    
    from qiskit.circuit.library import ZZFeatureMap
    print("✓ ZZFeatureMap imported")
    
    try:
        from qiskit_aer import AerSimulator
    except ImportError:
        from qiskit.providers.aer import AerSimulator
    print("✓ AerSimulator imported")
    
    from qiskit_machine_learning.kernels import FidelityQuantumKernel
    print("✓ FidelityQuantumKernel imported")
    
except ImportError as e:
    print(f"✗ Qiskit import error: {e}")
    print("  Install with: pip install qiskit qiskit-aer qiskit-machine-learning")
    sys.exit(1)

# Test 3: Model imports
print("\n[3/5] Testing model imports...")
try:
    sys.path.insert(0, str(Path(__file__).parent / 'model'))
    
    from model.qsvm_classifier import QSVM
    print("✓ QSVM class imported")
    
    from model.qcentroid_config import get_qcentroid_client
    print("✓ QCentroid config imported")
    
    from model.evaluation_metrics import FraudDetectionMetrics
    print("✓ Evaluation metrics imported")
    
except ImportError as e:
    print(f"✗ Model import error: {e}")
    sys.exit(1)

# Test 4: Create small quantum circuit
print("\n[4/5] Testing quantum circuit creation...")
try:
    # Create a simple 2-qubit circuit
    feature_map = ZZFeatureMap(feature_dimension=2, reps=1)
    print(f"✓ Created ZZ-FeatureMap: {feature_map.num_qubits} qubits")
    
    # Try to bind parameters (handle both Qiskit 0.x and 1.x)
    params = [0.5, 0.3]
    try:
        circuit = feature_map.assign_parameters(params)  # Qiskit 1.x
    except (AttributeError, TypeError):
        circuit = feature_map.bind_parameters(params)  # Qiskit 0.x
    
    print(f"✓ Bound parameters, circuit depth: {circuit.depth()}")
    
except Exception as e:
    print(f"✗ Circuit creation error: {e}")
    sys.exit(1)

# Test 5: Test QSVM instantiation
print("\n[5/5] Testing QSVM instantiation...")
try:
    qsvm = QSVM(n_features=4, reps=1, C=1.0)
    print("✓ QSVM instance created successfully")
    print(f"  - Features: {qsvm.n_features}")
    print(f"  - Regularization: {qsvm.C}")
    
except Exception as e:
    print(f"✗ QSVM instantiation error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 6: Optional - Test QCentroid connection
print("\n[Optional] Testing QCentroid connection...")
try:
    from dotenv import load_dotenv
    load_dotenv()
    
    client = get_qcentroid_client()
    backend_info = client.get_backend_info()
    
    print("✓ Connected to QCentroid!")
    print(f"  - Backend: {backend_info.get('backend', 'N/A')}")
    print(f"  - Type: {backend_info.get('type', 'N/A')}")
    print(f"  - Available: {backend_info.get('available', 'N/A')}")
    
except Exception as e:
    print(f"⚠️  QCentroid connection failed (this is OK for testing): {e}")
    print("   Set up .env file with credentials for quantum hardware access")

# Summary
print("\n" + "=" * 70)
print("✅ ALL CORE TESTS PASSED!")
print("=" * 70)
print()
print("The quantum solver is ready to run!")
print("Execute with: python quantum_solver.py")
print()
