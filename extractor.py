import re
from datetime import datetime


# Regular expression pattern to match date and time
pattern = r"\b(\d{1,2}[./-]\d{1,2}[./-]\d{2,4}|[a-z]+\s*\d{1,2}\s*,*\s*\d{2,4}|\d{2,4}[./-]\d{1,2}|\d{1,2}\s*[a-z]+\s*,*\s*\d{2,4})[\sa-z]*(\d{1,2}:\d{2}\s*[ap]?[m]?)?\b"

# Dictionary of regex patterns and corresponding date formats
regex_formats = {
    # Time formats
    r'\b(\d{1,2}:\d{2}[ap][m])\b': "%I:%M%p",
    r'\b(\d{1,2}:\d{2}\s*[ap][m])\b': "%I:%M %p",
    r'\b(\d{1,2}:\d{2}\s*)\b': "%I:%M",
    # Full year formats 
    r'\b(\d{1,2}([./-])\d{1,2}([./-])\d{4})\b': "%d2%m3%Y",
    r'\b([a-z]+(\s*)\d{1,2}(\s*,*\s*)\d{4})\b': "%B2%d3%Y",
    r'\b(\d{4}([./-])\d{1,2})\b': "%Y2%m",
    r'\b(\d{1,2}([./-])\d{4})\b': "%m2%Y",
    r'\b(\d{1,2}(\s*)[a-z]+(\s*,*\s*)\d{4})\b': "%d2%B3%Y",
    # Partial year formats
    r'\b(\d{1,2}([./-])\d{1,2}([./-])\d{2})\b': "%d2%m3%y",
    r'\b([a-z]+(\s*)\d{1,2}(\s*,*\s*)\d{2})\b': "%B2%d3%y",
    r'\b(\d{1,2}([./-])\d{2})\b': "%m2%y",
    r'\b(\d{1,2}(\s*)[a-z]+(\s*,*\s*)\d{2})\b': "%d2%B3%y"
}


def extract_datetime_object(raw_text):

    # Extracting date and time using regular expression with case-insensitive and global flags
    for pattern, date_format in regex_formats.items():
        match = re.search(pattern, raw_text, re.IGNORECASE | re.MULTILINE)
        if match:
            date_str = match.group(1)
            date_format_backreferences = re.findall(r'(\d{1})', date_format)
            for backreference in date_format_backreferences:
                date_format = date_format.replace(backreference,  match.group(int(backreference)))
            # Convert date string to datetime object
            date_obj = datetime.strptime(date_str, date_format)
            return date_obj, date_format
            
    return None, None
    

def extract_datetime(raw_text):
 
    # Extracting date and time using regular expression
    match = re.findall(pattern, raw_text, re.IGNORECASE | re.MULTILINE)
    if match:
        for date,time in match:
            date_object, date_format = extract_datetime_object(date)
            time_object, time_format = extract_datetime_object(time)
            if time_object:
                datetime_obj = datetime.combine(date_object.date(), time_object.time())
            else:
                datetime_obj = date_object
            return [datetime_obj, date_format, time_format, date, time]
    else:
        return None



PATTERN_NUMBER = r"^\bX*\d+X*\b$|^[X\s\d]+\b$"

def extract_number(raw_text):
    match = re.search(PATTERN_NUMBER, raw_text, re.IGNORECASE | re.MULTILINE)
    if match:
        if re.search("X", match.group(0), re.IGNORECASE | re.MULTILINE):
            return match.group(0), True
        else:
            return match.group(0), False
    return None



def extract_details(text_detected):
    extracted_details = []
    extracted_datetime_objects = []
    extracted_masked_numbers = []

    for raw_text in text_detected:
        # print(raw_text)
        response = extract_datetime(raw_text)
        if response:
            datetime_obj, date_format, time_format, date, time = response
            # print("Date_obj:", datetime_obj)
            # print("Date_format:", date_format)
            # print("Time_format:", time_format)
            extracted_datetime_objects.append(datetime_obj)
        else:
            datetime_obj = None
        response = extract_number(raw_text)
        if response:
            extracted_number, is_masked = extract_number(raw_text)
            extracted_number = extracted_number.replace(" ", "")
            if not is_masked:
                if len(extracted_number) > 6:
                    masked_number = "X" * (len(extracted_number)-6) + str(extracted_number[-6:])
                else:
                    masked_number = "X" * len(extracted_number)
            else:
                masked_number = extracted_number
            extracted_masked_numbers.append(masked_number)
        else:
            masked_number = None

    return [extracted_datetime_objects, extracted_masked_numbers]


text = "I will be attending a conference at Google on 25th November 2023 in New York."

def main():
    while True:
        text_detected = input('text_detected separated by | (if multiple): ').split('|')
        extracted_details = extract_details(text_detected)
        print("extracted_details: " + str(extracted_details))

if __name__ == "__main__":
    main()
