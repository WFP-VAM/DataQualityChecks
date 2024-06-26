# High Frenquency Checks for WFP Food Security Assessments

This repository supports WFP Country Offices in checking the quality of the data collected in needs assessment surveys. 


## Features

- **Food Consumption Score (FCS) Checks**: Performs a series of checks on the FCS data, including missing values, erroneous values, abnormal patterns (e.g., all zeros, all sevens, identical values), low staple consumption, and low/high FCS scores.
- **Reduced Coping Strategy Index (rCSI) Checks**: Validates the rCSI data by checking for missing values, erroneous values, and high rCSI scores.
- **Demographic Checks**: Checks for erroneous values in age groups and flags households with extremely large household sizes.
- **Household Dietary Diversity Score (HDDS) Checks**: Validates the HDDS data by checking for missing values and erroneous values.
- **Food Expenditure Checks**: Checks for erroneous values in food expenditure data for 7 days, 1 month, and 6 months.
- **Enumerator Performance Evaluation**: Generates reports summarizing the data quality issues at the enumerator level, including the total number of records and error percentages.
- **Mastersheet Generation**: Consolidates all indicator checks into a single mastersheet, providing an overview of data quality across all indicators.

## Installation

To use the data quality functionalities, follow these steps:

1. Clone the repository: `git clone https://github.com/your-repo/fcs-checks.git`
2. Install the required dependencies: `pip install -r requirements.txt`

## Usage

To run the data checks on your data, follow these steps:

1. Get your DataBridges ID or prepare your data in a CSV of Excel file format
2. Update the `config.py` file to contextualize the data quality checks (e.g. thresholds for a suspiciously low/high FCS).
3. Run the `HFC.py` script: `python HFC.py`

The script will generate a report in the `reports` directory, containing the FCS checks and flags for each household in the dataset.

## Data Quality checks
The reposity checks both outcome indicator data quality  and enumerator performance. 

### Food Consumption score
The FCS checks follow a hierarchical structure, with sequential and independent checks applied to the data. The decision logic is available in ```docs```.

The diagram highlights the following key aspects:

- **Sequential Checks**: The flags for missing values and erroneous values are sequential. If one of these flags is triggered, the subsequent conditions are not checked.
- **Independent Checks**: The flags for identical values, low and high FCS scores, as well as low staple consumption, are checked independently and are not mutually exclusive.
- **Flag Values**: In the generated report, each flag can be either equal to 0 (Condition Not Met), 1 (Condition Met), or NONE (Check did not execute).

This structured approach ensures that data quality issues are systematically identified and flagged, facilitating effective data management and analysis.

### rCSI
Documentation to be added

### Demographics
Documentation to be added

### HHDS
Documentation to be added


## Contributing

Contributions to this project are welcome. If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.


## Authors
- (Ali Assi)[https://github.com/AssiALi16]
- (Alessandra Gherardelli)[[https://github.com/AlexGherardelli]]

## License

This project is licensed under the Affero GPL v3.0 license.