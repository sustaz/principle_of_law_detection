import re

def return_paragraph_number(paragraph):
  return paragraph.split()[0]


def extract_text_between_markers(text):
    # Define the patterns to search for
    pattern1 = re.compile(r"Consideration of the question referred(.*?)Costs", re.DOTALL)
    pattern2 = re.compile(r"Consideration of the questions referred(.*?)Costs", re.DOTALL)

    # Try to find matches for both patterns
    match1 = pattern1.search(text)
    match2 = pattern2.search(text)

    # Return the matched text if found
    if match1:
        return match1.group(1).strip()
    elif match2:
        return match2.group(1).strip()
    else:
        return None