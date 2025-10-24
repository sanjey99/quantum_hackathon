package com.qcentroid.frauddetection.service;

import java.util.Arrays;
import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertTrue;
import org.junit.jupiter.api.Test;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.qcentroid.frauddetection.model.FraudPrediction;
import com.qcentroid.frauddetection.model.Transaction;

class FraudDetectionServiceTest {

    private final FraudDetectionService fraudDetectionService = new FraudDetectionService(new ObjectMapper());

    @Test
    void testDetectFraud() {
        // Create a test transaction
        Transaction transaction = new Transaction();
        transaction.setAmount(1000.0);
        transaction.setHour(14);
        transaction.setDayOfWeek(2);
        transaction.setIsWeekend(0);
        transaction.setAmountLog(Math.log(1000.0));
        transaction.setCustomerTxCount(5);
        transaction.setMerchantTxCount(10);
        transaction.setMerchantCategoryEncoded(1);
        transaction.setTransactionId("test-tx-1");

        // Call the service
        List<FraudPrediction> predictions = fraudDetectionService.detectFraud(Arrays.asList(transaction));

        // Verify the results
        assertNotNull(predictions);
        assertFalse(predictions.isEmpty());
        assertEquals(1, predictions.size());

        FraudPrediction prediction = predictions.get(0);
        assertEquals("test-tx-1", prediction.getTransactionId());
        assertNotNull(prediction.getIsFraud());
        assertTrue(prediction.getFraudProbability() >= 0.0 && prediction.getFraudProbability() <= 1.0);
    }
}