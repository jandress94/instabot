# instabot
Instagram Bot to Bulk Follow a List of Usernames


## Running

### 1. Download external software

#### Minicoda
Install the Python 3.7 version of Miniconda for your operating system from this [page](https://docs.conda.io/en/latest/miniconda.html)

#### Chromedriver
Go to this [page](https://sites.google.com/a/chromium.org/chromedriver/home) and click to view the "Latest stable release".
Download the zip file for your operating system.

### 2. Download everything in this repo
Click the green "Clone or download" button above, then "Download ZIP".
The repo files should download to your machine as a zip. 
Unzip the repo.
You can move this directory to somewhere convenient (I assume it's on the desktop in the example below).

### 3. Move the chromedriver executable into the project directory
In step 1, you downloaded a chromedriver zip file. 
Unzip it, which should produce a `chromedriver` file.
Move this file into the directory created when you unzipped the repo in step 2.
You should now have `instabot.py`, `environment.yml`, and `chromedriver` in the same directory.

### 4. Create the conda environment

#### Open a terminal prompt and navigate to the project directory.
On Mac, press `command + SPACE` to open spotlight search, then type `terminal.app` and run it.
A terminal command prompt should open.
You now need to navigate to the project directory.
There are three commands that might be helpful:
- `pwd`: prints the current working directory (where you currently are in the filesystem).
- `ls`: prints all the files and directories in the current working directory
- `cd`: move into a different directory. 
The command `cd xyz` will move you into the `xyz` directory (assuming one exists in the current working directory).
The command `cd ..` will move you one step up into the parent directory.

So, let's assuming the project directory you created in step 2 is called `instabot` and it is located on the desktop.
First type `pwd` to see where you are located (hopefully the default is something like `/Users/YOURUSERNAME`).
Next, type `ls` to see where you can go (hopefully will be a list which includes `Desktop`). 
Type `cd Desktop` to move to the desktop.
Type `ls` to see what files and directories are on the desktop.
Type `cd instabot` to move into the `instabot` directory.
Finally, type `ls` one more time and verify that you see all the project files.

#### Actually create the environment.
Use the command `conda env create -f environment.yml` to create the conda environment.
You should see something like
```
# To activate this environment, use
#
#     $ conda activate instabot
#
# To deactivate an active environment, use
#
#     $ conda deactivate
```

### 5. Put the file with the usernames into the project directory.

### 6. Run the bot

#### Activate the conda environment
Run the command `conda activate instabot`

#### Run the python script
You have to supply some flags to give the bot information it needs to run. 
Some are required and some are optional.
- `--username`: The username or email of the instagram account that will do the following.
- `--password`: The password of the instagram account that will do the following. 
Note: if the password contains an exclamation point, it must be surrounded by single quotes.
- `--account_list_file`: The file containing the usernames to follow. 
There should be a single username on each line and nothing else in the file.
- `--req_per_hour` (optional): How many requests to send per hour. The default is 20.
- `--req_per_day` (optional): The maximum number of requests to send per day. The default is 150.

So, the command to run will be something like `python3 instabot.py --username my_insta_account_123 --password my_s3cret_p@ssword --account_list_file accounts.txt --req_per_hour 25`

When the command is run, a Google chrome window should appear, navigate to instagram, and log in. 
Once it has done so, go back to the command prompt, which should be waiting for you to press ENTER.
As soon as you press ENTER, the bot will begin following accounts.
It will wait between each follow request.
If you need to stop the bot, press `control + C`.