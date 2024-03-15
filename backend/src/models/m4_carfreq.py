import MOVETOCLEAN_car_data


def m4_riskscores():
    # VEHICLE FREQUENCY MODEL
    cars_dff = MOVETOCLEAN_car_data.cars

    # Function to analyze frequency of vehicle models and calculate risk score
    def calculate_risk_score(row, model_frequency, max_frequency):
        # Normalize model frequency
        risk_score = model_frequency[row["model"]] / max_frequency
        return round(risk_score, 4)  # Round up to 4 decimal places

    # Analyze frequency of vehicle models
    model_frequency = cars_dff["model"].value_counts()
    max_frequency = model_frequency.max()

    # Calculate risk score based on frequency for each row
    cars_dff["risk_score_M4"] = cars_dff.apply(
        lambda row: calculate_risk_score(row, model_frequency, max_frequency), axis=1
    )

    return cars_dff
