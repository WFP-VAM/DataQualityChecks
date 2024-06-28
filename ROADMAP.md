# High Frenquency Checks for WFP Food Security Assessments - ROADMAP

## v0.1.0 (Enumerator Training)

### Indicator checks
- [X] FCS
- [X] rCSI
- [X] HDDS
- [X] Demographics
- [X] Food Expenditures
- [X] Non-food Expenditures
- [X] LCS

### Data connector
- [X] Get data from DataBridges
- [ ] Parse data as int 

### Visualization
- [ ] Output master report in DB
- [ ] Output master report in Tableau

## v.0.2.0
### Indicator checks
- [ ] HHS

### Enumerator performance
- [ ] Total survey completed
- [ ] Total survey completed by admin region (see sample size)
- [ ] Average daily completion by enumerator
- [ ] Survey duration too short
- [ ] Survey duration too long
- [ ] Flag invalid survey with interview less than 5 minutes
- [ ] Flag short survey 
- [ ] Flag long survey 

### Logbook 
- [ ] Create issue log in Excel

### Deployment
- [ ] Run code on a schedule from HPC

## Future releases (1.0.0)
- [ ] Additional checks
- [ ] Make config.py something usable with no knowledge of Python (CSV input)
- [ ] Optimize output (e.g. Excel vs CSV vs other format)
- [ ] Dashboard
- [ ] Optimize code (e.g. not running everything on all the dataset, but just on the data that have been collected the day before)
- [ ] Endpoint through Core Engine


## Issues
- Running wrong CO 
- Full vs Base
- Where to export the report
  - DB -> Tableau
