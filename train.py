import json, numpy as np
from sklearn.linear_model import Ridge
from sklearn.model_selection import cross_val_predict, KFold
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

rng = np.random.default_rng(42)
n = 500
study = rng.uniform(0, 12, n)
attend = rng.uniform(40, 100, n)
sleep = rng.uniform(4, 10, n)
prev = rng.uniform(0, 100, n)
assign = rng.integers(0, 11, n).astype(float)
# True generative score: study matters most, attendance + prev next
y_true = (4.2*study + 0.35*attend + 2.0*sleep + 0.28*prev + 1.5*assign
          - 0.18*study**2 + 0.02*study*prev)
y = np.clip(y_true + rng.normal(0, 5, n), 0, 100)
X = np.column_stack([study, attend, sleep, prev, assign])
names = ["study_hours","attendance_pct","sleep_hours","prev_score","assignments_done"]
mu, sd = X.mean(0), X.std(0)
Xs = (X - mu) / sd
model = Ridge(alpha=1.0).fit(Xs, y)
kf = KFold(5, shuffle=True, random_state=42)
pred_cv = cross_val_predict(Ridge(alpha=1.0), Xs, y, cv=kf)
mae = float(mean_absolute_error(y, pred_cv))
rmse = float(np.sqrt(mean_squared_error(y, pred_cv)))
r2 = float(r2_score(y, pred_cv))
baseline_mae = float(mean_absolute_error(y, np.full_like(y, y.mean())))
print(f"CV MAE={mae:.2f} RMSE={rmse:.2f} R2={r2:.3f} baseline_MAE={baseline_mae:.2f}")
print("coef", model.coef_, "intercept", model.intercept_)
print("means", mu, "stds", sd)
model_json = {"features": names, "means": mu.tolist(), "stds": sd.tolist(),
              "coef": model.coef_.tolist(), "intercept": float(model.intercept_),
              "metrics": {"cv_mae": mae, "cv_rmse": rmse, "cv_r2": r2, "baseline_mae": baseline_mae, "n": n}}
with open("model.json","w") as f: json.dump(model_json, f, indent=1)
# JS parity: replicate prediction in python formula for sample inputs
def predict(v):
    z = (np.array(v)-mu)/sd
    return float(model.intercept_ + z @ model.coef_)
samples = [[6,85,7,70,8],[2,60,5,40,3],[10,95,8,90,10],[0,50,4,20,0],[4,75,6,55,5]]
for s in samples: print(s, round(predict(s),2))
