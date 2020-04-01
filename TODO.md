# App TODO
- [x] Create an index/home page that will allow navigation to individual pages as they are created
- [x] Setup the app to run from a server and not localhost
- [x] Restructure file layout like the bottom of [this page](https://dash.plot.ly/urls)
- [x] Create "modules" for running individual pages on the Dash server so they can be updated without changing the entire page (also this will keep it from becoming one huge file to maintain)
    - Started this structure, simply create the file for the page then import the .py file to use its stuff
- [x] Finish designing the SQL table structure for program data captures
- [x] Create some sort of authentication system to allow authorized people 
to edit necessary information (ie. HR authorized to edit the personnel table)
- [x] Finish layout for employee roster table page
- [ ] Create chart that outlines over a -3 to +12 month line chart of employee count
    - [ ] This should be filterable by department (Finance Function)
- [x] Create the login page
- [x] ~~Create the `AuthAccess.py` for LDAP authentication with active directory through~~ [Flask](https://code.tutsplus.com/tutorials/flask-authentication-with-ldap--cms-23101)
    - Our LDAP uses port 389
- [x] Access control built into user database table with isAdmin boolean
    - [x] Use SQL table name and department for page access
- [x] Separate `app.py` and contain site core callbacks within it
- [x] Make navbar contain callbacks for formatting active pages
- [x] Create `SQL.py` to control all SQL database read/write requests
---
#Home TODO
- [x] Doge pics
- [x] Contact form
    - [x] Reason selection (feature request, issue report, admin request)
    - [x] Submitter info (maybe this can be automatic with the LDAP)
- [x] Change Log
- [x] Features in development
- [x] Add an IsAdmin boolean variable so admin only controls will or wont show
---
#Employees TODO
- [ ] User / Manager view based on LDAP credential check for admin in SQL
- [x] Employee table
    - [x] Search by field (doesn't currently work in IE but does in FF)
    - [x] Sort by field
    - [ ] Option to toggle employees with end date listed
- [ ] Edit employees button
    - [x] Modal to edit all fields in entry
    - [ ] Quick change level / position button to quickly prompt with end 
    date picker that when submitted will add new entry with selected date as
     start and all other information populated
- [x] Add New Employee button
    - Likely the same form as edit but not pre populated
---
#Programs TODO
- [x] Add a drag and drop zone to page to allow quick uploading of new 
resource summary and needs from program managers
    - [x] Make the upload overwrite existing entries in the database for 
    matching charge code and dates
    - [x] Add functionality to parse the data to a structure suitable for 
    the database table layout
- [x] Add data filter dropdowns at top of page
    - [ ] ~~Employee by name? (only if the names or employee numbers are added
     to resource sheets~~ 
    will this work)
    - [x] Charge #
    - [ ] ~~Program Name~~
    - [ ] ~~Project Name~~
    - [ ] ~~Start Date (figure out a toggle option for range date)~~
    - [ ] ~~End Date (same as above)~~
    - [x] Charge year
    - [x] Charge period
    - [x] Charge Quarter
- [x] Fetch Data button with filter criteria
- [x] Data table for filtered data
    - [ ] ~~Support inline editing~~
- [ ] ~~Add new entry (this is likely superseded by the drag and drop to upload)~~
- [x] Add a viewer for current Charge numbers, Major Programs and Projects
- [x] Add editor for the above items
---
#Capacity TODO
- [x] Add a table for displaying employee numbers over a range of -3 to +12 
months broken down by function
- [x] Add a chart that displays the breakdown of function over the same 
timeline