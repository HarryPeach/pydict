![Python application](https://github.com/HarryPeach/pydict/workflows/Python%20application/badge.svg)
# pydict
## A simple commandline dictionary program

### Setup
1. Install python3 and pip
2. Run ```pip install -r requirements.txt```
3. Run pydict using ```python3 -m pydict```

Alternatively:
1. Install python3 and pip
2. Run ```python3 -m pip install .``` in the source directory
3. Run pydict using ```python3 -m pydict```

> IMPORTANT: If you don't provide api key and app id information throught arguments you must set the following environment variables:
   1. ```PYDICT_API_KEY``` (Your Oxford Dictionaries API Key)
   2. ```PYDICT_APP_ID``` (Your Oxford Dictionaries App ID)

### Examples

Find the definition of the word "ace":
```sh
python3 -m pydict ace
```
```
a playing card with a single spot on it, ranked as the highest card in its suit in most card games
```

Find the definition of the word "assist" through piped input (Unix mode):
```sh
echo assist | python3 -m pydict -x
```
```
help (someone), typically by doing a share of the work
```

Find all definitions of the word "aid" as well as full definition data:
```sh
python3 -m pydict aid -a -v
```
```
aid • /eɪd/
help, typically of a practical nature
a grant of subsidy or tax to a king or queen.
```

### Testing
Each build is automatically tested, but you can run the tests yourself by using ```python3 -m test```