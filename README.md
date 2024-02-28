# data-consultancy-post
This repository contains the source code for the project we did for the course 'Data Consultancy in Action' at JADS

## Getting Started
### Creating a virtual environment
1. Clone the repository into a specific directory: `git clone https://github.com/hvdv99/data-consultancy-post.git`
2. Enter project directory: `cd data-consultancy-post`
3. Create a virtual environment: `python -m venv venv`
4. Activate virtual environment: `windows: venv\Scripts\activate or mac: source venv/bin/activate`
5. Install packages from requirements with pip: `pip install -r requirements.txt`

### Working with the data
1. Then add the csv files to the data directory on your machine
2. Add the database file to the data directory

### Constants
In the director `config` there is one file called `constants`, you 

### Add to gitignore
Different IDE's use files we do not want in our repo. Check your directory for hidden files and add those to the `.gitignore` file.

### Branching strategy
Here it is explained how you should work with branches. For each feature, we will create a new branch. After 
your feature is done, you can create a pull request (must be created on the graphical user interface) which has to be verified by the product owner and one other developer. Then your feature can be merged with the main branch. 

Here are some helpful commands:
#### Working with branches
- `git branch` - shows all branches
- `git checkout -b <branch_name>` - creates a new branch and switches to it. Without `-b` it only switches to the existing branch.
- Very important: before you start working on a branch, first run: `git pull` to make sure you have the 
latest version of the branch you are working on.
#### Commiting to a branch
- `git add .` - adds all files to the staging area
- `git status` - shows the files that are in the staging area. This is very helpful to check if you did not make any 
mistakes while pushing.
- `git commit -m "Your message"` - commits the files in the staging area to the branch you are working on.
- `git push` - pushes staged files to the branch you are working on.

#### Merging branches
- once the feature branch is complete, you first have to make sure it is up to date on github
- then you can create a pull request on the github website
- You select the product owner and another developer to review your code
- The reviewers will check your code and give you feedback
- You now have to make the changes the reviewers asked for
- After the reviewers are satisfied, the product owner will merge the branch with the main branch