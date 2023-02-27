import argparse
import os
import re
import yaml

# Create an ArgumentParser object
parser = argparse.ArgumentParser(description='Convert a bookmark file to YAML format')

# Add a positional argument for the bookmark file path
parser.add_argument('bookmark_file', type=str, help='Path to the bookmark file')

# Parse the command-line arguments
args = parser.parse_args()

# Read in the bookmark file
with open(args.bookmark_file, "r", encoding="utf-8") as f:
    bookmark_file = f.read()

# Extract the bookmark entries
bookmark_regex = r'<DT><A HREF="(?P<url>.*?)".*?>(?P<title>.*?)<\/A>\s*(?:<DD>(?P<desc>.*?)<\/DD>)?'
bookmark_entries = re.findall(bookmark_regex, bookmark_file, flags=re.DOTALL)

# Create the YAML data structure
data = []
for entry in bookmark_entries:
    url = entry[0]
    title = entry[1]
    desc = entry[2] if len(entry) > 2 else None
    if not title:
        title = desc
    if not title and not desc:
        title = "Untitled"
    data.append({"title": title.strip(), "url": url})

# Write the YAML data to a file
output_file = os.path.splitext(args.bookmark_file)[0] + ".yaml"
with open(output_file, "w", encoding="utf-8") as f:
    yaml.dump(data, f, default_flow_style=False, allow_unicode=True)

print(f"Conversion complete. Output saved to {output_file}")
