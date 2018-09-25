import re

OLD_COMMON_TRIGGER_PATTERN = '.*[гГ]о.+?есть.+?в\s+(.*)'
COMMON_TRIGGER_PATTERN = '.*[оО]прос\s*[:,]?\s*(.*)'
DINNER_TIME_TRIGGER_PATTERN = '\s*[кК]огда\s*(?:на)?\s*обед\??\s*'
DINNER_PLACE_TRIGGER_PATTERN = '\s*[кК]уда\s*(?:на)?\s*обед\??\s*'
BREAKFAST_TIME_TRIGGER_PATTERN = '\s*[кК]огда\s*(?:на)?\s*завтрак\??\s*'

SEP_PATTERN = re.compile(',|или', re.IGNORECASE)
STRIP_CHARS = ' ?!.'


def get_suggestions_in_common_case(message_text):
    raw_suggestion = re.findall(COMMON_TRIGGER_PATTERN, message_text)
    if raw_suggestion:
        return [op.strip(STRIP_CHARS) for op in re.split(SEP_PATTERN, raw_suggestion[0]) if op.strip(STRIP_CHARS)]


def get_suggestion(callback_title: str):
    dash_index = callback_title.rfind("-")
    return callback_title[:dash_index - 1]
