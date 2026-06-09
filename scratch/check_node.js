const fs = require('fs');
const Papa = require('papaparse'); // Wait, papaparse might not be installed globally, I'll just write a simple manual check.
const csv = fs.readFileSync('/Users/samudra/.gemini/antigravity/brain/82723891-e9fc-454a-82d4-77c267cd0cf8/.system_generated/steps/674/content.md', 'utf8');

// The CSV content starts at line 9.
const lines = csv.split('\n');
let startLine = 0;
for(let i=0; i<lines.length; i++) {
  if(lines[i].startsWith('Timestamp')) {
    startLine = i;
    break;
  }
}

const headerLine = lines[startLine];
const headers = headerLine.split(',');
console.log("Headers:");
headers.forEach((h, i) => console.log(i + ": " + h));

const row = lines[startLine + 1]; // First row data
const rowData = row.split(',');
console.log("\nRow Data:");
rowData.forEach((d, i) => console.log(i + ": " + d));
