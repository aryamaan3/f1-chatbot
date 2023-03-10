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

## Explication du chatbot

Notre chatbot est en rapport avec la Formula 1. Il va répondre aux questions sur la saison actuelle. Ces questions peuvent être en rapport avec les pilotes, les écuries ou les courses.

Nous avons utilisé deux outils:
- Ergast (http://ergast.com/mrd/) qui est une API en libre accès recensant les informations sur la F1
- Spacy pour la partie NLP

Tout d'abord on effectue une requête sur l'API et on récu^père l'ensemble des informations qui nous intéresse. Pour certains fonctions (comme avoir le gagnant de la dernière course) nous avons dû faire un autre appel à l'API. Lorsque vous allez poser votre question, le chatbot fera soit appel à l'APi ou il va récupérer l'information déjà stockée.

Pour le traitement des questions nous avons utilisé un mélange de if avec des mots en tant que "flag" (si on trouve un mot ou une combinaison on répond d'une certaine manière) et du POS tagging de spacy. Par exemple si on détecte une PERSON (Prénom Nom) on sait qu'on parle d'un pilote et on va récupérer ses informations.

Voici un exemple de questions:
- Can you give me the race schedule for the next Grand Prix?
- Who won the last race?
- Tell me about Lewis Hamilton
- What team does Charles Leclerc drive for?
- What is the location of the Australian Grand Prix?
- Can you give me information about the Silverstone Circuit?
- What is the points standing for the current season?
- When is the next race?
What is the previous race ?
