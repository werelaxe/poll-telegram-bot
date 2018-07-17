import re

COMMON_TRIGGER_PATTERN = '.*го.+?есть.+?в\s+(.*)'
DINNER_TIME_TRIGGER_PATTERN = '\s*когда\s*(?:на)?\s*обед\??\s*'
DINNER_PLACE_TRIGGER_PATTERN = '\s*куда\s*(?:на)?\s*обед\??\s*'
BREAKFAST_TIME_TRIGGER_PATTERN = '\s*когда\s*(?:на)?\s*завтрак\??\s*'

SEP_PATTERN = re.compile('(?:[,;?!\s]+)(?:или)?', re.IGNORECASE)


def get_suggestions_in_common_case(message_text):
    raw_suggestion = re.findall(COMMON_TRIGGER_PATTERN, message_text)
    if raw_suggestion:
        return [op.strip() for op in re.split(SEP_PATTERN, raw_suggestion[0]) if op.strip()]
