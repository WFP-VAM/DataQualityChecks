# ROADMAP

## To Do

- [ ] FCS 
- [ ] rCSI
- [ ] Demographics
- [ ] HDDS
- [ ] HHS
- [ ] LCS-FS
- [ ] Expenditures
- [ ] Enumerator checks

## Refactoring structure

```
high_frequency_checks/
├── __init__.py
├── utils.py # common module utils to export report
├── indicator_checks/
│   ├── __init__.py
│   ├── rci_checks # rCSI checks
│   ├── fcs_checks.py # food consumption score checks
│   └── base.py # base class for all indicator checks
├── enumerator_checks/
│   ├── __init__.py
│   ├── survey_completion.py
main.py # import data and runs checks, with parameters
README.md # user level documentation
LICENSE.md
ROADMAP.md # To Do list

```

```
ou can already appreciate, I'm just waiting to integrate the information on :
1. Community level (Health area) level 4;
2. Name of team supervisor ( or ID)
3. Name of Team Leader (or ID)
3. Name of interviewer (or ID).
``


c:\Users\alessandra.gherardel\OneDrive - World Food Programme\Documents\02. Information Management\02.Scripts\FSA_HFC\indicators\demographics.py:64: FutureWarning: A value is trying to be set on a copy of a DataFrame or Series through chained assignment using an inplace method.
The behavior will change in pandas 3.0. This inplace method will never work because the intermediate object on which we are setting values always behaves as a 
copy.

For example, when doing 'df[col].method(value, inplace=True)', try using 'df.method({col: value}, inplace=True)' or df[col] = df[col].method(value) instead, to perform the operation inplace on the original object.
