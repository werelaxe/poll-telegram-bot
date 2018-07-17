import re

COMMON_TRIGGER_PATTERN = re.compile('.*го.+?есть.+?в\s+(.*)', re.IGNORECASE)
DINNER_TIME_TRIGGER_PATTERN = re.compile('\s*когда\s*(?:на)?\s*обед\??\s*', re.IGNORECASE)
DINNER_PLACE_TRIGGER_PATTERN = re.compile('\s*куда\s*(?:на)?\s*обед\??\s*', re.IGNORECASE)
BREAKFAST_TIME_TRIGGER_PATTERN = re.compile('\s*куда\s*(?:на)?\s*завтрак\??\s*', re.IGNORECASE)

SEP_PATTERN = re.compile('(?:[,;?!\s]+)(?:или)?', re.IGNORECASE)


def get_suggestions_in_common_case(message_text):
    raw_suggestion = COMMON_TRIGGER_PATTERN.findall(message_text)
    if raw_suggestion:
        return [op.strip() for op in re.split(SEP_PATTERN, raw_suggestion[0]) if op.strip()]
