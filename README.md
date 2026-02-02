# UK National Student Survey Comparison Tool
#### Video Demo:  <https://youtu.be/ZRN3jphHTmY>
## Description

The National Student Survey (NSS) is a yearly survey conducted throughout the UK by final year undergraduate students at Universities (there are other modes of study, but this is what I have focused on for the comparison tool).

Whilst there are online tools for prospective students to interpret results and view information about specific institutions/courses compared to national benchmarks, there is not currently a tool that allows students to directly compare two different insitutions' results.

My 'UK NSS Tool' does this. For this project, for simplicity and as it is 'proof of concept' at this stage, I have limited the scope to comparisons between the 7 main "Themes" of the survey. For now, I have not given the option to drill down results by course, but the information is present in the database to later expand its features.

## Overall structure of the website

This is a flask web-app. NSS data is held in a sqlite database; "NSS.db". This is referenced by the "app.py" which takes user input from a front-end html form, and creates charts based on institutions selected by the user.

## Files included
### <ins>Files that form the web-app</ins>
### nss.db
This is the database which contains cleaned NSS data on full-time providers in the UK. It contains five tables:

**<ins>nss</ins>** - List of providers, their UKPRNs (unique identifier), subject codes and names (due to limited initial scope, you cannot yet filter by subjects, but I have retained this so that the feature can be added in later), and columns relating to question themes and responses. This table gives us the data made into results charts.

**<ins>institutions</ins>** - A list of unique insitution names and UKPRNs, used for autocomplete and validation on the user form.

**<ins>themes</ins>** - A list of themes and IDs, used for validation on the user form.

**<ins>addresses</ins>** - This table is not used in the web-app as currently built, but I have retained the table in case of later feature addition. This contains publically available information, community sourced and incomplete, linking insitution UKPRNs to addresses. The site is here: https://learning-provider.data.ac.uk/.

**<ins>courses</ins>** - This table is not used in the web-app as currently built, but I have retained the table in case of later feature addition. It contains a list of all unique subjects and their NSS codes.

### app.py
**<ins>/index</ins>** <br>
<ins>GET:</ins> Returns the 'index.html' template along with a list of UK providers for the autofill <br>
<ins>POST:</ins> Validates the user's form entries and returns the main 'index.html' template with an error message if the user has not provided valid responses. Otherwise, generates results charts and returns the 'comparison.html' template.

**<ins>/info</ins>** <br>
Renders html template "info.html".

**<ins>/autocomplete</ins>** <br>
Provides the autocomplete function for the 'institutions' section of the user form.

### helpers.py
Contains helper functions called in the main app.py:

<ins>get_db(), close_db()</ins> <br>
Open and close a link with nss.db

<ins>generate_chart()</ins> <br>
Takes two 'row' objects you would get from a db.execute() command. Generates a horizontal barchart using matplotlib, which compares each row's insitution and the positivity measures, from the relevant columns in the row.

### HTML Templates

**<ins>index.html</ins>** <br>
The initial landing page, including user form and info.

**<ins>comparison.html</ins>** <br>
The pages that renders once the user has selected institutions and themes, containing charts for each theme comparing scores.

**<ins>info.html</ins>** <br>
Information page, linked to in various places, containing info on the NSS Themes and Positivity Measure.

**<ins>layout.html</ins>** <br>
Contains the layout used across all pages, including Navbar.

### static - flatly.css
css file that allows bootstrap's 'flatly' theme styling to be applied.

### <ins>Other files</ins>
These files were used in the preparation stage of the project, are no longer needed but retained for info.

**<ins>Data prep</ins>** <br>
<ins>environment.yml</ins> - the Anaconda environment used to clean the NSS csv <br>
<ins>NSS.ipynb</ins> - Jupyter notebook containing the steps to clean the NSS data ready for import into nss.db <br>
<ins>Data dictionary NSS.csv</ins> - information on what the columns mean in the NSS data<br>
<ins>NSS_themes.csv</ins> - final, cleaned information for upload into nss.db. <br>
<ins>ukprn.csv</ins> - sourced info on UKPRNs and addresses of UK institutions. <br>
<ins>functions.ipynb</ins> - Juptyer notebook where I created and tested some of the functions used on the site.

## Sourcing/cleaning data: 
The data was sourced from the Office for Students NSS official site ([URL](https://www.officeforstudents.org.uk/data-and-analysis/national-student-survey-data/download-the-nss-data/)). I used the "teach_ft" 2025 data set, that compares the institutions which _delivered_ teaching to students. For the time being, I have limited comparison to full time students only.

I checked and cleaned the data using the Python pandas library, on a Jupyter notebook in an Anaconda environment (environment.yml), reading the CSV file into a dataframe. The "NSS.ipynb" file is the Jupyter notebook I used to do this, annotated with the steps taken. The cleaned data file is included: "NSS_themes.csv". The original csv file can be found in [this download](https://blobofsproduks.blob.core.windows.net/files/NSS/2025/publication_csv_cuts.zip) as "teach_ft.csv".

Details of columns are listed in "Data dictionary NSS.csv".

Summary of changes to data:
- Unnecessary columns were removed
- NULL values were replaced with "N/A" where appropriate
- Unnecessary rows and rows with suppressed results were removed
- Individual questions were removed, leaving only "Themes".