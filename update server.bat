@ECHO off

SET local_files=__init__.py^
				config.py^
				app.py^
				run.py^
				server.py^
				wsgi.py^
				assets\server.css^
				assets\bootstrap-grid.css^
				assets\bootstrap-grid.min.css^
				assets\bootstrap.css^
				assets\bootstrap.min.css^
				assets\callbacks.py^
				assets\font-awesome^
				assets\models.py^
				assets\navbar.py^
				assets\SQL.py^
				assets\__init__.py^
				assets\Files\Active_Features.txt^
				assets\Files\favicon.ico^
				assets\Files\Upcoming_Features.txt^
				assets\font-awesome\css\all.css^
				assets\font-awesome\css\all.min.css^
				assets\font-awesome\webfonts\fa-brands-400.eot^
				assets\font-awesome\webfonts\fa-brands-400.svg^
				assets\font-awesome\webfonts\fa-brands-400.ttf^
				assets\font-awesome\webfonts\fa-brands-400.woff^
				assets\font-awesome\webfonts\fa-brands-400.woff2^
				assets\font-awesome\webfonts\fa-regular-400.eot^
				assets\font-awesome\webfonts\fa-regular-400.svg^
				assets\font-awesome\webfonts\fa-regular-400.ttf^
				assets\font-awesome\webfonts\fa-regular-400.woff^
				assets\font-awesome\webfonts\fa-regular-400.woff2^
				assets\font-awesome\webfonts\fa-solid-900.eot^
				assets\font-awesome\webfonts\fa-solid-900.svg^
				assets\font-awesome\webfonts\fa-solid-900.ttf^
				assets\font-awesome\webfonts\fa-solid-900.woff^
				assets\font-awesome\webfonts\fa-solid-900.woff2^
				assets\Images\L3Harris.svg^
				assets\Images\cat_peel.jpg^
				pages\__init__.py^
				pages\capacity.py^
				pages\employees.py^
				pages\home.py^
				pages\programs.py

SET local_path=C:\Users\ghaag\Programming\Python Projects\Resource Tracker\Resources_App
SET network_path=\\frxsv-dauphin\users\thollis.sa\DashSiteFiles

(for %%i IN (%local_files%) DO (
	XCOPY "%local_path%\%%i" "%network_path%\%%i" /y
))
