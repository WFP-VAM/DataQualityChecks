# High Frenquency Checks for WFP Food Security Assessments - ROADMAP


This document outlines the high-level roadmap and future plans for the project.


## Current Status
 The project is currently in its initial development phase. The core data quality checks for main food security indicators have been implemented. The current version is 0.1.0, released on 2 July 2024. 

## Upcoming Milestones

### Milestone 1: Improved reporting outputs (Target Release: 0.2.0, 8 July 2024)

- [ ] Add start date to mastersheet report
- [ ] Enumerator performance indicators
  - [ ] Average daily completion by enumerator
  - [ ] Total survey completed
  - [ ] Total survey completed by admin region (see sample size)
  - [ ] Enumerator completion (overall number by day and scatter hours of the day if real-time submission is possible)
- [ ] Documentation on data quality checks and module usage
- [ ] Change database to Household Processed

### Milestone 2: Additional data qualit y checks (Target Release: 0.3.0, 12 July 2024)
- [ ] Additional data quality checks
  - [ ] HHS
- [ ] Country-specific configurations available through MoDa Form
  - [ ] db_config fields available in MoDa configuration

### Future versions 
- [ ] Configuration in settings folder (as separate module)
- [ ] Optimize code (e.g. not running everything on all the dataset, but just on the data that have been collected the day before)
- [ ] Logic for handling expenditure amount (i.e. amount only asked if the HH reported) and rural/urban LCS
- [ ] Read from official instead of full for everything that's not survey 

## Long-term Goals

- Integration with SHAPES CoreEngine, running the pipeline in 
- Expand country office adoption

## Feedback and Suggestions

We value your feedback and suggestions! If you have any ideas, feature requests, or issues to report, please submit them through our [issue tracker](https://github.com/WFP-VAM/DataQualityChecks/issues). 



