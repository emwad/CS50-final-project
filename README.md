# UK National Student Survey Comparison Tool
#### Video Demo:  <URL HERE>
#### Description:
The National Student Survey (NSS) is a yearly survey conducted throughout the UK by final year undergraduate students at Universities (there are other modes of study, but this is what I have focused on for the comparison tool).

Whilst there are online tools for prospective students to interpret results and view information about specific institutions/courses compared to national benchmarks, there is not currently a tool that allows students to directly compare two different insitutions' results.

My 'UK NSS Tool' aims to do this. For this project, I have limited the scope to comparisons between the 7 main "Themes" of the survey, but this could later be expanded to all 26 individual questions in the survey.

### Sourcing/cleaning data: 
The data was sourced from the Office for Students NSS official site ([URL](https://www.officeforstudents.org.uk/data-and-analysis/national-student-survey-data/download-the-nss-data/)). I used the "teach_ft" 2025 data set, that compares the institutions which _delivered_ teaching to students. For the time being, I have limited comparison to full time students only.

I checked and cleaned the data using the Python pandas library, on a Jupyter notebook in an Anaconda environment, reading the CSV file into a dataframe. The "NSS.ipynb" file is the Jupyter notebook I used to do this, annotated with the steps taken. The cleaned data file is included: "NSS_themes.csv". The original csv file can be found in [this download](https://blobofsproduks.blob.core.windows.net/files/NSS/2025/publication_csv_cuts.zip) as "teach_ft.csv".

Details of columns are listed in "Data dictionary NSS.csv".

Summary of changes to data:
- Unnecessary columns were removed
- NULL values were replaced with "N/A" where appropriate
- Unnecessary rows were removed (entire country summaries, which will not be used on the comparison tool)
- Individual questions were removed, leaving only "Themes".
