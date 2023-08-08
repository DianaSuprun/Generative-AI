# Generative-AI

The full project will have such sturture:
    ├──  model                - this folder contains all database models.
    │   ├── __init__.py         - init file for the package.
    │   ├── fine_tuning.py      - this file fine-tune chat gpt model.
    │   ├── Chatbot.py          - this file contains logic of communication with gpt model.
    │   ├── Preparation.py      - this file contains preparation for communication with gpt model.
    |   └── Order.py            - association table for Preparation and Chatbot entities.  
    │   
    ├── settings                - here you can store different constant values, connection parameters, etc.
    │   └── constants.py        -  multiple constants storage for their convenient usage.
    │ 
    ├── core                    - folder, which contains core application components.
    │   ├── __init__.py         - initializing our app.
    │   └── routes.py           - application routes (predefined commands).
    │
    ├── tests                   - this folder contains test cases for testing the correctness of operation handlers.
    │   
    ├── run.py                  - application run file.
    |
    └── requirements.txt		- list of used libraries 
