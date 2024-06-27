# High Frenquency Checks for WFP Food Security Assessments - ROADMAP

## v0.1.0 Stable


### Indicator checks
- [X] FCS
- [X] rCSI
- [X] HDDS
  - [ ] Non-sequential check
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
- [ ] 
-	Enumerator completion (overall number by day and scatter hours of the day if real-time submission is possible)
-	Flag invalid survey with interview less than 5 minutes
-	Flag short survey (<45 minutes)
-	Flag long survey (>150 minutes)
-	nombre_autre > 5
-	nombre_pnpr > 5
-	nombre_nsp > 

### Logbook 
- [ ] Create issue log with format ```uuid | issue | action | old.value | new.value```

### Data connector
- [ ] Get data from DataBridges

### Deployment
- [ ] Run code on a schedule from HPC
- [ ] Output report in Sharepoint

## Future releases

- [ ] Dashboard (TBC)
- [ ] Make config.py something usable with no knowledge of Python (CSV input)
- [ ] Make the output less ugly
- [ ] Optimize code (e.g. not running everything on all the dataset, but just on the data that have been collected the day before)
