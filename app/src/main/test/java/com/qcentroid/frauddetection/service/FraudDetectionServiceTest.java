package com.qcentroid.frauddetection.service;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.qcentroid.frauddetection.model.Transaction;
import com.qcentroid.frauddetection.model.FraudPrediction;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.util.ArrayList;
import java.util.List;

import static org.junit.jupiter.api.Assertions.*;

@ExtendWith(MockitoExtension.class)
class FraudDetectionServiceTest {

    private FraudDetectionService fraudDetectionService;

    @BeforeEach
    void setUp() {
        fraudDetectionService = new FraudDetectionService(new ObjectMapper());
    }

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

        List<Transaction> transactions = new ArrayList<>();
        transactions.add(transaction);

        // Call the service
        List<FraudPrediction> predictions = fraudDetectionService.detectFraud(transactions);

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