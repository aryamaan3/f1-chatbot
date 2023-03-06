# f1-chatbot

## Instructions to run the chatbot

1. Create a virtual environment

[venv](https://www.freecodecamp.org/news/how-to-setup-virtual-environments-in-python/) or [pipenv](https://pipenv.pypa.io/en/latest/)

2. Create a requirements.txt file

`pip freeze > requirements.txt`

3. Install the requirements

`pip install -r requirements.txt`

4. Download the spacy model

`python -m spacy download en_core_web_sm`

5. Run the chatbot

`python main.py`