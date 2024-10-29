Homework 3: Flask server thats lets you insert a new row into 'fruit_a' table and show unique fruits in both tables
Members: Ty Herring and Jacob Smith

## Quick Start
### Local Test Setup
1st step - Install Python 3 virtual environment:
```
sudo apt-get install python3-venv
```

2nd step - Create a virtual environment:
```
python3 -m venv python_venv
```

3rd step - Activate virtual environment when you want to run it
```
source python_venv/bin/activate
```

4th step - To fufil all the requirements for the python server, you need to run:
```
pip3 install -r requirements.txt
```

5th step - Start the server using:
```
python3 main.py
```

## Running the Program
To add a new row (5, 'Cherry) into the basket_a:
```
127.0.0.1:5000/api/update_basket_a
```
To show all unique fruits in basket_a and basket_b:
```
127.0.0.1:5000/api/unique
```
