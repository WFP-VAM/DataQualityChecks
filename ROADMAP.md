# High Frenquency Checks for WFP Food Security Assessments - ROADMAP


This document outlines the high-level roadmap and future plans for the project.

## Vision

<!-- To create a powerful and user-friendly application that streamlines task management and collaboration for teams of all sizes, enabling them to work more efficiently and effectively. -->

## Current Status

<!-- The project is currently in its initial development phase. The core task management features have been implemented, including the ability to create, assign, and track tasks, as well as basic project management capabilities. The current version is 0.1.0, released on May 1, 2023. -->

## Upcoming Milestones

<!-- ### Milestone 1: Enhanced Collaboration Features (Target Release: 0.2.0, 10 July 2024)

- [ ] Implement real-time team chat and messaging
- [ ] Add file sharing and document collaboration capabilities
- [ ] Integrate video conferencing for virtual meetings

### Milestone 2: Reporting and Analytics (Target Release: 0.3.0, November 1, 2023)

- [ ] Develop customizable reporting and dashboard features
- [ ] Implement project analytics and performance tracking
- [ ] Add resource management and capacity planning tools

### Milestone 3: Mobile App and Integrations (Target Release: 0.4.0, February 1, 2024)

- [ ] Develop a native mobile app for iOS and Android
- [ ] Integrate with popular productivity tools and services
- [ ] Implement advanced security and access control features


## v0.1.0
### Checks
- [X] FCS
- [X] rCSI
- [X] HDDS
- [X] Demographics
- [X] Food Expenditures
- [X] Non-food Expenditures
- [X] LCS

### Logbook 
- [X ] Create issue log with format ```uuid | issue | action | old.value | new.value```

### Data connector
- [X] Get data from DataBridges

### Deployment
- [X] Run code on a schedule from HPC
- [X] Output report in Tableau

### Next release (v0.2.0)
- [ ]  Add additional checks
  - [ ] HHS
  - [ ] Average daily completion by enumerator
  - [ ] Total survey completed
  - [ ] 
  - [ ] Total survey completed by admin region (see sample size)
  - [ ] Enumerator completion (overall number by day and scatter hours of the day if real-time submission is possible)
- [ ] Make config.py something usable with no knowledge of Python (CSV input)
- [ ] Revamp output report in Tableau
  - [ ] Add start date of survey
  - [ ] All HH issues
  - [ ] Add value labels to the output
- [ ] Flag more detailed

### Future versions
- [ ] Configuration in settings
- [ ] Optimize code (e.g. not running everything on all the dataset, but just on the data that have been collected the day before)
- [ ] Logic for handling expenditure amount (i.e. amount only asked if the HH reported) and rural/urban LCS
- [ ] Read from official instead of full for everything that's not survey 

# Long term  plans
- [ ] Integration with CoreEngine





## Long-term Goals

- Explore machine learning and artificial intelligence capabilities to enhance task automation and project planning
- Develop industry-specific solutions and vertical integrations
- Expand to support enterprise-level deployments and scalability

## Contributing

We welcome contributions from the community! Please refer to our [Contributing Guidelines](CONTRIBUTING.md) for more information on how to get involved.

## Feedback and Suggestions

We value your feedback and suggestions! If you have any ideas, feature requests, or issues to report, please submit them through our [issue tracker](https://github.com/project/issues) or join our [community forum](https://community.project.com) to discuss with other users and contributors. -->



## Enumerators checks

- uuid
- EnuName
- Admin1/Admin2/Admin3
- Labels for admin areas
- condition for completed
- Quota by Admin 2
- GPS