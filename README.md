m

This repository supports WFP Country Offices in checking the quality of the data collected in needs assessment surveys. 


> This package is under development, and we expect to release new versions and bug fixes frequently. 

## Features
This package checks data quality for the main indicators used in WFP needs assessments:

- **Food Consumption Score (FCS) Checks**:
  - Flag missing values in food groups
  - Flag all groups are identical
  - Flag very low (FCS <= 10) or very high (FCS >= 90/100) 
  - Flag low staple consumption
  - Low FCS with no coping (rCSI = 0)
  - High FCS with rCSI > 50
  - <0 or >7 score for all food groups
- **Reduced Coping Strategy Index (rCSI) Checks**:
  -  Missing values
  -  Out-of-range values
  -  High food-based coping (rCSI) with high consumption (FCS)
- **Demographic Checks**: 
  - Checks for erroneous values
  - Flags households with extremely large household sizes.
- **Household Dietary Diversity Score (HDDS) Checks**: 
  - Missing values
  - Out-of-range values
  - Inconsistencies with FCS (FCS == 7 -> HHDS == 0; FCS == 0  -> HHDS == 1)
- **Food Expenditure Checks**: Checks for erroneous values in food expenditure data for 7 days, 1 month, and 6 months.
- **Enumerator Performance Evaluation**: Generates reports summarizing the data quality issues at the enumerator level, including the total number of records and error percentages.
- **Mastersheet Generation**: Consolidates all indicator checks into a single mastersheet, providing an overview of data quality across all indicators.

The package is customizable by each Country Office by creating contextual configurations in the ```config.py` file.

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
