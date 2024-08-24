# FYP Supervised by BoA


This is the github repo for the MSc Summer Project with supervisors from BoA.


## Project Description
    This thesis critically examines the impact of incorporating correlations between output variables—specifically wind speed and total precipitation—on improving hurricane forecasting accuracy. Traditional machine learning approaches often predict these variables independently without explicit acknowledgment of inter-variable dependencies, or jointly with implicit, unquantified correlations. This research introduces a structured methodology using Multi-Output Gaussian Processes (MOGP) integrated with the Intrinsic Coregionalization Model (ICM) to explicitly model and leverage these correlations. By conducting a comparative analysis with Single-Output Gaussian Processes (SOGP), which treat outputs independently, and standard MOGP models that implicitly handle output interactions, this study uniquely isolates the effect of explicitly modeled correlations on predictive accuracy. Results across multiple hurricanes demonstrate that explicitly considering output correlations through MOGP with ICM leads to statistically significant improvements in forecast precision, as evidenced by lower Mean Squared Error (MSE) and Mean Absolute Percentage Error (MAPE). This research not only substantiates the hypothesis that explicit modeling of output correlations enhances forecasting but also sets a benchmark for future studies to quantify the benefits of correlation-aware modeling approaches in meteorology and beyond. These findings offer profound implications for advancing meteorological predictions, supporting enhanced disaster preparedness and response strategies.

## File Structure

- requirements.txt: contains the required libraries for the project. please run `pip install -r requirements.txt` to install the required libraries.
- data_extraction.py: contains the code for extracting the hourly data using the csv files from the Climate Data Store website.
- daily_data_extraction.py: contains the code for extracting the daily data using the csv files from the Climate Data Store website.
- EDA_CDS.ipynb: contains the exploratory data analysis for the hourly data along with the code for data reduction and correlation analysis.
- Events.csv: contains the list of hurricanes used in the project.
- mv_uv_add_ws.py: contains the code for adding the wind speed (calculated from the u/v components fo the windspeed, then removed the u/v components) to the hourly data.
- pred_utils.py: contains the utility functions for the project.
- pred.ipynb: contains the code for the prediction using the hourly data. The code uses the MOGP with ICM model for the prediction.