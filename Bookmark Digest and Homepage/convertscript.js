const fs = require('fs');
const yaml = require('js-yaml');
const fetch = require('node-fetch');
const { parse } = require('node-html-parser');

// Define the input file containing the list of websites
const inputFile = 'websites.txt';

// Define the output file for the YAML data
const outputFile = 'websites.yaml';

// Read the input file and parse the URLs
const urls = fs.readFileSync(inputFile, 'utf-8').trim().split('\n');

// Define a function to extract the title from a web page
async function getTitle(url) {
  try {
    const res = await fetch(url);
    const html = await res.text();
    const root = parse(html);
    const titleElement = root.querySelector('title');
    return titleElement ? titleElement.text.trim() : null;
  } catch (error) {
    console.error(`Error fetching title for ${url}: ${error}`);
    return null;
  }
}

// Define the YAML data structure
const data = [];

// Loop through the URLs and add them to the data structure
for (const url of urls) {
  const title = await getTitle(url) || url;
  data.push({ url, title });
}

// Write the YAML data to the output file
fs.writeFileSync(outputFile, yaml.safeDump(data));
