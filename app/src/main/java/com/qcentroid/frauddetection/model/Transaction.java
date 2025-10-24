package com.qcentroid.frauddetection.model;

import com.fasterxml.jackson.annotation.JsonProperty;

public class Transaction {
    private double amount;
    private int hour;
    @JsonProperty("day_of_week")
    private int dayOfWeek;
    @JsonProperty("is_weekend")
    private int isWeekend;
    @JsonProperty("amount_log")
    private double amountLog;
    @JsonProperty("customer_tx_count")
    private int customerTxCount;
    @JsonProperty("merchant_tx_count")
    private int merchantTxCount;
    @JsonProperty("merchant_category_encoded")
    private int merchantCategoryEncoded;
    @JsonProperty("transaction_id")
    private String transactionId;

    // Getters and Setters
    public double getAmount() {
        return amount;
    }

    public void setAmount(double amount) {
        this.amount = amount;
    }

    public int getHour() {
        return hour;
    }

    public void setHour(int hour) {
        this.hour = hour;
    }

    public int getDayOfWeek() {
        return dayOfWeek;
    }

    public void setDayOfWeek(int dayOfWeek) {
        this.dayOfWeek = dayOfWeek;
    }

    public int getIsWeekend() {
        return isWeekend;
    }

    public void setIsWeekend(int isWeekend) {
        this.isWeekend = isWeekend;
    }

    public double getAmountLog() {
        return amountLog;
    }

    public void setAmountLog(double amountLog) {
        this.amountLog = amountLog;
    }

    public int getCustomerTxCount() {
        return customerTxCount;
    }

    public void setCustomerTxCount(int customerTxCount) {
        this.customerTxCount = customerTxCount;
    }

    public int getMerchantTxCount() {
        return merchantTxCount;
    }

    public void setMerchantTxCount(int merchantTxCount) {
        this.merchantTxCount = merchantTxCount;
    }

    public int getMerchantCategoryEncoded() {
        return merchantCategoryEncoded;
    }

    public void setMerchantCategoryEncoded(int merchantCategoryEncoded) {
        this.merchantCategoryEncoded = merchantCategoryEncoded;
    }

    public String getTransactionId() {
        return transactionId;
    }

    public void setTransactionId(String transactionId) {
        this.transactionId = transactionId;
    }
}