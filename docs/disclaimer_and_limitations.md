# Disclaimer and Limitations

## Not Medical Advice

This tool is a student data science project built for educational purposes only. It does not provide medical advice, diagnosis, or treatment recommendations. The outputs of this model should never be used as a substitute for professional medical judgment. Always consult a qualified healthcare provider for any health concerns.

## Educational Purpose

This demo was created to explore machine learning techniques applied to publicly available health survey data (NHANES). It is intended to help students learn about data pipelines, model training, and responsible AI in healthcare contexts.

## Limitations

- **Dataset bias**: The dataset is derived from NHANES cross-sectional survey data. Because it captures a single point in time, it cannot establish causal relationships, and the stroke labels reflect self-reported stroke history rather than prospective future risk.
- **Simple model**: A logistic regression classifier is used as a baseline. This model is not optimized for clinical use and has limited predictive performance (ROC AUC ~0.62). More complex models and richer feature engineering would be needed for real-world deployment.
- **Not clinically validated**: This model has not been validated against clinical standards, peer-reviewed, or approved by any regulatory body. The risk scores and labels are for demonstration purposes only and do not reflect actual clinical risk thresholds.
