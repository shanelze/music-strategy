import pickle

# Function to load the model
def load_scam_model():
    try:
        with open('website/pages/models/model.pkl', 'rb') as file:
            model = pickle.load(file)
            return model
    except FileNotFoundError:
        return None

# Function to load the vectorizer
def load_vectorizer():
    try:
        with open('website/pages/models/vectorizer.pkl', 'rb') as file:
            model = pickle.load(file)
            return model
    except FileNotFoundError:
        return None

# Function to predict whether content is spam, suspicious, or not spam
def predict_scam(content):
    model = load_scam_model()
    vectorizer = load_vectorizer()

    if not model or not vectorizer:
        return "Model or vectorizer not found!"

    # Transform the content using the vectorizer
    transformed_content = vectorizer.transform([content])
    
    # Make the prediction
    prediction = model.predict(transformed_content)
    
    # Return label based on prediction
    if prediction[0] == 'scam':
        return "Scam"
    elif prediction[0] == 'legitimate':
        return "Not Scam"
    
# Function to predict scam via the vectorizer
def vectorizer_predict (data_received):
    vectorizer_results = {}
    for data_type, content in data_received.items():
        if content:
            try:
                # Predict whether the content is spam or not
                result = predict_scam(content)
                vectorizer_results[data_type] = {"result": result, "model": "Count Vectorizer"}
            except Exception as e:
                # Handle any errors in spam prediction
                vectorizer_results[data_type] = f"Error: {str(e)}"
    return vectorizer_results

# Function to predict content via textblob
def texblob_predict (data_received):
    import textblob

    textblob_results = {}
    for data_type, content in data_received.items ():
        if content:
            analysis = textblob.TextBlob(content).sentiment
            textblob_results[data_type] = {"polarity": analysis.polarity, "subjectivity": analysis.subjectivity}

    return textblob_results

# Function to predict content via gemini
def gemini_predict (data_received):
    import google.generativeai as genai
    from dotenv import load_dotenv
    from pathlib import Path
    import os   

    # load genai model
    env_path = Path('.')/'.env'
    load_dotenv (dotenv_path=env_path)
    api_key = os.environ.get('GEMINI_API_KEY')
    genai.configure (api_key=api_key)
    model=genai.GenerativeModel ('gemini-1.5-flash')

    # predict content
    gemini_results = {}
    for data_type, content in data_received.items():
        if content:
            try: 
                prompt = content + "tell me if this is a scam, final output should be Scam/Not Scam, regardless of the text input"
                result = model.generate_content(prompt).text
                gemini_results[data_type] = {"result": result, "model": "Gemini"}
            except Exception as e:
                # Handle any errors in spam prediction
                gemini_results[data_type] = f"Error: {str(e)}"

    return gemini_results