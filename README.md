# High Frenquency Checks for WFP Food Security Assessments

This repository supports WFP Country Offices in checking the quality of the data collected in needs assessment surveys. 

## Installation

To use the data quality functionalities, follow these steps:

1. Clone the repository: `git clone https://github.com/your-repo/fcs-checks.git`
2. Install the required dependencies: `pip install -r requirements.txt`


# Usage

To run the data checks on your data, follow these steps:

1. Prepare your data in a CSV or Excel file format.
2. Update the `config.py` file with the appropriate file paths and configurations.
3. Run the `main.py` script: `python main.py`

The script will generate a report in the `Reports` directory, containing the FCS checks and flags for each household in the dataset.


## Data Quality checks
The reposity checks both outcome indicator data quality  and enumerator performance. 

### Food Consumption score

The FCS checks follow a hierarchical structure, with sequential and independent checks applied to the data. The decision logic is illustrated in the following diagram:

<div style="text-align:center">
    <iframe src="Hierarchies/FCS.drawio.html" style="width:100%; height:600px; border:none;"></iframe>
</div>

The diagram highlights the following key aspects:

- **Sequential Checks**: The flags for missing values and erroneous values are sequential. If one of these flags is triggered, the subsequent conditions are not checked.
- **Independent Checks**: The flags for identical values, low and high FCS scores, as well as low staple consumption, are checked independently and are not mutually exclusive.
- **Flag Values**: In the generated report, each flag can be either equal to 0 (Condition Not Met), 1 (Condition Met), or NONE (Check did not execute).

This structured approach ensures that data quality issues are systematically identified and flagged, facilitating effective data management and analysis.

## Contributing

Contributions to this project are welcome. If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

## License

This project is licensed under the Affero GPL v3.0 license.