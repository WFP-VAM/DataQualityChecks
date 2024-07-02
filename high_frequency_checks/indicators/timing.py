import pandas as pd
import pytz
import logging
from high_frequency_checks.helpers.base_indicator import BaseIndicator

class Timing(BaseIndicator):

    flags = {
        'Flag_Timing_Invalid_Duration': "The survey duration is invalid",
        'Flag_Timing_Short_Duration': "The survey duration is short",
        'Flag_Timing_Long_Duration': "The survey duration is long",
        'Flag_Timing_Abnormal_Start_Period': "The survey started in an abnormal period of the day"
    }

    def __init__(self, df, base_cols, review_cols, standard_config, configurable_config, flags):
        super().__init__(df, base_cols, review_cols, standard_config, configurable_config, flags)
        self.logger = logging.getLogger(__name__)
        self.short_survey = self.configurable_config.get('short_survey')
        self.long_survey = self.configurable_config.get('long_survey')
        self.utc = self.configurable_config.get('utc')
        self.time_thresholds = self.configurable_config.get('time_thresholds')
        self.abnormal_start_time = self.configurable_config.get('abnormal_period')

    def _process_specific(self):
        self.logger.info("Performing specific processing for SurveyDuration indicator")
        self.transform_correct_timezone()
        self.calculate_duration_mins()
        self.categorize_start_time()
        self.check_invalid_duration()
        self.check_short_duration()
        self.check_long_duration()
        self.check_abnormal_start_period()

    def transform_correct_timezone(self):
        correct_tz = pytz.FixedOffset(self.utc * 60)
        self.df['start'] = pd.to_datetime(self.df['start']).dt.tz_convert(correct_tz).dt.tz_localize(None)
        self.df['end'] = pd.to_datetime(self.df['end']).dt.tz_convert(correct_tz).dt.tz_localize(None)

    def calculate_duration_mins(self):
        self.logger.info("Calculating Survey Duration")
        try:
            self.df['Duration_Mins'] = ((self.df['end'] - self.df['start']).dt.total_seconds() / 60).round().astype(int)
            self.logger.info("Survey Duration calculated successfully")
        except Exception as e:
            self.logger.error(f"Error calculating Survey Duration: {e}")

    def categorize_start_time(self):
        self.logger.info("Categorizing Start Time")
        def get_period(hour):
            for period, times in self.time_thresholds.items():
                try:
                    start_hour = int(times['start'])
                    end_hour = int(times['end'])
                    if start_hour <= hour < end_hour:
                        return period
                except ValueError as ve:
                    self.logger.error(f"Error in time threshold for period '{period}': {ve}")
            return 'Unknown'
        try:
            self.df['Start_Period'] = self.df['start'].dt.hour.apply(get_period)
            self.logger.info("Start Time Categorized Successfully")
        except Exception as e:
            self.logger.error(f"Error Categorizing Start Time: {e}") 

    def check_invalid_duration(self):
        self.logger.info("Checking for invalid survey durations")
        try:
            self.df['Flag_Timing_Invalid_Duration'] = (self.df['Duration_Mins'] < 5).astype(int)
            self.logger.info("Generated invalid survey duration flag for Timing")
        except Exception as e:
            self.logger.error(f"Error checking invalid durations for Timing: {e}")

    def check_short_duration(self):
        self.logger.info("Checking for short survey durations")
        try:
            self.df['Flag_Timing_Short_Duration'] = (self.df['Duration_Mins'] < self.short_survey).astype(int)
            self.logger.info("Generated short survey duration flag for Timing")
        except Exception as e:
            self.logger.error(f"Error checking short durations for Timing: {e}")

    def check_long_duration(self):
        self.logger.info("Checking for long survey durations")
        try:
            self.df['Flag_Timing_Long_Duration'] = (self.df['Duration_Mins'] > self.long_survey).astype(int)
            self.logger.info("Generated long survey duration flag for Timing")
        except Exception as e:
            self.logger.error(f"Error checking long durations for Timing: {e}")

    def check_abnormal_start_period(self):
        self.logger.info("Checking for Abnormal Start Periods")
        try:
            self.df['Flag_Timing_Abnormal_Start_Period'] = (self.df['Start_Period'].isin(self.abnormal_start_time)).astype(int)
            self.logger.info("Generated Abnormal Start Period flag for Timing")
        except Exception as e:
            self.logger.error(f"Error checking Abnormal Start Periods for Timing: {e}")

