# High Frenquency Checks for WFP Food Security Assessments - ROADMAP

## v0.1.0 Stable

### Indicator checks
- [X] FCS
- [X] rCSI
- [X] HDDS
- [X] Demographics
- [X] Food Expenditures
- [X] Non-food Expenditures
- [ ] LCS
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
- [ ] Create issue log with format ```uuid | issue | action | old.value | new.value```

### Data connector
- [X] Get data from DataBridges
- [ ] Parse data as int 

### Deployment
- [ ] Run code on a schedule from HPC
- [ ] Output report in Sharepoint

## Future releases 
- [ ] Additional checks
- [ ] Make config.py something usable with no knowledge of Python (CSV input)
- [ ] Optimize output (e.g. Excel vs CSV vs other format)
- [ ] Dashboard
- [ ] Optimize code (e.g. not running everything on all the dataset, but just on the data that have been collected the day before)
