# High Frenquency Checks for WFP Food Security Assessments - ROADMAP

## v0.1.0 Stable


### Checks
- [X] FCS
- [X] rCSI
- [X] HDDS
- [X] Demographics
- [X] Food Expenditures
- [X] Non-food Expenditures
- [X] LCS
- [ ] HHS
- [ ] Average daily completion by enumerator
-	Flag invalid survey with interview less than 5 minutes
-	Flag short survey (<45 minutes)
-	Flag long survey (>150 minutes)
- [ ] Total survey completed
- [ ] Total survey completed by admin region (see sample size)
- [ ] Enumerator completion (overall number by day and scatter hours of the day if real-time submission is possible)

### Logbook 
- [ ] Create issue log with format ```uuid | issue | action | old.value | new.value```

### Data connector
- [X] Get data from DataBridges

### Deployment
- [ ] Run code on a schedule from HPC
- [ ] Output report in Tableau

## v.2.0
- [ ] Configuration in settings
- [ ] Revamp output report in Tableau
- [ ] 


## Future releases

- [X] Make config.py something usable with no knowledge of Python (CSV input)
- [ ] Make the output less ugly
- [ ] Optimize code (e.g. not running everything on all the dataset, but just on the data that have been collected the day before)
