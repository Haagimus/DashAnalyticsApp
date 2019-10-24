#Introduction 
This project will serve to host as a data visualization and access point to the company SQL server for employee and project resources and demand (creation still in progress)

#Getting Started
1.	Installation process
    - If you do not have Python installed I recommend downloading and installing Anaconda 3 as it has most of the dependencies included
    - Install software dependencies
2.	Software dependencies
    - Dash w/ plot.ly
    - Python 3.7
    - Numpy
    - Pandas
    - SQL Server Management Studio (not required but allows direct SQL access)
3.	Latest releases
4.	API references
    - [Dash Reference](https://dash.plot.ly/)
    - [Anaconda Reference](https://docs.conda.io/projects/conda/en/latest/user-guide/index.html)

#Things remaining to do
[ ] Create an index/home page that will allow navigation to individual pages as they are created
[ ] Figure out how to run the Dash server non local host
[ ] Create "modules" for running individual pages on the Dash server so they can be updated without changing the entire page (also this will keep it from becoming one huge file to maintain)
    - Started this structure, simply create the file for the page then import the .py file to use its stuff
[ ] Finish designing the SQL table structure for program data captures
[ ] Create some sort of authentication system to allow authorized people to edit necessary information (ie. HR authorized to edit the personnel table)
[ ] Finish layout for employee roster table page
[ ] Create chart that outlines over a -3 to +12 month line chart of employee count
    - [ ] This should be filterable by department (Finance Function)

#Installing Python packages manually with our company proxy
1. Install anaconda
2. Add the anaconda installation path to your environmental variables
    - This should be in "[User Folder]\AppData\Local\Continuum\anaconda3" by default
3. Add the anaconda scripts path to your enviornmental variables
    - This should be in the "\Scripts" folder of the above filepath
4. Launch the command prompt, powershell or the conda terminal
5. Change to your download directory where the tar.gz archives were downloaded
6. type "pip install 'archive name.tar.gz'
    - If there are any prerequisites needed there will be an error message stating the missing dependency, just download that archive from pypi.org and install it first

#Useful Links
1. [Anaconda](https://www.anaconda.com/distribution/#download-section)
2. [Dash](https://pypi.org/project/dash/#files)
3. [Dash Core Components](https://pypi.org/project/dash-core-components/#files)
4. [Dash HTML Components](https://pypi.org/project/dash-html-components/#files)
5. [Dash Renderer](https://pypi.org/project/dash-renderer/#files)
6. [Dash Table](https://pypi.org/project/dash-table/#files)
7. [Flask Compress](https://pypi.org/project/Flask-Compress/#files)
8. [Retrying](https://pypi.org/project/retrying/#files)
9. [Plotly](https://pypi.org/project/plotly/#files)
10. [Virtual Environment Management](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html)