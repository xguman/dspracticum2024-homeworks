#!/bin/bash

mkdir -p downloaded_html

# Read the links from the links.txt file and download each one
while read -r link; do
    if [[ -n "$link" ]]; then
        # Extract the file name from the URL
        file_name=$(basename "$link").html
        # Download the HTML content and save it to a file
        wget -O "downloaded_html/$file_name" "$link"
        echo "Downloaded and saved: $file_name"
    fi
done < links.txt