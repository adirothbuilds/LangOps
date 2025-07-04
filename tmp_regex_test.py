import re

# Old regex pattern
old_pattern = re.compile(r"\[([A-Za-z][A-Za-z0-9\s]*)\]\s+(.*)")

# New regex pattern
new_pattern = re.compile(r"\[([A-Za-z][\w\s]*)\]\s+(.*)", re.IGNORECASE)

# Sample test strings
test_strings = [
    "[Git] Cloning repository...",
    "[Poetry] Installing dependencies...",
    "[Pipeline] sh",
    "[A] Single character stage",
    "[AB123] Complex stage name",
]

# Test the regex patterns
for test in test_strings:
    old_match = old_pattern.match(test)
    new_match = new_pattern.match(test)
    print(f"Test: {test}")
    print(f"Old Match: {old_match.groups() if old_match else None}")
    print(f"New Match: {new_match.groups() if new_match else None}\n")
