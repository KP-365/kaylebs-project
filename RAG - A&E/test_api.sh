#!/bin/bash

# Test script for AI Triage API

echo "Testing Health Endpoint..."
curl -X GET http://localhost:8000/api/health
echo -e "\n\n"

echo "Testing Triage Endpoint - Chest Pain (RED case)..."
curl -X POST http://localhost:8000/api/triage \
  -H "Content-Type: application/json" \
  -d '{
    "age": 55,
    "sex": "M",
    "chief_complaint": "chest_pain",
    "answers": {
      "shortness_of_breath": true,
      "sweating": true,
      "heart_disease": true
    }
  }'
echo -e "\n\n"

echo "Testing Triage Endpoint - Headache (GREEN case)..."
curl -X POST http://localhost:8000/api/triage \
  -H "Content-Type: application/json" \
  -d '{
    "age": 30,
    "sex": "F",
    "chief_complaint": "headache",
    "answers": {
      "severe": false,
      "confusion": false
    }
  }'
echo -e "\n\n"


