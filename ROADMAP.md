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




