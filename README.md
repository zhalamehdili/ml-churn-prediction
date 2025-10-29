# Customer Churn Prediction (ML Pipeline)

This project predicts customer churn using a machine learning pipeline in Python.  
It’s based on the Telco Customer Churn dataset and focuses on analyzing customer behavior, training predictive models, and preparing everything for future deployment with an API.

## 1. Overview
The goal is to identify which customers are likely to stop using the service (churn) by analyzing demographic, usage, and contract data.

## 2. What I Did
- Cleaned and explored the data (EDA)
- Trained and compared Logistic Regression and Random Forest models
- Evaluated performance using accuracy and F1 score
- Saved trained models and preprocessing objects for deployment

## 3. Results
| Model | Accuracy | F1 |
|:------|----------:|--:|
| Logistic Regression | 0.799 | 0.592 |
| Random Forest | 0.797 | 0.571 |

*(These results are from my training notebook and can change after tuning.)*

## 4. Tech Stack
- Python  
- pandas, numpy, scikit-learn, seaborn, matplotlib  
- joblib for saving models  
- FastAPI and Docker planned for deployment

## 5. Project Structure
ml-churn-prediction/
├── data/           # Dataset (churn.csv)
├── models/         # Saved models and preprocessing files
├── notebooks/      # Training and analysis notebooks
├── src/            # Code for the upcoming API
├── tests/          # Will include unit tests later
└── requirements.txt
## 6. Next Steps
- Build an API with FastAPI to serve the model  
- Add a database (PostgreSQL) to log predictions  
- Containerize everything with Docker for deployment  