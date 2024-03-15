# Importing the M3_riskscores and M4_riskscores functions from their respective modules
from m3_kbbprice import m3_riskscores
from m4_carfreq import m4_riskscores
import pandas as pd

# todo: pass in data from mongo through each function
# todo: calculate post-weight-product scores here, and not in each individual function.
def model_manager():
    m3_results = m3_riskscores()
    m4_results = m4_riskscores()

    # Merging the results from both models based on a common identifier, if applicable
    merged_results = pd.merge(m3_results, m4_results, on='_id', how='inner', validate='one_to_one')
    # Perform any additional data processing or calculations to derive the final risk score
    final_risk_score = min(100,merged_results['risk_score_M3'] + merged_results['risk_score_M4_y'])
    # Add the final risk score to the merged results DataFrame
    merged_results['final_risk_score'] = final_risk_score

    # Extracting the 'id' column and 'final_risk_score' column as a list of tuples
    output = merged_results[['_id', 'final_risk_score']]
    # Save the output to a CSV file
    output.to_csv('final_risk_scores.csv', index=False)

    # Returning the list of tuples containing 'id' and 'final_risk_score'
    return output.values.tolist()

print(model_manager())
