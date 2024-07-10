# High Frenquency Checks for WFP Food Security Assessments - ROADMAP


This document outlines the high-level roadmap and future plans for the project.


## Current Status
 The project is currently in its initial development phase. The core data quality checks for main food security indicators have been implemented. The current version is 0.1.0, released on 2 July 2024. 

## Upcoming Milestones (v1.0.0)
### Milestone 1: Improved reporting outputs (Target Release: 0.2.0)
- [X] Add start date to mastersheet report (0.2.1)
- [X] Change database to Household Processed (0.2.1)
- [ ] Documentation on data quality checks and module usage
- [ ] Enumerator data labels
- [ ] Quotas

### Milestone 2: Additional data quality checks (Target Release: 0.3.0)
- [ ] Additional data quality checks
  - [ ] HHS
  - [ ] Total survey completed
  - [ ] Total survey completed by admin region (see sample size)
  - [ ] Enumerator completion

### Milestone 3: Configurations (Target Release 0.4.0)
- [ ] db_config fields available in MoDa configuration
- [ ] Country-specific configurations available through MoDa Form
- [ ] Configuration in settings folder (as separate module)
- [ ] Read from official instead of full for everything that's not survey 
- [ ] Package it as module (PyPI)

## Future versions (v2.0.0)
- [ ] Optimize code 
  - [ ] Incremental loading to database
  - [ ] Incremental data quality  checks (i.e. only on the day before)
- [ ] Logic for handling expenditure amount (i.e. amount only asked if the HH reported) and rural/urban LCS

### Long-term Goals (v3.0.0)
- Integration with SHAPES CoreEngine, running the pipeline in the cloud
- Expand country office adoption

## Feedback and Suggestions
We value your feedback and suggestions! If you have any ideas, feature requests, or issues to report, please submit them through our [issue tracker](https://github.com/WFP-VAM/DataQualityChecks/issues). 



