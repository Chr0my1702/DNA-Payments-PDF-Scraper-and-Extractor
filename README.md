# DNA-Payments-PDF-Scraper-and-Extractor

## The work is split up into 6 parts:
### • Scraping & Downloading
### • Unzipping & Steralisation
### • Folder & Infomaker
### • Scanning & Processing
### • Compiling it all
### • Finalisation









## Part 1: Scraping & Downloading
Open browser, go to salesforce, and search by files and your term. Then limit to PDFs only. 
Then open developer tools and go to console.
Paste in the autoscroller.js.
Wait till it scrolls to the bottom.
Then in your browser, "save page as", into a folder.
Run the python script, which will output a file to output.txt.
Then run "run.ps1" but make sure you change the variables in the powershell script. 
**It will look like it is not downloading, but give it a few minutes as the server takes time to respond to the download request**


## Part 2: Unzipping
In a "master" folder, make another folder called "raw-pdfs". Use an unzipper, and unzip all to raw-pdfs. 

## Part 3: Folder & Infomaker
Now run filemaker.py. It will make make folders and place each file in a folder.
Then run infomaker.py. It will read each pdf and make a JSON file with data about the PDF and merchant name. **(This will take a while)**
The JSON file will contain information like this:
```
{
    "file_name": "SIGNED_MSA_Example.pdf",
    "merchant_name": "Example Ltd",
    "trader_name": "Example",
    "page_number": 3,
    "table_number": 2,
    "table_type": 1,
    "is_cut_off": false
}
```

## Part 4: Scanning & Processing


## Part 5: Compiling it all
## Part 6: Finalisation



