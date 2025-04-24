from sklearn.linear_model import LinearRegression
import numpy as np

sample_x = np.array([[1.2, 2.3, 3.1],
              [2.0, 3.1, 4.0],
              [3.5, 1.2, 2.4],
              [4.8, 3.8, 5.7],
              [5.1, 2.2, 3.3],
              [6.2, 2.9, 4.6],
              [7.3, 3.1, 5.8],
              [8.4, 4.2, 6.7]])
sample_y = np.array([6.4, 8.3, 7.2, 12.5, 9.1, 10.0, 12.2, 14.5])

model = LinearRegression()
model.fit(sample_x, sample_y)

print("Coefficients:", model.coef_)
print("Intercept:", model.intercept_)

X_new = np.array([[5.0, 3.0, 4.0]])
y_pred = model.predict(X_new)
print("Prediction for input [5.0, 3.0, 4.0]:", y_pred)
