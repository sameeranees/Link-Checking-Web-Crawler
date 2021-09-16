# Link-Checking-Web-Crawler
The Web Crawler checks links on the website recursively and then outputs the URLs that are broken, the Parent URLs and the Exception Errors in a CSV file.
## Installation
The following libraries are needed:
1. Requests (pip install requests)
2. Beautiful Soap (pip install beautifulsoup4)
3. Joblib (pip install joblib)
## Usage
The file can be run by providing arguments: Url of website to check links, Name of File.
```
python webcrawler.py --url <URL OF WEBSITE> --name <NAME OF FILE(CSV FILE)>
```
For example:
```
python webcrawler.py --url wwww.google.com --name BrokenLinks.csv
```
