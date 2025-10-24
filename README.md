# Quantum Fraud Detection System

A fraud detection system using quantum computing via QCentroid and machine learning, developed during a 36-hour hackathon.

## Project Structure

```
quantum_hackathon/
├── app/                  # Java Spring Boot service
│   ├── src/             # Java source code
│   └── pom.xml          # Maven dependencies
├── data/                # Dataset storage
│   └── processed/       # Preprocessed datasets
├── model/               # Python production code
│   ├── fraud_data_analysis.py    # Data preprocessing
│   ├── fraud_model_development.py # Model training
│   └── predict.py               # Prediction service
├── notebooks/           # Jupyter notebooks for development
│   ├── fraud_data_analysis.ipynb
│   ├── fraud_detection.ipynb
│   └── fraud_model_development.ipynb
└── requirements.txt     # Python dependencies
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

1. Data Scientists:
   - Work in the `model/` directory
   - Use Jupyter notebooks for data exploration
   - Develop ML models using QCentroid's quantum computing capabilities

2. Backend Engineers:
   - Work in the `app/` directory
   - Run the Spring Boot application using:
   ```bash
   # Windows
   .\build.cmd spring-boot:run

   # Unix/Linux/Mac
   ./build.sh spring-boot:run
   ```

3. Testing:
   - Python tests can be run using pytest
   - Java tests can be run using Maven

## Team Members

- Member 1: Data Scientist (Python/ML)
- Member 2: Backend/Integration Engineer (Java)
- Member 3: Support Developer & Integrator

## Technology Stack

- Python for ML/Model Development
  - Pandas, Scikit-learn for classical ML
  - QCentroid for quantum computing
  - Jupyter for interactive development

- Java Spring Boot for Backend
  - REST API for model integration
  - Maven for dependency management

## Project Goals

Build a fraud detection system that:
1. Processes transaction data
2. Uses quantum computing for enhanced pattern recognition
3. Provides real-time fraud detection via API
4. Demonstrates improved accuracy over classical methods