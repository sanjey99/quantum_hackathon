# QCentroid Integration Guide

This guide explains how to integrate your fraud detection project with QCentroid's online IDE and quantum execution platform.

## What is QCentroid?

QCentroid is a quantum computing platform that provides:
- Online IDE for quantum algorithm development
- Quantum circuit simulators
- Access to real quantum hardware (if available)
- Python SDK for quantum computing

## Prerequisites

### 1. QCentroid Account Setup
1. Visit the QCentroid platform website
2. Create an account or sign in
3. Obtain your API credentials/access token
4. Note your workspace/project ID

### 2. Install QCentroid Python SDK

Update your `requirements.txt` to include the QCentroid SDK:

```bash
# Quantum Computing
qcentroid>=1.0.0  # QCentroid Python SDK
qiskit>=0.43.0    # Optional: IBM Quantum framework (often compatible)
cirq>=1.0.0       # Optional: Google Quantum framework
pennylane>=0.30.0 # Optional: Quantum ML framework
```

Install the dependencies:
```bash
pip install qcentroid
# Or if QCentroid is not yet on PyPI:
pip install qcentroid --extra-index-url https://qcentroid.example.com/pypi/
```

## Project Configuration

### 1. Environment Variables

Create a `.env` file in your project root (already in `.gitignore`):

```bash
# QCentroid Configuration
QCENTROID_API_KEY=your_api_key_here
QCENTROID_WORKSPACE_ID=your_workspace_id
QCENTROID_BACKEND=simulator  # or 'hardware' for real quantum computer
QCENTROID_API_URL=https://api.qcentroid.com/v1

# Python Configuration
PYTHON_ENV=production
```

### 2. Install Additional Quantum Dependencies

```bash
pip install python-dotenv  # For loading .env files
pip install qiskit-aer     # Quantum simulator backend
pip install matplotlib     # For quantum circuit visualization
```

### 3. Update requirements.txt

Add these to your `requirements.txt`:

```python
# Quantum Computing & QCentroid
qcentroid>=1.0.0
qiskit>=0.43.0
qiskit-aer>=0.12.0
pennylane>=0.30.0
python-dotenv>=1.0.0

# Additional ML for Quantum
scikit-optimize>=0.9.0  # For hyperparameter optimization
scipy>=1.10.0           # Scientific computing
```

## Integration Steps

### 1. Configure QCentroid Client

Create `model/qcentroid_config.py`:

```python
import os
from dotenv import load_dotenv
import qcentroid as qc

# Load environment variables
load_dotenv()

class QCentroidClient:
    def __init__(self):
        self.api_key = os.getenv('QCENTROID_API_KEY')
        self.workspace_id = os.getenv('QCENTROID_WORKSPACE_ID')
        self.backend = os.getenv('QCENTROID_BACKEND', 'simulator')
        
        if not self.api_key:
            raise ValueError("QCENTROID_API_KEY not found in environment")
        
        # Initialize QCentroid connection
        self.client = qc.Client(
            api_key=self.api_key,
            workspace_id=self.workspace_id
        )
        
    def get_backend(self):
        """Get quantum backend (simulator or hardware)"""
        return self.client.get_backend(self.backend)
    
    def submit_circuit(self, circuit):
        """Submit quantum circuit for execution"""
        job = self.client.execute(circuit, backend=self.backend)
        return job
    
    def get_results(self, job_id):
        """Retrieve results from completed job"""
        return self.client.get_job_results(job_id)

# Global client instance
qcentroid_client = QCentroidClient()
```

### 2. Update Fraud Model to Use QCentroid

Modify `model/fraud_model_development.py` to use the QCentroid client:

```python
from qcentroid_config import qcentroid_client

def create_quantum_classifier(n_qubits):
    """Create a quantum classifier circuit using QCentroid"""
    backend = qcentroid_client.get_backend()
    circuit = qc.QuantumCircuit(n_qubits, backend=backend)
    
    # Your quantum circuit logic here
    # ...
    
    return circuit

class QuantumFraudDetector:
    def __init__(self, n_features, use_cloud=True):
        self.n_features = n_features
        self.n_qubits = min(n_features, 10)  # Limit qubits based on hardware
        self.use_cloud = use_cloud
        
        if use_cloud:
            self.circuit = create_quantum_classifier(self.n_qubits)
        else:
            # Use local simulator
            self.circuit = qc.QuantumCircuit(self.n_qubits)
```

### 3. Using QCentroid Online IDE

#### Option A: Upload Project to QCentroid IDE
1. Log in to QCentroid IDE
2. Create a new project or workspace
3. Upload your Python files:
   - `model/fraud_model_development.py`
   - `model/fraud_data_analysis.py`
   - `model/predict.py`
4. Upload your data files to QCentroid storage
5. Run notebooks directly in the QCentroid IDE

#### Option B: Connect Local Environment to QCentroid Cloud
1. Keep your development environment local
2. Use QCentroid SDK to submit jobs to cloud
3. Results are fetched back to your local environment

```python
# Example: Submit job to QCentroid cloud
job = qcentroid_client.submit_circuit(quantum_circuit)
print(f"Job submitted: {job.id}")

# Wait for completion
job.wait_for_completion()

# Get results
results = qcentroid_client.get_results(job.id)
print(f"Quantum results: {results}")
```

## Running Quantum Experiments

### 1. Local Testing (Simulator)
```bash
# Activate your environment
.\venv-new\Scripts\activate

# Set to use simulator
$env:QCENTROID_BACKEND="simulator"

# Run your model
python model/fraud_model_development.py
```

### 2. Cloud Execution (Real Quantum Hardware)
```bash
# Set to use quantum hardware
$env:QCENTROID_BACKEND="hardware"
$env:QCENTROID_API_KEY="your_api_key"

# Run your model (will submit to QCentroid cloud)
python model/fraud_model_development.py
```

### 3. Hybrid Approach
```python
# Use classical ML for preprocessing
# Use quantum computing for specific operations

from sklearn.ensemble import RandomForestClassifier
from qcentroid_config import qcentroid_client

# Classical preprocessing
classical_model = RandomForestClassifier()
classical_features = classical_model.fit_transform(X_train, y_train)

# Quantum enhancement
quantum_model = QuantumFraudDetector(n_features=classical_features.shape[1])
quantum_results = quantum_model.predict(classical_features)

# Combine results
final_predictions = combine_classical_quantum(classical_pred, quantum_results)
```

## QCentroid-Specific Features

### 1. Quantum Circuit Visualization
```python
import qcentroid as qc

circuit = qc.QuantumCircuit(4)
# Build your circuit...

# Visualize in QCentroid IDE
circuit.draw(output='qcentroid')

# Or save as image
circuit.draw(output='mpl', filename='circuit.png')
```

### 2. Job Monitoring
```python
# Submit job
job = qcentroid_client.submit_circuit(circuit)

# Monitor status
while not job.is_complete():
    print(f"Status: {job.status()}")
    time.sleep(5)

# Get results when done
results = job.results()
```

### 3. Resource Management
```python
# Check available quantum resources
resources = qcentroid_client.client.get_available_resources()
print(f"Available backends: {resources.backends}")
print(f"Queue size: {resources.queue_size}")
print(f"Estimated wait time: {resources.estimated_wait}")
```

## Troubleshooting

### Common Issues

1. **"qcentroid module not found"**
   - Install the SDK: `pip install qcentroid`
   - Check if it requires special installation from QCentroid's repository

2. **"Authentication failed"**
   - Verify your API key in `.env`
   - Check if your account has access to quantum resources
   - Ensure your subscription/credits are active

3. **"Backend not available"**
   - Try using 'simulator' backend first
   - Check QCentroid status page for hardware availability
   - Verify your account has hardware access permissions

4. **"Circuit too large"**
   - Reduce number of qubits (n_qubits parameter)
   - Optimize your quantum circuit
   - Consider breaking into smaller sub-circuits

### Getting Help

- QCentroid Documentation: https://docs.qcentroid.com
- Support: support@qcentroid.com
- Community Forum: https://forum.qcentroid.com
- GitHub Issues: https://github.com/qcentroid/python-sdk/issues

## Best Practices

1. **Start with Simulators**: Test your quantum circuits on simulators before using real hardware
2. **Optimize Circuits**: Minimize gate count and circuit depth
3. **Handle Errors**: Quantum operations can fail; implement retry logic
4. **Monitor Costs**: Real quantum hardware may have usage costs
5. **Version Control**: Don't commit API keys; use `.env` files
6. **Batch Processing**: Submit multiple jobs at once when possible
7. **Result Caching**: Cache quantum results to avoid re-computation

## Example: Complete Workflow

```python
#!/usr/bin/env python3
import numpy as np
from dotenv import load_dotenv
from qcentroid_config import qcentroid_client
import qcentroid as qc

# Load environment
load_dotenv()

# Load your data
X_train = np.load('data/processed/X_train_scaled.npy')
y_train = np.load('data/processed/y_train_resampled.npy')

# Create quantum model
quantum_model = QuantumFraudDetector(
    n_features=X_train.shape[1],
    use_cloud=True
)

# Train (will use QCentroid backend)
print("Training quantum model on QCentroid...")
quantum_model.train(X_train, y_train)

# Make predictions
predictions = quantum_model.predict(X_test)

# Save results
np.save('results/quantum_predictions.npy', predictions)
print("Quantum predictions saved!")
```

## Next Steps

1. ✅ Set up QCentroid account
2. ✅ Install QCentroid SDK and dependencies
3. ✅ Configure environment variables
4. ✅ Test with simulator backend
5. ✅ Optimize quantum circuits
6. ✅ Submit to real quantum hardware
7. ✅ Integrate with Java service via REST API

For more information, refer to the QCentroid documentation and API reference.
