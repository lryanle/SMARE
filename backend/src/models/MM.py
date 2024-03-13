# Importing the M3_riskscores and M4_riskscores functions from their respective modules
import M3
import M4
import pandas as pd


def model_manager():
    # Calling M3_riskscores function to get results from Model M3
    m3_results = M3.M3_riskscores()
    # Calling M4_riskscores function to get results from Model M4
    m4_results = M4.M4_riskscores()
    # Merging the results from both models based on a common identifier, if applicable
    merged_results = pd.merge(m3_results, m4_results, on='_id', how='inner')
    # Perform any additional data processing or calculations to derive the final risk score
    final_risk_score = (merged_results['risk_score_M3'] + merged_results['risk_score_M4_y']) / 2
    # Add the final risk score to the merged results DataFrame
    merged_results['final_risk_score'] = final_risk_score

    # Extracting the 'id' column and 'final_risk_score' column as a list of tuples
    output = merged_results[['_id', 'final_risk_score']]
    # Save the output to a CSV file
    output.to_csv('final_risk_scores.csv', index=False)

    # Returning the list of tuples containing 'id' and 'final_risk_score'
    return output.values.tolist()


# Call the model_manager function to execute the model management process
final_results = model_manager()

# Print the final results
print(final_results)
