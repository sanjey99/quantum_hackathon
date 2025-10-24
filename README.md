# Quantum Fraud Detection System

A fraud detection system using quantum computing via QCentroid and machine learning, developed during a 36-hour hackathon.

## 🚀 Quick Links

- **[Quick Start Guide](QUICKSTART.md)** - Get running in 5 minutes
- **[QCentroid Setup](QCENTROID_SETUP.md)** - Quantum computing integration
- **[Contributing](CONTRIBUTING.md)** - How to contribute to this project
- **[API Documentation](#api-endpoints)** - REST API reference

## Project Structure

```
quantum_hackathon/
├── .github/              # GitHub workflows and templates
├── app/                  # Java Spring Boot service
│   ├── src/
│   │   ├── main/java/com/qcentroid/frauddetection/
│   │   │   ├── controller/          # REST API controllers
│   │   │   ├── model/               # Data models (Transaction, FraudPrediction)
│   │   │   ├── service/             # Business logic (FraudDetectionService)
│   │   │   └── FraudDetectionApplication.java
│   │   └── test/        # Java unit tests
│   ├── pom.xml          # Maven dependencies
│   └── target/          # Build output (gitignored)
├── data/                # Dataset storage
│   ├── raw/             # Original datasets (gitignored)
│   └── processed/       # Preprocessed datasets (gitignored)
├── model/               # Python production code
│   ├── fraud_data_analysis.py       # Data preprocessing & feature engineering
│   ├── fraud_model_development.py   # Model training (Classical + Quantum)
│   ├── predict.py                   # Prediction service
│   ├── qcentroid_config.py          # QCentroid client configuration
│   └── saved_models/                # Trained models (gitignored)
├── notebooks/           # Jupyter notebooks for exploration
│   ├── fraud_data_analysis.ipynb
│   ├── fraud_detection.ipynb
│   └── fraud_model_development.ipynb
├── tools/               # Build tools (auto-downloaded, gitignored)
│   └── apache-maven-*/  # Maven installation
├── .env.example         # Environment variables template
├── .gitignore          # Git ignore rules
├── build.cmd           # Windows build script
├── build.sh            # Unix/Linux/Mac build script
├── CONTRIBUTING.md     # Contribution guidelines
├── QCENTROID_SETUP.md  # QCentroid integration guide
├── README.md           # This file
└── requirements.txt    # Python dependencies
```

## Setup Instructions

### Prerequisites

- Python 3.13+ (for ML and quantum computing)
- Java JDK 11+ (for Spring Boot service)
- Git

### Python Environment Setup

1. Create a virtual environment with Python 3.13:
```bash
# Windows
py -3.13 -m venv venv-new
.\venv-new\Scripts\activate

# Unix/Linux/Mac
python3.13 -m venv venv-new
source venv-new/bin/activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

### QCentroid Setup

For quantum computing integration with QCentroid's online IDE and execution platform, see the detailed guide:

📘 **[QCentroid Integration Guide](QCENTROID_SETUP.md)**

Quick setup:
1. Copy `.env.example` to `.env`
2. Add your QCentroid API credentials
3. Install quantum dependencies: `pip install -r requirements.txt`
4. Test connection: `python model/qcentroid_config.py`

### Java Environment Setup

1. Ensure you have JDK 11+ installed and JAVA_HOME environment variable is set
2. Build the Java application:

**Windows:**
```batch
.\build.cmd clean install
```

**Unix/Linux/Mac:**
```bash
chmod +x build.sh
./build.sh clean install
```

Note: The build script will automatically download and set up Maven 3.9.5 if it's not already installed. The build process requires JDK 11 or higher.

## Development Workflow

### 1. Data Scientists
- Work in the `model/` directory
- Use Jupyter notebooks for data exploration (`notebooks/`)
- Develop ML models using QCentroid's quantum computing capabilities
- Train and save models to `model/saved_models/`

### 2. Backend Engineers
- Work in the `app/` directory
- Build the Java service:
  ```bash
  # Windows
  .\build.cmd clean install
  
  # Unix/Linux/Mac
  ./build.sh clean install
  ```
- Run the Spring Boot application:
  ```bash
  # Windows
  .\build.cmd spring-boot:run
  
  # Unix/Linux/Mac
  ./build.sh spring-boot:run
  ```

### 3. Testing

**Python Tests:**
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=model --cov-report=html

# Run specific test file
pytest tests/test_fraud_detection.py
```

**Java Tests:**
```bash
# Windows
.\build.cmd test

# Unix/Linux/Mac
./build.sh test
```

## API Endpoints

Once the Spring Boot service is running (default: http://localhost:8080):

- `POST /api/fraud/detect` - Detect fraud in transactions
  ```json
  {
    "transactions": [{
      "amount": 150.00,
      "hour": 14,
      "day_of_week": 3,
      "is_weekend": 0,
      "merchant_category": "retail"
    }]
  }
  ```

- `GET /api/health` - Health check endpoint

## Technology Stack

### Python Stack (ML/Data Science)
- **Core ML**: Pandas, NumPy, Scikit-learn
- **Advanced ML**: XGBoost, Imbalanced-learn
- **Quantum Computing**: QCentroid, Qiskit, PennyLane
- **Visualization**: Matplotlib, Seaborn
- **Development**: Jupyter, IPython
- **Testing**: Pytest, pytest-cov
- **Code Quality**: Black, Flake8

### Java Stack (Backend Service)
- **Framework**: Spring Boot 2.7.x
- **Build Tool**: Maven 3.9.5 (auto-installed)
- **Testing**: JUnit 5
- **JSON Processing**: Jackson
- **Logging**: SLF4J + Logback

### Quantum Computing Integration
- **Primary**: QCentroid platform (when available)
- **Fallback**: Qiskit (IBM Quantum)
- **Alternative**: PennyLane (Quantum ML)

## Project Goals

Build a fraud detection system that:
1. ✅ Processes and analyzes transaction data
2. ✅ Integrates quantum computing for enhanced pattern recognition
3. ✅ Provides real-time fraud detection via REST API
4. ✅ Demonstrates improved accuracy over classical methods
5. ✅ Supports both local development and cloud quantum execution

## Key Features

- **Hybrid Classical-Quantum ML**: Combines traditional ML with quantum algorithms
- **REST API Integration**: Java Spring Boot service for production deployment
- **Scalable Architecture**: Modular design for easy enhancement
- **Automated Build**: Cross-platform build scripts with automatic Maven setup
- **Cloud-Ready**: Integration with QCentroid's online IDE and quantum hardware
- **Comprehensive Testing**: Unit tests for both Python and Java components

## Documentation

- 📘 [QCentroid Integration Guide](QCENTROID_SETUP.md) - Quantum computing setup
- 📦 [Build Scripts](build.cmd) / [build.sh](build.sh) - Automated build process
- 🔧 [Environment Setup](.env.example) - Configuration template
- 📊 [Notebooks](notebooks/) - Interactive analysis and exploration

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Make your changes and commit: `git commit -am 'Add new feature'`
4. Push to the branch: `git push origin feature/your-feature`
5. Submit a pull request

## License

This project was developed during a 36-hour hackathon for educational and demonstration purposes.

## Team Members

- **Data Scientist**: Python/ML model development
- **Backend Engineer**: Java/Spring Boot integration
- **DevOps/Integration**: Build automation and deployment

## Troubleshooting

### Python Issues
- **ImportError**: Ensure virtual environment is activated and dependencies are installed
- **Quantum Backend Error**: Check `.env` configuration or use simulator backend
- **Model Not Found**: Train models first using `fraud_model_development.py`

### Java Issues
- **JAVA_HOME not set**: Set environment variable to your JDK installation
- **Build fails**: Ensure JDK 11+ is installed and accessible
- **Tests fail**: Models may not be trained yet - use `-DskipTests` flag

### Build Issues
- **Maven download fails**: Check internet connection or use local Maven installation
- **Permission denied**: On Unix/Linux, run `chmod +x build.sh`

For more help, see individual documentation files or open an issue.