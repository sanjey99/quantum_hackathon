# QCentroid Solver Registration Form - Answers

Use these answers to register your solver on the QCentroid platform.

---

## 📋 Form Fields & Answers

### **SDK** *
```
Qiskit
```
**Explanation:** Your solver uses Qiskit (IBM's quantum computing SDK) for quantum circuit creation, QSVM implementation, and quantum kernel computation.

---

### **Provider** *
```
QCentroid
```
**Explanation:** The solver runs on QCentroid's quantum hardware infrastructure, which provides access to IBM quantum computers and simulators.

---

### **Solver name** *
```
DBS Fraud Detection QSVM
```
**Explanation:** This is the readable display name. Uses capital letters and spaces as allowed.

**Alternative names (if you prefer):**
- `Quantum Fraud Detection Solver`
- `Credit Card Fraud QSVM Detector`
- `DBS Quantum Fraud Classifier`

---

### **Description** *
```
Quantum Support Vector Machine (QSVM) for credit card fraud detection using real quantum computing. This solver processes transaction data from the Kaggle Credit Card Fraud dataset, applies quantum feature selection, and trains a QSVM classifier with quantum kernels on QCentroid hardware. Uses ZZFeatureMap for quantum state encoding and implements quantum kernel estimation. Detects fraudulent transactions by leveraging quantum computing's ability to explore high-dimensional feature spaces. Returns fraud predictions with accuracy, precision, recall, and F1-score metrics. Processes 500 training samples and 200 test samples per execution, with quantum circuit execution on IBM quantum backends.
```
**Character count:** 670/1000 ✅

**Shorter alternative (if needed):**
```
Quantum SVM for fraud detection using Qiskit on QCentroid hardware. Trains on Kaggle credit card fraud data with quantum kernels and ZZFeatureMap encoding. Detects fraudulent transactions using quantum computing to explore high-dimensional feature spaces. Returns predictions with performance metrics (accuracy, precision, recall, F1-score). Executes quantum circuits on IBM backends via QCentroid platform.
```
**Character count:** 396/1000 ✅

---

### **Solver URN** *
```
dbs-fraud-qsvm-classifier
```
**Explanation:** Unique identifier without spaces or special characters. This will be used in API calls.

**Alternative URNs (if first is taken):**
- `quantum-fraud-detection-qsvm`
- `qsvm-fraud-detector-dbs`
- `fraud-qsvm-team9-singapore`
- `creditcard-fraud-qsvm`

---

### **Type of solver** *
```
Quantum: Quantum circuit
```
**Explanation:** Your solver uses Qiskit to create and execute quantum circuits for QSVM with quantum kernels. It builds quantum circuits using ZZFeatureMap and executes them on quantum hardware.

**Why this is the correct choice:**
- ✅ You create quantum circuits with Qiskit
- ✅ You execute these circuits on QCentroid quantum backends
- ✅ QSVM uses quantum circuits for kernel estimation
- ✅ Not purely analog, annealing, or tensor network based

**Alternative if needed:**
- `Hybrid: Hybrid quantum circuit` (if you consider the classical SVM training as hybrid)
- `Quantum inspired: Quantum circuit simulation` (only if running on simulator, not real hardware)

---

### **Estimated cost** *
```
50
```
**Explanation:** Cost in credits per execution. This is an estimate for:
- Quantum circuit execution (~500 quantum kernel computations)
- Training QSVM on 500 samples
- Testing on 200 samples
- Approximate runtime: 15-30 minutes

**Cost reasoning:**
- Quantum kernel matrix computation requires significant quantum resources
- Multiple quantum circuit executions (one per training pair)
- Consider adjusting after first run based on actual consumption

**Alternative costs:**
- `25` credits (if 50 seems high)
- `100` credits (if quantum hardware is heavily used)
- `75` credits (mid-range estimate)

---

### **Branch/tag** *
```
main
```
**Explanation:** Your cleaned, optimized code is now on the `main` branch after the recent merge.

**Alternative (if you want to keep development separate):**
- `production` (create this branch for stable releases)
- `v1.0` (create a version tag)
- `sanjey_challenge_demo_fix` (if you want to use your dev branch)

---

### **Programming language** *
```
Python
```
**Explanation:** Your entire solver is written in Python 3.

---

### **Repository name** *
```
quantum_hackathon
```
**Explanation:** Your GitHub repository name in lowercase with underscore. Only lowercase letters, hyphens (-), and underscores (_) are allowed.

**Alternative names (if you want to create a new repo):**
- `quantum-hackathon` (with hyphen)
- `dbs-fraud-qsvm`
- `fraud-detection-quantum`
- `qsvm-fraud-detector`

---

### **Git repository SSH URL** *
```
git@github.com:sanjey99/quantum_hackathon.git
```
**Explanation:** The SSH URL for your GitHub repository. QCentroid will use this to clone your code.

**Alternative formats if needed:**
- HTTPS URL: `https://github.com/sanjey99/quantum_hackathon.git`
- If using SSH: `git@github.com:sanjey99/quantum_hackathon.git` ✅ (Recommended)

**Note:** Make sure QCentroid has access to your repository:
- If **public repository** → Still need to add deploy key (see below)
- If **private repository** → Must add QCentroid's SSH key or deploy key to your repo

---

## 🔑 Add QCentroid SSH Key to Your Repository

**IMPORTANT:** You must add QCentroid's public SSH key to your GitHub repository for the platform to access your code.

### Step-by-Step Instructions:

1. **Go to your repository on GitHub:**
   ```
   https://github.com/sanjey99/quantum_hackathon
   ```

2. **Navigate to Settings → Deploy keys:**
   ```
   https://github.com/sanjey99/quantum_hackathon/settings/keys
   ```

3. **Click "Add deploy key" button**

4. **Fill in the form:**
   - **Title:** `QCentroid Platform`
   - **Key:** Copy and paste the public key below
   - **Allow write access:** ☑️ Check this box (optional - only if you want to edit solver in QCentroid LaunchPad)

5. **Click "Add key"**

### QCentroid Public SSH Key:

```
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQDhBBLeSMyzP+IL4ndEAN1w2TyAhnnQ7hWBKVoW4AODm4o2MxCgIPruYMu9dzICxkFRu80EOzHrcSRoviaToTD4/j0zpxpPPLVaFanAR2L/qLSq87P1GSLHbvppdHrKHmjOL5lI2l0L0aPTZyuSdYXQjxNPlxc6RV9Jtlf5UQCUiuRpLC66AaexbFFZkinZVjlewX3BTgmYj3TywQ5BC3rXdkeYWDGYQmZWC7xE+xXkDuLMIQrQDU2U6DOb0rLvf8SKstiAr4gkOtXmLaUBAYv8JxbwGcCUB7aj9QWMCnCkCy82x/2HGZ0j1Al3IMW9h1huwBJQyi74Y/IO5KebvzIM7MpVtm6OQRCrbxA5iXx/k/0OjfYEBv82NcrtTFpIPNA9yx77fuJccd3Esy/nOSe7A/09QLcs19Icka1hpwa8ZZU53C1HTQ5t6zgMdnGqsAB6muStjm+1VcE6DEFut5nEDAWnxEuksQopd0SAQrVYPCKCLdBKK2GOe6614yI3pc2BJh+oW/zGqzv2VhTBBg2Jy0wD0T/7lSJ+KuoIfPo5c+QThX7gJ/8uBMb1gUcoFtiHg9E/ndKhMAfyLVNr/ucq/JpQn2DOi+o9qKDuBSNH9MHn31Y3CpaNK1B3OwHJk4DWT2OVhUtKeSbIL5b9GXypy1zHTtwa2vblyYll6PjG0w==
```

### ✅ Verification:

After adding the key, you should see it listed in your repository's deploy keys with:
- **Title:** QCentroid Platform
- **Status:** Active (green checkmark)
- **Access:** Read-only (or Read/Write if you checked the box)

---

## 📝 Repository Requirements

Make sure your repository has these files at the root (already done ✅):

- ✅ `main.py` - Entry point
- ✅ `quantum_solver.py` - Main solver logic  
- ✅ `requirements.txt` - Dependencies
- ✅ `model/qsvm_classifier.py` - QSVM implementation
- ✅ `model/qcentroid_config.py` - QCentroid connection
- ✅ `README.md` - Documentation

---

## 🔧 Additional Configuration (if asked)

### **Entry point / Main file:**
```
main.py
```

### **Command to run:**
```
python main.py
```

### **Required environment variables:**
```
QCENTROID_EMAIL
QCENTROID_ORG
QCENTROID_URL
```
(These are already in your `.env.example`)

### **Dependencies file:**
```
requirements.txt
```

### **Minimum Python version:**
```
3.8
```

### **Recommended Python version:**
```
3.9
```

---

## 🎯 Quick Copy-Paste Version

For easy form filling:

| Field | Answer |
|-------|--------|
| **SDK** | Qiskit |
| **Provider** | QCentroid |
| **Solver name** | DBS Fraud Detection QSVM |
| **Description** | Quantum Support Vector Machine (QSVM) for credit card fraud detection using real quantum computing. This solver processes transaction data from the Kaggle Credit Card Fraud dataset, applies quantum feature selection, and trains a QSVM classifier with quantum kernels on QCentroid hardware. Uses ZZFeatureMap for quantum state encoding and implements quantum kernel estimation. Detects fraudulent transactions by leveraging quantum computing's ability to explore high-dimensional feature spaces. Returns fraud predictions with accuracy, precision, recall, and F1-score metrics. Processes 500 training samples and 200 test samples per execution, with quantum circuit execution on IBM quantum backends. |
| **Solver URN** | dbs-fraud-qsvm-classifier |
| **Type of solver** | Quantum: Quantum circuit |
| **Estimated cost** | 50 |
| **Branch/tag** | main |
| **Programming language** | Python |
| **Repository name** | quantum_hackathon |
| **Git repository SSH URL** | git@github.com:sanjey99/quantum_hackathon.git |

---

## 📍 Repository URL

When asked for repository URL, provide:
```
https://github.com/sanjey99/quantum_hackathon
```

---

## ✅ Pre-Registration Checklist

Before submitting the form, verify:

- [ ] Code is pushed to the `main` branch ✅ (Done!)
- [ ] `requirements.txt` is complete ✅
- [ ] `main.py` exists and is executable ✅
- [ ] `.env.example` shows required variables ✅
- [ ] README.md has clear documentation ✅
- [ ] No large files in repository ✅ (`.npy` files excluded)
- [ ] Repository is public or QCentroid has access ✅
- [ ] **QCentroid SSH key added to GitHub deploy keys** ⚠️ **REQUIRED!**

### How to Add SSH Key:
1. Go to: `https://github.com/sanjey99/quantum_hackathon/settings/keys`
2. Click "Add deploy key"
3. Title: `QCentroid Platform`
4. Paste the SSH key (shown above in this document)
5. Check "Allow write access" (optional)
6. Click "Add key"

---

## 🚀 After Registration

Once registered, QCentroid will:

1. **Clone your repository** from the `main` branch
2. **Install dependencies** from `requirements.txt`
3. **Set environment variables** from your QCentroid account
4. **Execute** `python main.py`
5. **Capture results** and display to users
6. **Charge credits** based on actual usage

Your solver will then be available via:
- QCentroid web interface
- API calls using URN: `dbs-fraud-qsvm-classifier`
- SDK integrations

---

## 🎉 You're Ready!

All your answers are prepared. Just copy and paste them into the QCentroid solver registration form!

**Good luck with your submission! 🚀⚛️**
