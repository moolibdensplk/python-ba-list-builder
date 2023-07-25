# python-ba-list-builder
Python + PYQT5 Warhammer 40K Boarding Actions List Builder

## Requirements
This tool has been written using:

* Python 3.11.4
* PyQT5 (5.15.9)
* pyqt5-tools (5.15.9.3.3)
* * PyQT5 Designer (provided by pip package: pyqt5-tools)

## How To Install

* Install Python 3.11.4 first, I used `pyenv` (on MacOS X)
```
pyenv install 3.11.4
```

* Create a virtual env using pyenv
```
pyenv virtualenv 3.11.4 list_builder_app
```

* Activate the env
```
pyenv activate 3.11.4/envs/list_builder_app
```

* Install all dependencies
```
pip install --upgrade pip
pip install pyqt5
pip install pyqt5-tools
```

* checkout the code from the repo
```
git clone git@github.com:moolibdensplk/python-ba-list-builder.git 
```

or download it as ZIP and uncompress...

```
cd <folder with the code>
```

* Runthe code:
```
python main.py
```

## DISCLAIMER :
This app is not even an ALPHA version !
Purely EXPERIMENTAL code.
I take NO RESPONSIBILITY for any issues - use it on your own.
If you don't like something - feel free to fork the repo and write a better version :)

## Things that work in the app:
* Adding / Removing units from army list
* Using "Validate" button to check if your list is valid
* Some basic sanity checking when attempting to add a unit to the list (like cost vs remaining cost, units where you can increase size like Krotox Riders), unit dependencies prior to adding )
* Removing units (selected unit!) from list
* clearing the list

## Things that DO NOT work yet (not coded yet)
* Saving the list as a file
* Openning and loading in an existing list

