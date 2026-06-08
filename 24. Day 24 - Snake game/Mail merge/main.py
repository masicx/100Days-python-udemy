with open(r"C:\Code\100DaysCourse\24. Day 24 - Snake game\Mail merge\input\names\invited_names.txt", "r") as file:
    names = file.readlines()

with open(r"C:\Code\100DaysCourse\24. Day 24 - Snake game\Mail merge\input\letters\starting_letter.txt", "r") as file:
    letter = file.read()
    for name in names:
        new_letter = letter.replace("[User]", name.strip())
        with open(rf"C:\Code\100DaysCourse\24. Day 24 - Snake game\Mail merge\output\readytosend\letter_for_{name.strip()}.txt", "w") as file:
            file.write(new_letter)