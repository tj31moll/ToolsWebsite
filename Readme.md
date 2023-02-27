# ToolsWebsite - Start

This is a Python script that converts a bookmark file to YAML format. It uses the argparse module to create a command-line interface for specifying the path to the bookmark file. Then it reads in the file and extracts the bookmark entries using a regular expression pattern (bookmark_regex).

The regular expression pattern matches the following structure:

"<DT><A HREF=": a required pattern at the start of each bookmark entry.
"(?P<url>.*?)": a required named capturing group for the bookmark URL.
'.*?>': a pattern for the end of the URL, including any other attributes like ADD_DATE, PRIVATE, TOREAD, and TAGS.
"(?P<title>.*?)": a required named capturing group for the bookmark title.
"</A>": a pattern for the end of the bookmark title.
"\s*(?:<DD>(?P<desc>.*?)</DD>)?": an optional named capturing group for the bookmark description, which may be preceded by whitespace characters and a <DD> tag.
Once the bookmark entries are extracted, the script creates a YAML data structure that includes the bookmark title and URL for each entry. If a title is not available, it uses the description instead. If neither title nor description is available, it sets the title to "Untitled".

Finally, the script writes the YAML data to a file with the same name as the input file but with a .yaml extension, and prints a message indicating the name of the output file.
