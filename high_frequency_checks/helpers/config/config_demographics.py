male_cols = ['HHSize01M',
             'HHSize24M',
             'HHSize511M',
             'HHSize1217M',
             'HHSize1859M',
             'HHSize60AboveM']

female_cols = ['HHSize01F',
               'HHSize24F',
               'HHSize511F',
               'HHSize1217F',
               'HHSize1859F',
               'HHSize60AboveF']

adult_cols = ['HHSize1859M',
              'HHSize60AboveM',
              'HHSize1859F',
              'HHSize60AboveF']

demo_flags = {
    'Flag_Demo_High_HHSize': "The Household Size is very high (More than 30)",
    'Flag_Demo_Inconsistent_HHSize': "Sum of Males and Females does not match the household size",
    'Flag_Demo_No_Adults': "There are no adults in the household",
    'Flag_Demo_plw': "Number of pregnant and lactating females is higher than females aged 12-59"
}
