from datetime import datetime

def parse_iso8601(timestamp):
    return datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S.%fZ')


def get_date_from_timestamp(item):
    print("Timestamp: ", item)
    timestamp = parse_iso8601(item)
    return timestamp.date()
