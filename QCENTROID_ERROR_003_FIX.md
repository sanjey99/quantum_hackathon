# QCentroid Execution Error 003 - Solution

## 🔴 Error: Execution internal error 003

**Status:** Execution started but failed immediately

**Log Analysis:**
```
2025-10-25 09:06:44,193 - INFO - STARTING EXECUTION
2025-10-25 09:06:44,807 - INFO - Execution input data (first 100 chars): {'dataset_info': {'name': 'Credit Card Fraud Detection'...
2025-10-25 09:06:44,807 - INFO - Execution solver params (first 100 chars): {}
2025-10-25 09:06:44,808 - INFO - Execution additional arguments (first 100 chars): {'dataset': 'kaggle_credit_card_fraud', 'random_state': 42...
2025-10-25 09:06:44,966 - INFO - Error: Execution internal error 003.
```

---

## 🔍 Problem Identified

1. ✅ Execution **started** - Your solver is being called
2. ✅ Input data is being passed (dataset JSON)
3. ❌ **Fails within 1 second** with "internal error 003"
4. ⚠️ **Only Microsoft provider available** on QCentroid

---

## 🎯 Root Cause

**QCentroid is passing your dataset JSON as input**, but your solver expects to:
1. Load data from local files (`data/processed/*.npy`)
2. Connect to quantum backend
3. Train QSVM

**The mismatch causes immediate failure.**

---

## ✅ Solution: Update Your Solver for QCentroid Input Format

QCentroid is providing the dataset JSON as input. You need to modify your solver to accept this format.

### **Step 1: Create a new entry point for QCentroid**

Create a new file: `qcentroid_main.py`

```python
"""
QCentroid-compatible entry point for DBS Fraud Detection QSVM
Accepts input data from QCentroid platform
"""
import json
import sys
import numpy as np
from pathlib import Path

def main():
    try:
        print("="*80)
        print("   DBS FRAUD DETECTION - QSVM SOLVER")
        print("   Running on QCentroid Platform")
        print("="*80)
        print()
        
        # QCentroid provides input data via stdin or as arguments
        # Try to read from stdin first
        import sys
        if not sys.stdin.isatty():
            input_data = json.load(sys.stdin)
            print("✓ Received input data from stdin")
        else:
            # Fallback: use local data
            print("⚠ No stdin data, using local dataset")
            from quantum_solver import main as run_quantum_solver
            return run_quantum_solver()
        
        # Extract configuration from input
        additional_args = input_data.get('additional_arguments', {})
        dataset_info = input_data.get('dataset_info', {})
        
        print(f"✓ Dataset: {dataset_info.get('name', 'Credit Card Fraud')}")
        print(f"✓ Random state: {additional_args.get('random_state', 42)}")
        print()
        
        # Check if processed data exists locally
        data_path = Path('data/processed')
        if not data_path.exists() or not list(data_path.glob('*.npy')):
            print("⚠ Processed data not found locally")
            print("✓ Preparing to download and process dataset...")
            
            # Download and process data
            from model.load_kaggle_data import main as load_data
            print("✓ Running data preparation...")
            load_data()
            print("✓ Data preparation complete")
            print()
        else:
            print("✓ Using existing processed data")
            print()
        
        # Now run the quantum solver
        print("="*80)
        print("   STARTING QUANTUM SOLVER")
        print("="*80)
        print()
        
        from quantum_solver import main as run_quantum_solver
        result = run_quantum_solver()
        
        # Format output for QCentroid
        output = {
            "status": "success",
            "solver": "DBS Fraud Detection QSVM",
            "result": result,
            "additional_info": {
                "random_state": additional_args.get('random_state', 42),
                "save_results": additional_args.get('save_results', True)
            }
        }
        
        # Return output as JSON
        print()
        print("="*80)
        print("   EXECUTION COMPLETE")
        print("="*80)
        print(json.dumps(output, indent=2))
        
        return 0
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        
        # Return error output
        error_output = {
            "status": "error",
            "error": str(e),
            "traceback": traceback.format_exc()
        }
        print(json.dumps(error_output, indent=2))
        return 1

if __name__ == '__main__':
    sys.exit(main())
```

### **Step 2: Update your solver registration**

Go back to QCentroid and update:

**Entry point / Main file:**
```
qcentroid_main.py
```

**Command to run:**
```
python qcentroid_main.py
```

---

## 🔧 Alternative: Fix Microsoft Azure Connection

Since **only Microsoft provider is available**, you need Azure Quantum credentials.

### **Option A: Contact QCentroid Support**

**Email them:**
```
Subject: Microsoft Azure Quantum Connection Required - Team 9

Hello,

We're Team 9 (c2_team9_singapore@qai-ventures.com) from GenQ - Singapore 2025.

Our solver requires quantum backend but only Microsoft provider is available.
We're getting "Execution internal error 003" because Azure connection string 
is invalid.

Could you please:
1. Provide valid Azure Quantum credentials for our team, OR
2. Enable QCentroid native provider for IonQ access, OR
3. Configure the Microsoft provider with valid Azure credentials

Solver: dbs-fraud-qsvm-classifier
Error: Execution internal error 003

Thank you!
```

### **Option B: Add Azure Configuration to Your Code**

If QCentroid expects you to provide Azure credentials, modify `model/qcentroid_config.py`:

```python
import os
from qiskit_ibm_runtime import QiskitRuntimeService

def get_quantum_backend():
    """Get quantum backend for QCentroid execution"""
    
    # Try QCentroid environment variables first
    qcentroid_url = os.getenv('QCENTROID_URL')
    qcentroid_token = os.getenv('QCENTROID_TOKEN')
    
    if qcentroid_url and qcentroid_token:
        # QCentroid native connection
        print(f"✓ Connecting to QCentroid: {qcentroid_url}")
        # Your existing QCentroid connection code
        pass
    else:
        # Fallback: Try Azure Quantum
        try:
            from azure.quantum import Workspace
            
            # Check if Azure credentials are in environment
            resource_id = os.getenv('AZURE_QUANTUM_RESOURCE_ID')
            location = os.getenv('AZURE_QUANTUM_LOCATION', 'eastus')
            
            if resource_id:
                print(f"✓ Using Azure Quantum: {location}")
                workspace = Workspace(
                    resource_id=resource_id,
                    location=location
                )
                
                # Get IonQ target
                ionq_target = workspace.get_targets("ionq.simulator")
                return ionq_target
            else:
                print("⚠ No quantum backend credentials found")
                print("Using local simulator...")
                from qiskit_aer import AerSimulator
                return AerSimulator()
                
        except ImportError:
            print("⚠ Azure Quantum not available, using local simulator")
            from qiskit_aer import AerSimulator
            return AerSimulator()
```

---

## 📝 Quick Fix Checklist

Try these in order:

### **Fix 1: Update Entry Point** ⭐ RECOMMENDED
1. Create `qcentroid_main.py` (code above)
2. Push to GitHub: `git add qcentroid_main.py && git commit -m "Add QCentroid entry point" && git push`
3. Update solver registration: Entry point = `qcentroid_main.py`
4. Retry job

### **Fix 2: Ensure Data is Available**
1. Make sure `data/processed/` directory exists in your repo
2. Add a `.gitkeep` file to keep the directory
3. Update `qcentroid_main.py` to download data if missing

### **Fix 3: Contact Support**
1. Use the email template above
2. Request valid Azure credentials or QCentroid native access
3. Wait for response

### **Fix 4: Test Locally First**
```bash
# On your machine, test the QCentroid input format
echo '{"dataset_info": {"name": "test"}, "additional_arguments": {"random_state": 42}}' | python qcentroid_main.py
```

---

## 🎯 What "Error 003" Likely Means

Based on the timing (< 1 second failure):

1. **Missing dependency**: Required package not installed
2. **Import error**: Can't import quantum_solver or dependencies
3. **File not found**: Can't find data files
4. **Configuration error**: Missing environment variables
5. **Azure connection**: Can't connect to Azure Quantum (most likely)

---

## ✅ Recommended Action Plan

**Immediate steps:**

1. **Create `qcentroid_main.py`** with the code above
2. **Test locally**: `python qcentroid_main.py`
3. **Commit and push**: 
   ```bash
   git add qcentroid_main.py
   git commit -m "Add QCentroid-compatible entry point"
   git push origin main
   ```
4. **Update solver registration**:
   - Entry point: `qcentroid_main.py`
5. **Retry the job**

6. **If still fails**: Contact QCentroid support with the email template

---

## 📊 Expected Behavior After Fix

```
✓ STARTING EXECUTION
✓ Received input data from stdin
✓ Dataset: Credit Card Fraud Detection
✓ Random state: 42
✓ Using existing processed data (or downloading)
✓ STARTING QUANTUM SOLVER
✓ Loading dataset...
✓ Connecting to quantum backend...
✓ Training QSVM...
✓ Evaluating model...
✓ EXECUTION COMPLETE
```

---

## 🆘 Still Not Working?

Share these logs with QCentroid support:
- Full execution log
- Error 003 details
- Your solver configuration
- This troubleshooting document

**The issue is likely either:**
1. Missing entry point adaptation for QCentroid input format
2. Azure Quantum credentials not configured

Both are fixable! 🚀
