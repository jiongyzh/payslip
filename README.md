# payslip
# This is a console application created for generating payslips for employees

## Getting started

To setup the test environment
Go to the directory where Dockerfile sits and run
```
docker build -t payslip .
```

To run unit tests
```
docker run -it payslip python -m unittest payslip/tests/payslip.py
```
* Need to cover more methods in future

To run the application
```
docker run -it  payslip python manage.py
```
* Make sure run 'Migrate' command first to create the table and import the data


###
You can also directely run this application on your local if Python3 is installed.
Just got to the directory where manage.py sits and run
```
python -m unittest payslip/tests/payslip.py
python manage.py
```
