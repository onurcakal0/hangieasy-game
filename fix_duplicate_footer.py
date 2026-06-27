import re

with open('templates/dashboard.html', 'r') as f:
    content = f.read()

# Find all occurrences of the footer
# The footer starts with "    <!-- YENİ GELİŞMİŞ FOOTER (QUIZEI TARZI) -->" and ends with "    </style>\n"
pattern = re.compile(r'    <!-- YENİ GELİŞMİŞ FOOTER \(QUIZEI TARZI\) -->.*?    </style>\n', re.DOTALL)
matches = pattern.findall(content)

if len(matches) > 1:
    # Remove the first match
    first_match = matches[0]
    content = content.replace(first_match, "", 1)
    
    with open('templates/dashboard.html', 'w') as f:
        f.write(content)
    print(f"Removed the first duplicate footer. Total footers were {len(matches)}.")
else:
    print(f"Only found {len(matches)} footer. No duplicates.")
