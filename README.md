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
- [clone the repository](https://help.github.com/en/articles/cloning-a-repository)
- Optional: create a new git branch for deployment on heroku using `git checkout -b new_branch_name`
- in the `app.py` file modify the secret key (lines 9 and 10) so that it has a fixed value (otherwise you might get session conflicts depending on how many workers Heroku assigns to your app): instead of generating a key with `os.urandom(16)` every time the script is run, use `os.urandom(<bits of choice>)` externaly (in IDLE, for example) and copy the result for your key, or alternatively assign it a strong secret key by hand
- create a mongoDB ATLAS account (or another mongoDB online database service), create a sandbox (free) database cluster, and in the `auth.py` file change the MongoClient line to `client = MongoClient('mongodb+srv://<your_username>s:<your_password>@<your_db_URI>')` (also add an `import dns` statement) replacing the fields as per instructions/your choices when you created your online database (you should allow your database to be accessed from any IP, as Heroku does not assign static IPs to apps) 
- Optional: you may also use Heroku's own mLab extension and follow their instructions
- Install the [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli#download-and-install)
- Run `heroku create app_name` (I used `heroku create pithy-notes` so that name is already taken)
- With the git branch you want to deploy on Heroku selected run `git push heroku master` or `git push heroku new_branch_name:master` depending on whether you created a different branch for Heroku deployment or not
- Make sure that your app is online by running `heroku ps:scale web=1`
- I have created all the necessary files (requirements.txt, runtime.txt, Procfile) already so you should be good to go after this, with your site running at `app_name.herokuapp.com`
- For a more detailed take on how to deploy on Heroku with python, read their [own guide](https://devcenter.heroku.com/articles/getting-started-with-python)
