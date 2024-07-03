# High Frenquency Checks for WFP Food Security Assessments

This repository supports WFP Country Offices in checking the quality of the data collected in needs assessment surveys. 

## Features

Indicator Modules: The package includes modules for calculating and validating various indicators commonly used in survey data analysis, such as Food Consumption Score (FCS), Reduced Coping Strategy Index (rCSI), Household Dietary Diversity Score (HDDS), Household Expenditure, Livelihoods Coping Strategies, Housing conditions, and Demographic information.
Configurable Checks: Each indicator module includes a set of configurable checks to identify potential errors or inconsistencies in the data. These checks can be customized based on the specific requirements of the survey or data collection process.
Flagging System: The package implements a flagging system to mark records with potential issues. Flags are generated based on the configured checks, and a narrative description is provided for each flagged record, facilitating review and follow-up.
Master Sheet Generation: The package can generate a master sheet that consolidates the original data with the calculated indicators and flags. This master sheet can be used for further review and analysis.
Data Loading: The package includes utilities for loading data from various sources, such as Excel files or databases.

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
- [Ali Assi](https://github.com/AssiALi16)
- [Alessandra Gherardelli](https://github.com/AlexGherardelli)

## License

This project is licensed under the Affero GPL v3.0 license.
