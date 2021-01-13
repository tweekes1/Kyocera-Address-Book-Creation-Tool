# Kyocera Address Book Creation Tool

A Python3 tool that I re-wrote to automate the creation
of address books specifically for Kyocera Printer and Scanners. The tool
does not utilize any special technology created by Kyocera, I was able to 
see how the scanners utilized xml files to populate their address books and
created a tool to allow for QoL changes and persistence using a lightweight
sqlite database.

## Prerequistes

You will need a system with python3.6 or higher. No external libraries were used
to create tool although I highly recommend installing [sqlite3](https://www.sqlite.org/index.html) to your machine to see
how database is working or if you would add improvements.

## Usage

```
$> python main.py
```
or
```
$> python3 main.py
```

## Known Issue

Kyocera has a weird way of encoding passwords into their scanners and pasting clear text passwords into the [constant.py](https://github.com/tweekes1/Kyocera-Address-Book-Creation-Tool/blob/master/utils/constants.py) file will not work
**(and is not encouraged).** I found the way that works is to export a copy of your address book using Kyocera Net Viewer and taking the 
encoded string and using that for the password string.