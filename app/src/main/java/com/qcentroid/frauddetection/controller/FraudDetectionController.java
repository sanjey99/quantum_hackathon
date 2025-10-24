package com.qcentroid.frauddetection.controller;

import java.util.List;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.qcentroid.frauddetection.model.FraudPrediction;
import com.qcentroid.frauddetection.model.Transaction;
import com.qcentroid.frauddetection.service.FraudDetectionService;

@RestController
@RequestMapping("/api/fraud")
public class FraudDetectionController {
    private final FraudDetectionService fraudDetectionService;

    public FraudDetectionController(FraudDetectionService fraudDetectionService) {
        this.fraudDetectionService = fraudDetectionService;
    }

    @PostMapping("/detect")
    public ResponseEntity<List<FraudPrediction>> detectFraud(@RequestBody List<Transaction> transactions) {
        List<FraudPrediction> predictions = fraudDetectionService.detectFraud(transactions);
        return ResponseEntity.ok(predictions);
    }
}