# QCentroid Job Configuration - Answers

Use these settings when creating a job to run your DBS Fraud Detection QSVM solver.

---

## 📋 Job Configuration

### **Job title** (Optional)
```
DBS Fraud Detection - Quantum QSVM Execution
```
**Alternative titles:**
- `Credit Card Fraud Detection - QSVM Run`
- `Quantum Fraud Classifier - Production Run`
- `QSVM Fraud Detection Test Run`
- `DBS Challenge - Quantum Solver Execution`

---

### **Job comment** (Optional)
```
Executing quantum QSVM on credit card fraud dataset with 500 training samples and 200 test samples. Uses ZZFeatureMap and quantum kernels on QCentroid hardware. Expected runtime: 15-30 minutes.
```

**Shorter alternative:**
```
Quantum fraud detection using QSVM with quantum kernels. Training on Kaggle credit card fraud dataset.
```

**Leave blank if:** You want a quick test run

---

### **Number of shots**
```
1
```
**Explanation:** One shot = one complete execution of the solver
- **Use 1** for initial testing and development
- **Use 3-5** for production runs to get average performance metrics
- **Use 10+** for statistical validation and research

**Recommendation:** Start with `1` shot to verify everything works, then increase for production.

---

### **Max. execution time in minutes**
```
60
```
**Explanation:** Maximum time allowed before job auto-stops
- Your solver typically runs 15-30 minutes
- Set to **60 minutes** as a safety buffer
- Set to **0** for no time limit (not recommended)

**Alternative values:**
- `30` - Tight deadline, may timeout
- `45` - Reasonable buffer
- `60` - Recommended (2x expected time)
- `90` - Extra safe for slower hardware
- `0` - No limit (may waste credits if stuck)

---

## 🔧 Additional Configuration

### **Additional arguments as a JSON object** (Optional)
```json
{
  "dataset": "kaggle_credit_card_fraud",
  "n_train_samples": 500,
  "n_test_samples": 200,
  "feature_dimension": 10,
  "quantum_backend": "qcentroid",
  "random_state": 42,
  "enable_logging": true,
  "save_results": true
}
```

**Character count:** 246/1000 ✅

**Explanation of parameters:**
- `dataset`: Identifies which dataset is being used
- `n_train_samples`: Number of samples for quantum training (500)
- `n_test_samples`: Number of samples for testing (200)
- `feature_dimension`: Number of features after quantum feature selection (10)
- `quantum_backend`: Specifies QCentroid backend
- `random_state`: Seed for reproducibility (42)
- `enable_logging`: Turn on detailed logging
- `save_results`: Save predictions and metrics to results folder

**Minimal version (if you prefer):**
```json
{
  "n_train_samples": 500,
  "n_test_samples": 200,
  "random_state": 42
}
```

**Leave blank if:** Your solver doesn't need custom parameters (it will use defaults from code)

---

## 🖥️ Hardware Configuration

### **Hardware Resources (CPU & Memory)**

**Recommended for your solver:**
```
CPU: 4 vCPU & Memory: 8 GB
```

**Explanation:** Your QSVM solver processes 500 training samples with quantum kernels
- Quantum kernel computation is memory-intensive
- Classical SVM training needs CPU power
- 4 vCPU provides good parallelization
- 8 GB memory handles dataset and quantum circuit operations

**Available Options:**

| Configuration | Use Case | Cost |
|---------------|----------|------|
| **1 vCPU & 2 GB** | Minimal test (may be slow) | Lowest |
| **1 vCPU & 4 GB** | Light testing | Very Low |
| **2 vCPU & 4 GB** | Small dataset tests | Low |
| **2 vCPU & 8 GB** | Moderate workloads | Low-Medium |
| **4 vCPU & 8 GB** | ✅ **RECOMMENDED** for your solver | Medium |
| **4 vCPU & 16 GB** | Large datasets, complex operations | Medium-High |
| **4 vCPU & 30 GB** | Very large datasets | High |
| **8 vCPU & 16 GB** | Heavy parallel processing | High |
| **8 vCPU & 32 GB** | Production workloads | Very High |
| **16 vCPU & 64 GB** | Enterprise scale | Premium |

**Why 4 vCPU & 8 GB is optimal:**
- ✅ Handles 500 training samples efficiently
- ✅ Sufficient memory for quantum circuit execution
- ✅ Good CPU power for classical SVM training
- ✅ Balanced cost vs performance
- ✅ Completes in 15-30 minutes

**For testing:** Use `2 vCPU & 4 GB` (cheaper, still works)
**For production:** Use `4 vCPU & 8 GB` or higher

---

### **Device (Quantum Backend)**

**Recommended for your solver:**
```
IonQ Simulator (free)
```

**Available Options:**

1. **IonQ Simulator (free)** ✅ **RECOMMENDED**
   - Cost: FREE
   - Type: Classical simulation of quantum circuits
   - Qubits: Unlimited (simulated)
   - Speed: Fast
   - Accuracy: Perfect simulation
   - **Use for:** Testing, development, debugging
   - **Best for first run**

2. **IonQ Forte 1** (Real Quantum Hardware)
   - Cost: EXPENSIVE (charges per shot)
   - Type: Real trapped-ion quantum computer
   - Qubits: 35+ physical qubits
   - Gate fidelity: 99.8%+
   - Speed: Queue time + execution
   - **Use for:** Production runs, final results
   - **Use only after simulator confirms everything works**

**Recommendation:**
1. **First run:** `IonQ Simulator (free)` - Verify your solver works
2. **Development:** `IonQ Simulator (free)` - Test and debug
3. **Final production:** `IonQ Forte 1` - Generate results on real quantum hardware

**Cost Comparison:**
- IonQ Simulator: FREE ✅
- IonQ Forte 1: ~$100-500 per run depending on circuit complexity

---

### **Hardware provider parametrization**
```
No configuration needed
```
**Explanation:** Microsoft provider (classical computing) has no additional parameters.

If QCentroid asks for quantum provider parameters, typical options might be:
- Optimization level: `1` or `2`
- Resilience level: `1`
- Shots per circuit: `1024`

**Leave as default** unless you have specific requirements.

---

## 🎯 Quick Copy-Paste Configuration

| Field | Value |
|-------|-------|
| **Job title** | DBS Fraud Detection - Quantum QSVM Execution |
| **Job comment** | Executing quantum QSVM on credit card fraud dataset with 500 training samples and 200 test samples. Uses ZZFeatureMap and quantum kernels on QCentroid hardware. Expected runtime: 15-30 minutes. |
| **Number of shots** | 1 |
| **Max. execution time** | 60 |
| **Additional arguments** | `{"dataset": "kaggle_credit_card_fraud", "n_train_samples": 500, "n_test_samples": 200, "feature_dimension": 10, "quantum_backend": "qcentroid", "random_state": 42, "enable_logging": true, "save_results": true}` |
| **Device** | ibmq_qasm_simulator (or select available device) |

---

## 💡 Recommended Configurations by Use Case

### **1. Initial Test Run (Quick validation)**
- Job title: `Test Run - QSVM Fraud Detection`
- Shots: `1`
- Max time: `30` minutes
- **Hardware:** `2 vCPU & 4 GB`
- **Device:** `IonQ Simulator (free)`
- Additional args: `{"n_train_samples": 100, "n_test_samples": 50}`
- **Purpose:** Verify solver works correctly
- **Expected cost:** FREE (using simulator)

### **2. Development Run (Standard testing)** ✅ **RECOMMENDED FIRST RUN**
- Job title: `Dev Run - DBS Fraud Detection QSVM`
- Shots: `1`
- Max time: `60` minutes
- **Hardware:** `4 vCPU & 8 GB`
- **Device:** `IonQ Simulator (free)`
- Additional args: `{"n_train_samples": 500, "n_test_samples": 200, "random_state": 42}`
- **Purpose:** Full test with complete dataset
- **Expected cost:** FREE (using simulator)

### **3. Production Run (Final results on real hardware)**
- Job title: `Production - DBS Fraud Detection Quantum QSVM`
- Shots: `3`
- Max time: `90` minutes
- **Hardware:** `4 vCPU & 16 GB`
- **Device:** `IonQ Forte 1` (real quantum hardware)
- Additional args: `{"n_train_samples": 500, "n_test_samples": 200, "random_state": 42, "enable_logging": true, "save_results": true}`
- **Purpose:** Generate final results for submission
- **Expected cost:** $300-900 (real quantum hardware)

### **4. Research Run (Statistical validation)**
- Job title: `Research - QSVM Multiple Runs for Statistics`
- Shots: `10`
- Max time: `120` minutes
- **Hardware:** `8 vCPU & 16 GB`
- **Device:** `IonQ Simulator (free)` or `IonQ Forte 1`
- Additional args: `{"n_train_samples": 500, "n_test_samples": 200, "enable_logging": true}`
- **Purpose:** Generate statistics across multiple runs
- **Expected cost:** FREE (simulator) or $1000+ (real hardware)

---

## ⚠️ Important Notes

1. **Start with simulator:** Always test on `ibmq_qasm_simulator` first before using real quantum hardware

2. **Monitor credits:** Check your credit balance before submitting expensive jobs

3. **Time limits:** Set reasonable time limits to avoid wasting credits if something goes wrong

4. **Shots consideration:** 
   - 1 shot = Quick test
   - 3-5 shots = Good for averaging results
   - 10+ shots = Statistical analysis

5. **Additional arguments:** These are optional - your solver should work with defaults if not provided

6. **Device availability:** Real quantum devices may have queue times; simulator runs immediately

7. **Cost estimation:** 
   - Simulator: ~25-50 credits per run
   - Real hardware: ~100-300 credits per run (varies by device)

---

## ✅ Pre-Submission Checklist

Before submitting the job:

- [ ] SSH key added to GitHub repository
- [ ] Solver registered and visible in QCentroid
- [ ] Job title is descriptive
- [ ] Number of shots is appropriate (start with 1)
- [ ] Time limit set (60 minutes recommended)
- [ ] Device selected (simulator for testing)
- [ ] Additional arguments validated (valid JSON)
- [ ] Credit balance checked

---

## 🚀 After Job Submission

What happens next:

1. **Job queued:** Your job enters the execution queue
2. **Repository cloned:** QCentroid clones your GitHub repo
3. **Dependencies installed:** `pip install -r requirements.txt`
4. **Solver executed:** `python main.py` runs with your configuration
5. **Results captured:** Output, logs, and results files saved
6. **Credits charged:** Based on actual usage
7. **Notification:** You'll be notified when job completes

Expected outputs:
- Console logs with progress
- Performance metrics (accuracy, precision, recall, F1)
- Predictions file (if save_results=true)
- Quantum circuit execution details
- Runtime statistics

---

## 🎉 You're Ready to Submit!

All configuration options are explained. Choose the settings that match your use case and submit your job!

**Recommended for first run:** Use the "Development Run" configuration above.

Good luck! 🚀⚛️
