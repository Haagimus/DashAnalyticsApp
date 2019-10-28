#Introduction 
This project will serve to host as a data visualization and access point to the company SQL server for employee and project resources and demand (creation still in progress)

#Getting Started
1.	Installation process
    - If you do not have Python installed I recommend downloading and installing Anaconda 3 as it has most of the dependencies included
    - Install software dependencies
2.	Software dependencies
    - [Anaconda](https://www.anaconda.com/distribution/#download-section)
    - [Dash](https://pypi.org/project/dash/#files)
    - [Dash Core Components](https://pypi.org/project/dash-core-components/#files)
    - [Dash HTML Components](https://pypi.org/project/dash-html-components/#files)
    - [Dash Renderer](https://pypi.org/project/dash-renderer/#files)
    - [Dash Table](https://pypi.org/project/dash-table/#files)
    - [Flask Compress](https://pypi.org/project/Flask-Compress/#files)
    - [Retrying](https://pypi.org/project/retrying/#files)
    - [Plotly](https://pypi.org/project/plotly/#files)
    - SQL Server Management Studio (not required but allows direct SQL access)
3.	Latest releases
4.	API references
    - [Dash Reference](https://dash.plot.ly/)
    - [Anaconda Reference](https://docs.conda.io/projects/conda/en/latest/user-guide/index.html)

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
1. [Virtual Environment Management](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html)