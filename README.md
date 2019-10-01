# Pithy-Notes
A pithy note taking app using Flask, Flask-RESTful, and MongoDB (pymongo) for the back-end, and plain HTML/CSS and Javascript for the front-end. Requires [ace editor](https://ace.c9.io/). 

## Installation instructions
### Local playground
- [clone the repository](https://help.github.com/en/articles/cloning-a-repository)
- in the `resources/static` folder create a new folder titled `lib`
- download an ace editor [build](https://github.com/ajaxorg/ace-builds/) (`ace.js` file) of your choice from their repository (I used the src-min-noconflict version)
- download an ace editor theme script file and highlight option script file from the same folder you downloaded `ace.js` (I used `theme-chrome.js` and `mode-markdown.js`)
- copy them into the `lib` directory you created previously
- modify the `index.html` file in the `resources/templates` folder to match your choices (or leave it intact if you picked the same files; more info [here](https://ace.c9.io/#nav=embedding))
- open a terminal or a powershell window in the project folder and run `pip install -r requirements.txt`
- download [mongoDB](https://www.mongodb.com/download-center/community) (click on the server tab and download the version appropriate for your OS) and [install](https://docs.mongodb.com/manual/installation/) it following the instructions provided
- navigate to the `bin` directory of your mongoDB installation folder, open a terminal or a powershell window and run `./mongod(.exe) --dbpath <path to where you want your local database instance created, should end in data/db>` 
- open a terminal or a powershell window in the project folder (where the `app.py` file is located) and run `python app.py`

### Deploy on Heroku
