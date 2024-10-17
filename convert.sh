
#!/bin/bash

# Define the template file
template="template.html"

file="main.md"
# Loop through all .md files in the current directory
output="${file%.md}.html"
echo "${output}"

# Run the pandoc command
pandoc "$file" --template "$template" -o "$output"

echo "Converted $file to $output"

