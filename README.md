# data-consultancy-post
This repository contains the source code for the course 'Data Consultancy in Action' project we did for the  at JADS

## Getting Started
In the next section some explanation will follow on how work on this repository on your own machine.

### Creating a virtual environment
A Python virtual environment is a self-contained environment that includes a specific version of Python and a set of 
installed packages, isolated from the system-wide Python installation.

Virtual environments allow you to create separate Python environments for different projects, each with its own Python 
version and installed packages. This can be useful when you need to use different versions of packages or Python itself
for different projects, or when you want to avoid conflicts between packages that have conflicting dependencies.
1. First clone the repository into a specific directory: `git clone https://github.com/hvdv99/data-consultancy-post.git`
2. Enter project directory: `cd data-consultancy-post`
3. Create a virtual environment: `python -m venv venv`
4. Activate virtual environment: `windows: venv\Scripts\activate` or `mac: source venv/bin/activate`
5. Install packages from requirements with pip: `pip install -r requirements.txt`

Once the dependencies grow, add them to the `requirements.txt` file.

### Working with the data
1. Then add the csv files to the data directory on your machine
2. Add the database file to the data directory

### Constants
In the directory `config` there are two files: `constants.py` and `personal_constants.py`. We consider it a best
practice to include all non confidential constant variables in the `constants.py` file and all confidential constants
in the `personal_constants.py` file. `personal_constants.py` is included in`.gitignore` thus your confidential constants 
are never pushed to Github. Make sure to define all constants in UPPERCASE. Whenever you need a confidential constant,
first import the personal constant in `constants.py`, then import `constants.py` in your script.

#### Personal constants
You have to create your own personal constants file `config/personal_constants.py`. Make sure to include your own 
API-key and your model name. 

### Add to gitignore
Different IDE's use files we do not want in our repo. Check your directory for hidden files and add those to the 
`.gitignore` file.

### Branching strategy
Here it is explained how you should work with branches. The main point is that nobody is allowed to push directly to the
`main` brach. So, for each feature, we will create a new branch. After the feature is done, you can create a pull 
request (must be created on through graphical user interface of Github) which has to be reviewed by the Product Owner 
and one other developer (make sure to assign them in your pull request). After approval, your feature can be merged with 
the main branch. 

Here are some helpful commands to implement this strategy:
#### Working with branches
- `git branch` - shows all branches
- `git checkout -b <branch_name>` - creates a new branch and switches to it. Without `-b` it only switches to the 
existing branch.
- Very important: before you start working on a branch, first run: `git pull` to make sure you have the 
latest version of the branch you are working on.
#### Commiting to a branch
- `git add .` - adds all files to the staging area
- `git status` - shows the files that are in the staging area. This is very helpful to check if you did not make any 
mistakes while pushing.
- `git commit -m "Your message"` - commits the files in the staging area to the branch you are working on.
- `git push` - pushes staged files to the branch you are working on.

#### Creating a Pull Request & Merging branches
- Once the feature branch is complete, you first have to make sure it is up to date with the remote repo on Github. To
assure this, run in the CLI: `git pull`
- Then you can create a pull request on the Github website
- You select the Product Owner and another developer to review your code
- The reviewers will check your code and give you feedback by adding comments to your code.
- You can now resolve the comments by making new commits to the branch.
- After the reviewers are satisfied, the Product Owner will merge the branch with the main branch.
- 