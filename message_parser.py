import re

TRIGGER_PATTERN = re.compile('.*го.+?есть.+?в\s+(.*)', re.IGNORECASE)
SEP_PATTERN = re.compile('(?:[,;?!\s]+)(?:или)?', re.IGNORECASE)


def get_suggestions(message_text):
    raw_suggestion = TRIGGER_PATTERN.findall(message_text)
    if raw_suggestion:
        return [op.strip() for op in re.split(SEP_PATTERN, raw_suggestion[0]) if op.strip()]
