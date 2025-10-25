# How to Add Your Solver to QCentroid

## 🎯 Overview

Your quantum fraud detection solver is ready to run on QCentroid! This guide explains how to deploy it as a solver on the QCentroid platform.

## 📋 Prerequisites

- ✅ QCentroid account with team credentials
- ✅ GitHub repository with your code (already done!)
- ✅ Dataset prepared in `data/processed/` (already done!)
- ✅ Clean, optimized codebase (already done!)

## 🚀 Method 1: Git Clone (Recommended - Simplest)

This is the **easiest** method since your code is already on GitHub!

### Step 1: Access QCentroid IDE

1. Open browser and go to: **https://ide.qcentroid.xyz**
2. Login with:
   - Email: `c2_team9_singapore@qai-ventures.com`
   - Organization: `GenQ - Singapore 2025`

### Step 2: Clone Your Repository

In the QCentroid terminal, run:

```bash
# Navigate to your workspace
cd ~/work/git

# Clone the repository (if not already cloned)
git clone https://github.com/sanjey99/quantum_hackathon.git

# Enter the directory
cd quantum_hackathon

# Make sure you're on the main branch
git checkout main
git pull origin main
```

### Step 3: Set Up Environment

```bash
# Create .env file with your credentials
cat > .env << 'EOF'
QCENTROID_EMAIL=c2_team9_singapore@qai-ventures.com
QCENTROID_ORG=GenQ - Singapore 2025
QCENTROID_URL=https://api.qcentroid.xyz
EOF

# Install dependencies
pip install -r requirements.txt
```

### Step 4: Prepare Data Files

Since the large `.npy` files are not in Git (they exceed 100MB), you need to generate them:

```bash
# Run the data preparation script
python model/load_kaggle_data.py
```

This will:
- Download the Kaggle dataset (if not present)
- Process and scale features
- Create the `.npy` files in `data/processed/`
- Save feature names

### Step 5: Run Your Solver!

```bash
# Run the quantum solver
python main.py
```

**Expected Output:**
```
================================================================================
   QUANTUM FRAUD DETECTION SOLVER
================================================================================

📊 Loading Dataset...
   ✓ Training samples: 227,845
   ✓ Testing samples: 56,962
   ✓ Features: 30

🔬 Initializing Quantum Backend...
   ✓ Connected to QCentroid
   ✓ Backend: ibmq_qasm_simulator (or real hardware)

⚛️  Training QSVM with Quantum Kernels...
   ✓ Feature map: ZZFeatureMap
   ✓ Training quantum kernel matrix...
   [Progress bar...]

📈 Evaluating Model...
   ✓ Accuracy: 0.XX
   ✓ Precision: 0.XX
   ✓ Recall: 0.XX
   ✓ F1-Score: 0.XX

✅ Results saved to: results/
```

---

## 🗂️ Method 2: Manual Upload (Alternative)

If Git clone doesn't work, you can manually upload files.

### What Files to Upload

**Essential Core Files:**
```
quantum_hackathon/
├── main.py                          ← Entry point
├── quantum_solver.py                ← Main solver logic
├── requirements.txt                 ← Dependencies
├── .env                             ← Credentials (create this)
├── model/
│   ├── __init__.py
│   ├── qsvm_classifier.py          ← QSVM implementation
│   ├── qcentroid_config.py         ← QCentroid connection
│   ├── evaluation_metrics.py       ← Metrics
│   └── load_kaggle_data.py         ← Data loading
└── data/
    ├── raw/
    │   └── creditcard.csv           ← Kaggle dataset
    └── processed/
        └── (will be generated)
```

### Upload Steps

1. **In QCentroid IDE:**
   - Create folder: `mkdir -p ~/work/git/quantum_hackathon`
   - Use the **Upload** button to upload files

2. **Upload in this order:**
   ```bash
   # First, upload these files:
   main.py
   quantum_solver.py
   requirements.txt
   
   # Then upload the model/ folder with all Python files
   model/__init__.py
   model/qsvm_classifier.py
   model/qcentroid_config.py
   model/evaluation_metrics.py
   model/load_kaggle_data.py
   ```

3. **Create .env file:**
   ```bash
   cd ~/work/git/quantum_hackathon
   nano .env
   ```
   
   Add:
   ```
   QCENTROID_EMAIL=c2_team9_singapore@qai-ventures.com
   QCENTROID_ORG=GenQ - Singapore 2025
   QCENTROID_URL=https://api.qcentroid.xyz
   ```
   
   Save with `Ctrl+O`, `Enter`, `Ctrl+X`

4. **Upload dataset:**
   ```bash
   # Create data directory
   mkdir -p ~/work/git/quantum_hackathon/data/raw
   
   # Upload creditcard.csv to data/raw/
   ```

5. **Install and Run:**
   ```bash
   cd ~/work/git/quantum_hackathon
   pip install -r requirements.txt
   python model/load_kaggle_data.py  # Generate processed data
   python main.py                      # Run solver!
   ```

---

## 📦 Method 3: ZIP Package Upload

### Create ZIP Package Locally

```powershell
# On your Windows machine
cd C:\Users\sanje\Documents\GitHub\quantum_hackathon

# Create a deployment package (excluding large files)
Compress-Archive -Path main.py,quantum_solver.py,requirements.txt,model,docs,README.md,.env.example -DestinationPath qcentroid_solver.zip
```

### Upload to QCentroid

1. In QCentroid IDE, navigate to: `~/work/git/`
2. Click **Upload** button
3. Select `qcentroid_solver.zip`
4. In terminal:
   ```bash
   cd ~/work/git
   unzip qcentroid_solver.zip -d quantum_hackathon
   cd quantum_hackathon
   
   # Create .env with credentials
   cp .env.example .env
   nano .env  # Add your credentials
   
   # Install and prepare data
   pip install -r requirements.txt
   python model/load_kaggle_data.py
   
   # Run!
   python main.py
   ```

---

## 🔧 Troubleshooting

### Issue: "No module named 'qiskit'"

**Solution:**
```bash
pip install qiskit qiskit-aer qiskit-ibm-runtime
```

### Issue: "Cannot connect to QCentroid backend"

**Solution:**
1. Check your `.env` file has correct credentials
2. Verify you're logged into QCentroid platform
3. Check network connectivity

```bash
# Test connection
python -c "from model.qcentroid_config import get_quantum_backend; backend = get_quantum_backend(); print(backend)"
```

### Issue: "Dataset not found"

**Solution:**
```bash
# Download dataset manually
cd ~/work/git/quantum_hackathon/data/raw
wget https://storage.googleapis.com/kaggle-data-sets/310/684/creditcard.csv

# Or run data preparation
cd ~/work/git/quantum_hackathon
python model/load_kaggle_data.py
```

### Issue: "Memory error during training"

**Solution:**
The solver automatically uses a subset of data for quantum training. If you still get memory errors:

1. Edit `quantum_solver.py`
2. Reduce sample size:
   ```python
   # Line ~150
   n_train_samples = 100  # Reduce from 500
   n_test_samples = 50    # Reduce from 200
   ```

---

## 📊 Expected Runtime

| Operation | Time |
|-----------|------|
| Data loading | 30 seconds |
| Quantum backend setup | 1 minute |
| QSVM training (500 samples) | 10-20 minutes |
| Testing | 2-5 minutes |
| **Total** | **15-30 minutes** |

---

## ✅ Verification

After running, you should see:

1. **Results folder created:**
   ```
   results/
   ├── predictions.csv         ← Model predictions
   ├── evaluation_metrics.txt  ← Performance metrics
   └── quantum_features.npy    ← Quantum features
   ```

2. **Console output showing:**
   - Dataset loaded successfully
   - Quantum backend connected
   - Training progress
   - Final metrics (accuracy, precision, recall, F1)

3. **Proof of quantum computing:**
   - Backend name shown (e.g., `ibmq_qasm_simulator` or real hardware)
   - Quantum circuit execution logs
   - Quantum kernel matrix computation

---

## 🎯 Quick Commands Reference

```bash
# Clone and setup (first time)
cd ~/work/git
git clone https://github.com/sanjey99/quantum_hackathon.git
cd quantum_hackathon
git checkout main
pip install -r requirements.txt

# Run solver
python main.py

# Update code (if you made changes on GitHub)
git pull origin main
python main.py

# Test components individually
python test_quantum_solver.py

# Re-generate data if needed
python model/load_kaggle_data.py
```

---

## 📝 Next Steps

Once your solver runs successfully on QCentroid:

1. **Capture Results:**
   - Screenshot the console output
   - Download `results/` folder
   - Note execution time and metrics

2. **Document for Submission:**
   - Quantum backend used
   - Number of qubits utilized
   - Training time on quantum hardware
   - Final performance metrics

3. **Optimize (Optional):**
   - Adjust feature selection
   - Try different quantum feature maps
   - Experiment with different sample sizes
   - Compare simulator vs real hardware results

---

## 🆘 Support

If you encounter issues:

1. Check the `DEPLOYMENT_GUIDE.md` for detailed explanations
2. Review `QUANTUM_SOLVER_README.md` for solver internals
3. Run `python test_quantum_solver.py` to diagnose issues
4. Check QCentroid documentation: https://docs.qcentroid.xyz

---

**Your solver is production-ready and optimized for QCentroid! 🚀**
