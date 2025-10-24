package com.qcentroid.frauddetection.model;

import com.fasterxml.jackson.annotation.JsonProperty;

public class FraudPrediction {
    @JsonProperty("transaction_id")
    private String transactionId;
    @JsonProperty("fraud_probability")
    private double fraudProbability;
    @JsonProperty("is_fraud")
    private boolean isFraud;
    private String confidence;

    // Getters and Setters
    public String getTransactionId() {
        return transactionId;
    }

    public void setTransactionId(String transactionId) {
        this.transactionId = transactionId;
    }

    public double getFraudProbability() {
        return fraudProbability;
    }

    public void setFraudProbability(double fraudProbability) {
        this.fraudProbability = fraudProbability;
    }

    public boolean getIsFraud() {
        return isFraud;
    }

    public void setIsFraud(boolean isFraud) {
        this.isFraud = isFraud;
    }

    public String getConfidence() {
        return confidence;
    }

    public void setConfidence(String confidence) {
        this.confidence = confidence;
    }
}