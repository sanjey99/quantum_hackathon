# Classical Bottleneck Analysis: Feature Selection in Fraud Detection

## Executive Summary

This document analyzes the computational bottlenecks of classical machine learning approaches to fraud detection, with a focus on feature selection. We demonstrate why quantum computing approaches, specifically Quantum Support Vector Machines (QSVM) with quantum kernels, offer potential advantages for this problem.

---

## 1. The Feature Selection Problem

### 1.1 Problem Statement

In fraud detection with **d** features, we seek to find an optimal subset **z ∈ {0,1}ᵈ** where:
- z_i = 1 if feature i is selected
- z_i = 0 if feature i is excluded

**Goal:** Minimize |z| (number of features) while maximizing classification accuracy.

### 1.2 Combinatorial Explosion

The number of possible feature subsets is **2ᵈ**, which grows exponentially:

| Features (d) | Possible Subsets | Search Time* |
|--------------|------------------|--------------|
| 10           | 1,024            | ~1 second    |
| 20           | 1,048,576        | ~17 minutes  |
| 30           | 1,073,741,824    | ~12 days     |
| 40           | 1.1 × 10¹²       | ~35 years    |

*Assuming 1ms per evaluation

**Impact on Fraud Detection:**
- Credit card fraud datasets typically have 30-100+ features
- Exhaustive search becomes computationally intractable
- Must resort to heuristic methods (greedy, genetic algorithms)

---

## 2. Classical Approach Limitations

### 2.1 Greedy Forward Selection

**Method:** Start with empty set, iteratively add the best single feature.

**Computational Complexity:** O(d² · n · T)
- d: number of features
- n: number of samples
- T: training time per model

**Limitations:**
1. **Local Optima:** May miss globally optimal feature combinations
2. **No Backtracking:** Cannot undo previous selections
3. **Interaction Blindness:** Cannot detect synergistic feature combinations
4. **Scalability:** Still O(d²) evaluations required

**Example:**
```
Dataset: 50 features, 100,000 samples
Greedy iterations: 50 × 49 / 2 = 1,225 model trainings
Time per training: ~10 seconds
Total time: ~3.4 hours (for suboptimal solution)
```

### 2.2 Classical SVM with Kernel Methods

**Standard Kernels:**
- Linear: K(x, y) = x · y
- RBF: K(x, y) = exp(-γ||x - y||²)
- Polynomial: K(x, y) = (x · y + c)ᵖ

**Limitations:**
1. **Fixed Geometry:** Kernel function predetermined, not data-adaptive
2. **Curse of Dimensionality:** Performance degrades with high dimensions
3. **Manual Tuning:** Hyperparameters (γ, p, c) require extensive grid search
4. **Limited Expressiveness:** Cannot capture arbitrary feature correlations

**Computational Cost:**
- Kernel matrix computation: O(n² · d)
- For 100,000 samples, 30 features: ~300 billion operations
- Memory: ~40 GB for full kernel matrix

### 2.3 Random Forest and Ensemble Methods

**Advantages:**
- Built-in feature importance
- Handles non-linear relationships

**Limitations:**
1. **Feature Importance ≠ Feature Selection:** 
   - Importance doesn't tell you which *subset* to use
   - Still need search over combinations
2. **Computational Cost:** O(T · n · log(n) · d)
   - T: number of trees (typically 100-500)
   - Still linear in d, but multiplicative constant is large
3. **Black Box:** Cannot explain *why* certain feature combinations work

---

## 3. Dimensionality and the Curse

### 3.1 High-Dimensional Feature Spaces

Fraud detection datasets are inherently high-dimensional:

**Typical Features:**
- Transaction amount, time, location
- Merchant category, customer history
- Device fingerprints, IP addresses
- Behavioral patterns (>50 derived features)

**Problem:** Most classical algorithms struggle in high dimensions

### 3.2 Sample Complexity

Required samples for reliable classification scales exponentially with dimensions:

**Rule of Thumb:** Need at least 10 samples per dimension
- 50 features → 500 minimum samples
- But fraudulent transactions are <1% of data!
- Need 50,000+ transactions to get 500 fraud examples

### 3.3 Distance Concentration

In high dimensions, distances between points become uniform:
- All points appear equidistant
- Classical distance-based methods (KNN, SVM) fail
- Fraud signals get "lost in the noise"

---

## 4. Computational Bottlenecks Summary

### 4.1 Time Complexity Comparison

| Method | Complexity | 50 Features | 100 Features |
|--------|------------|-------------|--------------|
| Exhaustive Search | O(2ᵈ) | 1.1 × 10¹⁵ | 1.3 × 10³⁰ |
| Greedy Forward | O(d²) | 2,500 | 10,000 |
| Classical SVM | O(n² · d) | High | Very High |
| Random Forest | O(T · n log n · d) | Medium | High |

### 4.2 Energy Consumption

Training large-scale fraud detection systems:

**Classical Approach:**
- 1 epoch on 1M samples: ~50 kWh
- Hyperparameter tuning: 100+ experiments
- **Total: ~5,000 kWh** (equivalent to 500 km of electric car driving)

**Problem Scale:**
- Banks process billions of transactions daily
- Models need retraining weekly/daily
- Energy costs and carbon footprint are significant

---

## 5. Why Quantum Computing?

### 5.1 Quantum Advantage for Feature Selection

**Quantum Superposition:**
- Can explore multiple feature combinations simultaneously
- Not limited by classical O(2ᵈ) search space

**Quantum Entanglement:**
- Naturally captures feature correlations
- Can represent exponentially large feature spaces compactly

**Quantum Kernels:**
- Implicit mapping to high-dimensional Hilbert space
- Can capture correlations intractable for classical kernels

### 5.2 Theoretical Speedup

**QSVM with Quantum Kernels:**
- Kernel computation: O(poly(log d)) vs O(n²d) classical
- Feature space dimension: 2ⁿ (exponential in qubits)
- Potential quadratic speedup in certain regimes

**Feature Selection:**
- Quantum algorithms (QAOA, VQE) can explore 2ᵈ space more efficiently
- Not guaranteed speedup, but more expressive search

### 5.3 Better Fraud Detection

**Quantum Kernels:**
- Can capture subtle, non-linear fraud patterns
- Better separation in quantum Hilbert space
- Potentially higher AUC-ROC and AUC-PR scores

**Compact Feature Sets:**
- Quantum feature selection finds smaller |z|
- Faster real-time inference
- Lower deployment costs

---

## 6. Empirical Evidence

### 6.1 Literature Support

**Research Papers:**
1. "Quantum Support Vector Machines for Classification" (Rebentrost et al., 2014)
   - Demonstrates exponential speedup for certain kernels
   
2. "Quantum Feature Selection for Classification" (Li et al., 2022)
   - Shows 10-20% accuracy improvement on benchmark datasets
   
3. "Mixed Quantum-Classical Method for Fraud Detection" (CERN, 2022)
   - Applied to credit card fraud, achieved 15% reduction in false positives

### 6.2 Challenge Objectives

This hackathon challenge specifically targets:
1. **Quantum-enhanced feature selection** using quantum kernels
2. **Comparison with classical baselines** on same datasets
3. **Benchmarking AUC-ROC, AUC-PR, F1 scores**

---

## 7. Limitations and Caveats

### 7.1 NISQ Era Constraints

Current quantum hardware limitations:
- Limited qubits (~10-50 for stable computation)
- High noise levels (~1% error rate)
- Short coherence times (~100 μs)

**Implication:** Cannot yet outperform classical on large-scale problems

### 7.2 When Quantum Helps

Quantum advantage likely when:
- **High-dimensional** feature spaces (d > 50)
- **Complex correlations** between features
- **Non-linear** decision boundaries
- **Imbalanced** datasets (fraud detection!)

### 7.3 Hybrid Approach

Best current strategy:
- **Quantum:** Feature selection, kernel computation
- **Classical:** Optimization (SVM training), data preprocessing
- **Hybrid:** Quantum-classical iterative refinement

---

## 8. Conclusion

### Key Takeaways

1. **Combinatorial Explosion:** Feature selection is exponentially hard (2ᵈ possible subsets)

2. **Classical Bottlenecks:**
   - Greedy methods: O(d²), finds local optima
   - Classical SVM: O(n²d), limited kernel expressiveness
   - High-dimensional curse: distance concentration, sample complexity

3. **Quantum Potential:**
   - Superposition explores multiple combinations simultaneously
   - Quantum kernels capture complex correlations
   - Potential for compact, high-performing feature sets

4. **Current Reality:**
   - NISQ devices have limitations
   - Hybrid quantum-classical approach is practical
   - Focus on demonstrating methodology, not claiming superiority

### Forward-Looking Statement

**Near-term (1-3 years):**
- QSVM competitive with classical on small-scale problems (d < 20)
- Useful for research and algorithm development

**Medium-term (3-7 years):**
- Error-corrected quantum computers with 100+ logical qubits
- Potential advantage for high-dimensional fraud detection
- Hybrid quantum-classical systems in production

**Long-term (7+ years):**
- Fault-tolerant quantum computers with 1000+ qubits
- Quantum advantage clearly demonstrated
- Quantum fraud detection as standard practice in financial industry

---

## References

1. Rebentrost, P., Mohseni, M., & Lloyd, S. (2014). "Quantum support vector machine for big data classification." Physical review letters, 113(13).

2. Havlíček, V., et al. (2019). "Supervised learning with quantum-enhanced feature spaces." Nature, 567(7747), 209-212.

3. Schuld, M., & Killoran, N. (2019). "Quantum machine learning in feature Hilbert spaces." Physical Review Letters, 122(4).

4. CERN Quantum Computing (2022). "Mixed Quantum-Classical Method for Fraud Detection With Quantum Feature Selection."

5. Preskill, J. (2018). "Quantum Computing in the NISQ era and beyond." Quantum, 2, 79.

6. Bharti, K., et al. (2022). "Noisy intermediate-scale quantum algorithms." Reviews of Modern Physics, 94(1).

---

**Document Version:** 1.0  
**Last Updated:** October 2025  
**Challenge:** DBS Fraud Detection Challenge-2 Singapore
