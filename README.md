# DoordashOrderScraper
automatically collects group order history for an account over a set period, how much each person spent, and all fees cost. can export to json or csv.

## instalation
first, go to the location you want to install the script, and clone the repo. all files will stay in this folder, so put it somewhere nice
```sh
git clone https://github.com/popcornman209/DoordashOrderScraper.git
cd DoordashOrderScraper
```
then, create a python venv called "venv" in the folder. this is optional if your fine installing packages system wide.
```sh
python -m venv venv
source venv/bin/activate
```
now install the required libraries
```sh
pip install -r requirements.txt
```
if you want to open the app via "runLinux" or "runMacOS" run this command
```sh
chmod a+x runMacOS.command runLinux.sh
```

## running the program
> [!WARNING]
> you need chrome installed, for some reason a google meets update has broken this script.<br />
> a solution to this is downloading ungoogled-chromium, you can tell this script to use it by putting its binary path in `configs/chromiumPath.txt` or in the orders menu in the gui.<br />
to run the program with a gui, doubleclick the "runLinux" or "runMacOS" file or the below command. if runMacOS doesnt open a terminal, right click and click open with, then other. then, change "recommended applications" to all, and select applications/utilities/terminal.app.<br>
if you want to start it in a tty instead, run:
```sh
venv/bin/python main.py
```
or if your not using a venv just:
```sh
python main.py
```
if you do not want to use the gui, see the arguments below for how to run this in a tty as a headless script.

### program arguments
`--help` is for bringing up the help page, obviously lol<br>
`--headless` will run the program in a headless configuration, fully in a tty.<br>
`--days x` will make the script get orders x days in the past. this is needed if tryng to run the script automatically, as otherwise it will try and get an input of which orders to count.<br>
`--force-display-browser` forces the browser to display when in headless mode<br>
`--output x` saves the data to a file, formatted as a json by default. only works in headless mode<br>
`--output-type x`: set to 'json' or 'csv' to say output type, also only in headless

## configs
you will be able to edit these settings in the gui, but without that you can do it manually.

### configs/loginInfo.json
this is fairly self explanatory, setting "autoLogin" to true will automatically log in, otherwise it will wait until you do so yourself.

setting DDusername and DDpassword is for your doordash username and password, 2 factor authentication has not been programmed in, so you will must turn that off.
