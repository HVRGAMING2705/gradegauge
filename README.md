# GradeGauge — Student Exam Score Predictor

Predicts a student's exam score (0–100) from 5 inputs: study hours/day, attendance %, sleep hours/night, previous exam score, and assignments completed.

## Model
Ridge regression (alpha = 1.0) on standardized features, trained on 500 synthetic student records (`train.py`, seed 42).

## Results (5-fold CV)
- R² = 0.871, MAE = 4.54 marks, RMSE = 5.81 marks
- Baseline (predict the mean): MAE = 13.94 marks

## Demo
Open `index.html` — the demo runs entirely in the browser using the exported coefficients in `model.json`. No backend needed.

## Live
https://gradegauge-theta.vercel.app

Built by Vikranth Reddy (B.Tech CSE AI&ML, Woxsen University).
