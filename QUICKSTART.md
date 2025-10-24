# Quick Start Guide

Get the Quantum Fraud Detection System up and running in 5 minutes!

## Prerequisites Checklist

- [ ] Python 3.13+ installed
- [ ] Java JDK 11+ installed
- [ ] Git installed
- [ ] Internet connection (for downloading dependencies)

## 🚀 Quick Setup (5 minutes)

### Step 1: Clone and Navigate (30 seconds)

```bash
git clone https://github.com/sanjey99/quantum_hackathon.git
cd quantum_hackathon
```

### Step 2: Set Up Python Environment (2 minutes)

```bash
# Windows
py -3.13 -m venv venv-new
.\venv-new\Scripts\activate
pip install -r requirements.txt

# Unix/Linux/Mac
python3.13 -m venv venv-new
source venv-new/bin/activate
pip install -r requirements.txt
```

### Step 3: Build Java Service (2 minutes)

```bash
# Windows
.\build.cmd clean install -DskipTests

# Unix/Linux/Mac
chmod +x build.sh
./build.sh clean install -DskipTests
```

### Step 4: Test Configuration (30 seconds)

```bash
# Test quantum backend connection
python model/qcentroid_config.py

# Expected output:
# ✓ Using Qiskit AerSimulator (fallback)
# ✓ Quantum backend is ready!
```

## 🎯 Running the System

### Option A: Run Python Models Directly

```bash
# Activate environment
.\venv-new\Scripts\activate  # Windows
# source venv-new/bin/activate  # Unix/Linux/Mac

# Run data analysis
python model/fraud_data_analysis.py

# Train models
python model/fraud_model_development.py

# Test predictions
python model/predict.py < sample_input.json
```

### Option B: Run Java REST API

```bash
# Start Spring Boot service
.\build.cmd spring-boot:run  # Windows
./build.sh spring-boot:run   # Unix/Linux/Mac

# Service starts at: http://localhost:8080
```

### Option C: Use Jupyter Notebooks

```bash
# Activate environment
.\venv-new\Scripts\activate

# Start Jupyter
jupyter notebook

# Open notebooks in notebooks/ directory
```

## 🧪 Quick Test

### Test 1: Python Environment

```bash
python -c "import numpy, pandas, sklearn, qiskit; print('✓ All packages imported successfully!')"
```

### Test 2: Java Build

```bash
# Windows
.\build.cmd --version

# Unix/Linux/Mac
./build.sh --version
```

### Test 3: API Health Check

```bash
# Start the service first, then:
curl http://localhost:8080/api/health
```

## 📊 Sample Data

Create a sample transaction file `sample_transaction.json`:

```json
{
  "amount": 150.00,
  "hour": 14,
  "day_of_week": 3,
  "is_weekend": 0,
  "amount_log": 5.01,
  "customer_tx_count": 45,
  "merchant_tx_count": 230,
  "merchant_category_encoded": 5
}
```

Test prediction:

```bash
python model/predict.py < sample_transaction.json
```

## 🔧 QCentroid Setup (Optional)

For quantum computing features:

1. **Copy environment template:**
   ```bash
   cp .env.example .env
   ```

2. **Add your credentials to `.env`:**
   ```bash
   QCENTROID_API_KEY=your_key_here
   QCENTROID_WORKSPACE_ID=your_workspace_id
   ```

3. **Test connection:**
   ```bash
   python model/qcentroid_config.py
   ```

For detailed quantum setup, see [QCENTROID_SETUP.md](QCENTROID_SETUP.md)

## 📝 Next Steps

Now that you're set up:

1. **Explore the notebooks** - `notebooks/` directory
2. **Train your own models** - Run `fraud_model_development.py`
3. **Customize the API** - Modify files in `app/src/`
4. **Read the docs** - Check [README.md](README.md) for full documentation

## 🐛 Common Issues

### "Python not found"
```bash
# Windows: Install from python.org
# Mac: brew install python@3.13
# Linux: sudo apt install python3.13
```

### "JAVA_HOME not set"
```bash
# Windows
set JAVA_HOME=C:\Program Files\Java\jdk-11

# Unix/Linux/Mac
export JAVA_HOME=/usr/lib/jvm/java-11
```

### "Permission denied on build.sh"
```bash
chmod +x build.sh
./build.sh clean install
```

### "Module not found"
```bash
# Ensure virtual environment is activated
.\venv-new\Scripts\activate  # Windows
source venv-new/bin/activate # Unix/Linux/Mac

# Reinstall dependencies
pip install -r requirements.txt
```

## 💡 Tips

- **Use virtual environments** - Always activate before running Python code
- **Check Java version** - Must be 11 or higher
- **Internet required** - First build downloads Maven and dependencies
- **Be patient** - First setup takes a few minutes

## 🆘 Need Help?

- 📖 Full documentation: [README.md](README.md)
- 🔬 Quantum setup: [QCENTROID_SETUP.md](QCENTROID_SETUP.md)
- 🤝 Contributing: [CONTRIBUTING.md](CONTRIBUTING.md)
- 🐛 Issues: [GitHub Issues](https://github.com/sanjey99/quantum_hackathon/issues)

---

**Ready to detect fraud with quantum power!** 🚀✨
