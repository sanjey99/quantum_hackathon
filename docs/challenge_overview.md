### Overview 
In this hackathon challenge, participants are tasked with developing a quantum-enhanced feature selection
method for credit-card fraud detection. The goal is to select compact, high-information feature subsets that
maximize fraud-classification performance and ideally to benchmark quantum and classical approaches under
identical conditions. Participants receive two labeled dataset of anonymized transactions. Each record includes
features such as transaction amount, timestamp, etc. where fraudulent samples form less than 1% of the dataset.
The task is to find the smallest feature subset that achieves strong fraud-detection accuracy while being
compatible with limited quantum resources of today’s noisy intermediate scale quantum hardware (NISQ).

## Key focus areas 
Data preprocessing of classical transaction data
Mitigate the imbalance between fraudulent and legitimate transactions for model training
Removal of highly correlated features
Normalization of features
Initial choice of dominant features, e.g. with principal component analysis
Quantum encoding of transaction data
Choice and computation of quantum kernel for support vector machine
Minimization of the objective function with a classical optimizer
Determine model accuracy with performance metrics and adjust chosen feature subset if needed
Comparison with classical feature selection baselines