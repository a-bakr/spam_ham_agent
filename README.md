# Alfred's Email Assistant

A modern Streamlit interface for the Batman-themed LangGraph email assistant.

![Alfred Email Assistant](https://upload.wikimedia.org/wikipedia/commons/thumb/1/1f/Batman_%28black_background%29.jpg/320px-Batman_%28black_background%29.jpg)

## Features

-   📧 Email spam detection using LangGraph agent
-   ✍️ Automated response drafting for legitimate emails
-   🔵 Modern UI with blue color palette
-   🦇 Batman-themed interface with Alfred as your assistant

## Requirements

-   Python 3.8+
-   OpenAI API key

## Installation

1. Clone this repository:

    ```
    git clone <repository-url>
    cd <repository-directory>
    ```

2. Install the required dependencies:

    ```
    pip install -r requirements.txt
    ```

3. Set up your environment variables:
    ```
    cp .env.example .env
    ```
    Edit the `.env` file to add your OpenAI API key.

## Running the App

Start the Streamlit app:

```
python app.py
```

or

```
streamlit run app.py
```

The app will be available at http://localhost:8501 in your web browser.

## Usage

1. Enter the email sender address in the form
2. Add the email subject
3. Type or paste the email body
4. Click "Process Email" to analyze the content

Alfred will:

-   Check if the email is spam
-   Draft a professional response if the email is legitimate
-   Display the results in a clean, organized interface

## How It Works

The app uses a LangGraph agent that:

1. Reads the email
2. Classifies it as spam or legitimate
3. Drafts a response for legitimate emails
4. Presents everything in a user-friendly interface
