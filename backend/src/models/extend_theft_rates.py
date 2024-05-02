import pandas as pd
from sklearn.linear_model import LinearRegression
import json
import numpy as np

with open('n_nhtsa_theft_rates.json', 'r') as file:
    data = json.load(file)

df = pd.DataFrame(list(data.items()), columns=['model_year', 'theft_rate'])
df['theft_rate'] = pd.to_numeric(df['theft_rate'])
df['year'] = df['model_year'].apply(lambda x: int(x.split(' ')[-1]))
df['model'] = df['model_year'].apply(lambda x: ' '.join(x.split(' ')[:-1]))

prediction_years = range(2015, 2025)
predictions = {}

for model in df['model'].unique():
    model_data = df[df['model'] == model]
    X = model_data[['year']]
    y = model_data['theft_rate']
    model_lr = LinearRegression()
    model_lr.fit(X, y)

    future_X = pd.DataFrame(prediction_years, columns=['year'])
    future_y = model_lr.predict(future_X)

    future_y = np.maximum(0, future_y)

    for year, rate in zip(prediction_years, future_y):
        key = f"{model} {year}"
        predictions[key] = f"{rate:.2f}"

predictions_json = json.dumps(predictions, indent=4)

with open('predicted_theft_rates_2015_2024.json', 'w') as f:
    f.write(predictions_json)

print("Predictions for 2015-2024 have been calculated and saved, ensuring no negative values.")
