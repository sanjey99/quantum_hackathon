package com.qcentroid.frauddetection.service;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.util.Arrays;
import java.util.List;
import java.util.concurrent.TimeUnit;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.qcentroid.frauddetection.model.FraudPrediction;
import com.qcentroid.frauddetection.model.Transaction;

@Service
public class FraudDetectionService {
    private static final Logger logger = LoggerFactory.getLogger(FraudDetectionService.class);
    private final ObjectMapper objectMapper;
    private static final String PYTHON_SCRIPT = "../model/predict.py";

    public FraudDetectionService(ObjectMapper objectMapper) {
        this.objectMapper = objectMapper;
    }

    public List<FraudPrediction> detectFraud(List<Transaction> transactions) {
        try {
            // Convert transactions to JSON
            String input = objectMapper.writeValueAsString(transactions);

            // Build process
            ProcessBuilder processBuilder = new ProcessBuilder("python", PYTHON_SCRIPT);
            processBuilder.redirectErrorStream(true);

            // Start process
            Process process = processBuilder.start();

            // Write input
            try (OutputStreamWriter writer = new OutputStreamWriter(process.getOutputStream())) {
                writer.write(input);
                writer.flush();
            }

            // Read output
            StringBuilder output = new StringBuilder();
            try (BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()))) {
                String line;
                while ((line = reader.readLine()) != null) {
                    output.append(line);
                }
            }

            // Wait for process to complete
            if (!process.waitFor(30, TimeUnit.SECONDS)) {
                process.destroyForcibly();
                throw new RuntimeException("Python script execution timed out");
            }

            if (process.exitValue() != 0) {
                throw new RuntimeException("Python script execution failed: " + output);
            }

            // Parse predictions
            return Arrays.asList(objectMapper.readValue(output.toString(), FraudPrediction[].class));

        } catch (Exception e) {
            logger.error("Error detecting fraud: ", e);
            throw new RuntimeException("Failed to process fraud detection", e);
        }
    }
}