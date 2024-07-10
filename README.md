# High Frenquency Checks for WFP Needs Assessments

This repository supports WFP Country Offices in checking the quality of the data collected in needs assessment surveys. 

## Features

- **Indicator Modules:** The package includes modules for calculating and validating various indicators commonly used in survey data analysis, such as Food Consumption Score (FCS), Reduced Coping Strategy Index (rCSI), Household Dietary Diversity Score (HDDS), Household Expenditure, Livelihoods Coping Strategies, Housing conditions, and Demographic information.
- **Configurable Checks:** Each indicator module includes a set of configurable checks to identify potential errors or inconsistencies in the data. These checks can be customized based on the specific requirements of the survey or data collection process.
- **Flagging System:** The package implements a flagging system to mark records with potential issues. Flags are generated based on the configured checks, and a narrative description is provided for each flagged record, facilitating review and follow-up.
- **Summary report:** The package can generate a summary report (mastersheet) that consolidates the original data with the calculated indicators and flags. This master sheet can be used for further review and analysis.
- **Data Loading:** The package includes utilities for loading data from various sources, such as Excel files or databases.

## Installation
> Note: This package is still under development and available for testing and contribution. Further guidance on installation and usage will be provided in the near future.

To install the package, follow the steps below:

1. Clone the repository: `git clone https://github.com/your-repo/fcs-checks.git`
2. Install the required dependencies: `pip install -r requirements.txt`


## Data Quality checks
The reposity checks data quality for the main food security outcome indicators used in WFP Needs Assessments. 

Issues for each indicators are flagged through a hierarchical structure of **sequential** and **independent** checks.

The checks are organized in the following way:
- **Sequential Checks**: The flags for missing values and erroneous values are sequential. If one of these flags is triggered, the subsequent conditions are not checked. 
  - For categorical variables (e.g. housing options), a value is marked as erroneous if it is not consistent with the WFP Codebook. 
  - For numerical variables (e.g. food groups) a value is marked as erroneous if it is not within the acceptable range.
- **Independent Checks**: If the indicator has no missing or erronous values, custom indipendent checks are executed for each indicator. 
- **Flag Values**: In the generated reports, each flag can be either equal to 0 (Condition Not Met), 1 (Condition Met), or NONE (Check did not execute).

### Demographic module
The following graph shows the decision logic of both sequential and independent checsk:

![Demographics Checks](docs/demographic.png)

The **indipendent checks** for this indicators are:
- missing values for pregnant and breastfeeding women
- number of pregnant and breastfeeding women exceeds the number of women aged 12-59
- household size is very high (default: 30)
- number of males and females in the household does not match household size
- no adults in the household (default: adult > 15 age)

### Food Consumption Score (FCS)
The following graph shows the decision logic of both sequential and independent checsk:

![FCS Checks](docs/FCS.jpg)

The **indipendent checks** for this indicators are:
- identical values
- low FCS score (default: <10) 
- high FCS score (default: >100)
- low staple consumption (default: <= 4 days)

### Reduced Coping Strategy Index (rCSI)
The following graph shows the decision logic of both sequential and independent checsk:

![rCSI Checks](docs/rCSI.jpg)

The **indipendent checks** for this indicators are:
- identical values
- poor FCS with no coping (default: rCSI == 0)
- adequate FCS with high coping (default: rCSI > 50)
- adults reduced their meail intake so children could eat in households with no children

### Food Expenditures

#### 7-day recall period

#### 1 month recall period

### Non-food Expenditures

#### 7-day recall period

#### 1 month recall period


### LCS-FS
TODO 

#### LCS-FS-rural
TODO 

### LCS-EN
TODO 

### Housing
TODO


### Timing
Documentation to be added

### Household Diet Diversity Score (HDDS)
Indicator check coming soon

### HHS
Indicator check coming soon

## Contextualization
Some data quality checks can be contextualized based on the country context (e.g. abnormally high/low food expenditure). WFP Country Offices can insert the custom thresholds for the customizable indicators in the configuration files contained in the ```config``` folder. 


## Contributing

Contributions to this project are welcome. If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.


## Authors
- [Ali Assi](https://github.com/AssiALi16)
- [Alessandra Gherardelli](https://github.com/AlexGherardelli)

## License

This project is licensed under the Affero GPL v3.0 license.
