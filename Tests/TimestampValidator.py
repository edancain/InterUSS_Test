from datetime import datetime
import re


class TimestampValidator:
    @staticmethod
    def is_rfc3339(timestamp):
        """
        Check if the provided timestamp is in RFC 3339 format.
        RFC 3339 format: YYYY-MM-DDTHH:MM:SSZ or YYYY-MM-DDTHH:MM:SS.sssZ
        """
        # Regular expression for RFC 3339 format
        rfc3339_regex = r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z$'

        try:
            if re.match(rfc3339_regex, timestamp):
                # Try to parse the timestamp
                datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
                return True
            else:
                return False
        except ValueError:
            # If parsing fails, the format is not RFC 3339
            return False


# Example usage
# timestamp = "2023-11-16T21:00:00Z"
# if TimestampValidator.is_rfc3339(timestamp):
#    print(f"The timestamp {timestamp} is in RFC 3339 format.")
# else:
#    print(f"The timestamp {timestamp} is not in RFC 3339 format.")
