# travel-assistant

## Description

A chatbot that provides more information about things to do and see in some area. The chatbot can process specific dates and areas and general user intent using NLP. It looks at static touristic places as well as dynamic one-time events and the current weather. It then formulates a sensible answer using a local language model. Admin users can also insert events themselves and even prioritize certain events. Only sources with free licenses or with a free tier subscription were used.

## Steps to run code: - Jad, Ruben

- **Setup Database**
    - **Install MongoDB**: https://www.mongodb.com/try/download/community
    - Create default connection. 

- **Setup Backend**
    - `cd backend`
    - **Create virtual environment**: `python -m venv venv`
    - **Activate virtual environment**: 
    - macOS/Linux: `source venv/bin/activate`
    - Windows: `venv\Scripts\activate`
    - **Install dependencies**: `pip install -r requirements.txt`    

- **Setting up Frontend**:
    - `cd frontend`
    - `npm install`
    - `npm run build-api` - run each time you do changes to API routes

- **Running Backend**: 
    - `cd backend`
    - `fastapi dev app/main.py`

- **Running Frontend**:
    - `cd frontend`
    - `npm start`
