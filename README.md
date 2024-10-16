# travel-assistant

# Steps to run code: - Jad 

- **Setup spaCy Language Model**: 

    - `python -m spacy download en_core_web_sm`

- **Setup Backend**
    - `cd backend`
    - **Create virtual environment**: `python -m venv venv`
    - **Install dependencies**: `pip install -r requirements.txt`
    - **Activate virtual environment**: 
    - macOS/Linux: `source venv/bin/activate`
    - Windows: `venv\Scripts\activate`

- **Setting up Frontend**:
    - `cd frontend`
    - `npm install`

- **Running Backend**: 
    - `cd backend`
    - `uvicorn app.main:app --reload`

    
- **Running Frontend**:
    - `cd frontend`
    - `npm start`
