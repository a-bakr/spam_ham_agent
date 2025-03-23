import streamlit as st
from agent import run_agent
import os
import json

# Configure the page
st.set_page_config(
    page_title="Email Spam Detector",
    page_icon="📧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load example emails
def load_example_emails():
    try:
        with open("example_emails.json", "r") as f:
            return json.load(f)
    except Exception as e:
        st.error(f"Failed to load example emails: {e}")
        return []

example_emails = load_example_emails()

# Initialize session state for form fields
if "sender" not in st.session_state:
    st.session_state.sender = ""
if "subject" not in st.session_state:
    st.session_state.subject = ""
if "body" not in st.session_state:
    st.session_state.body = ""

# Sidebar content
with st.sidebar:
    st.image("https://static1.srcdn.com/wordpress/wp-content/uploads/2025/02/batman-from-batman-arkham-game-with-a-fire.jpg", width=200)
    st.title("Alfred's Email Assistant")
    st.markdown("""
    ### How it works
    Alfred, your trusted email assistant, uses advanced AI to:
    
    - 📊 Analyze incoming emails
    - 🚫 Detect spam messages
    - ✍️ Draft professional responses
    
    Simply enter the email details in the form and let Alfred handle the rest.
    """)
    
    # Example emails section in sidebar
    if example_emails:
        st.markdown("### Example Emails")
        example_options = [f"{email['sender']} - {email['subject']}" for email in example_emails]
        selected_example = st.selectbox("Select an example:", options=range(len(example_emails)), 
                                        format_func=lambda i: example_options[i])
        
        if st.button("Load Example"):
            st.session_state.sender = example_emails[selected_example]["sender"]
            st.session_state.subject = example_emails[selected_example]["subject"]
            st.session_state.body = example_emails[selected_example]["body"]
            st.rerun()
    
    st.markdown("---")
    st.markdown("*Powered by LangGraph*")

# Main content
st.title("📧 Email Processor")
st.markdown("Let Alfred analyze your emails and prepare responses")

# Email input form
st.subheader("Email Details")

col1, col2 = st.columns(2)
with col1:
    sender = st.text_input("Sender:", placeholder="Your name", value=st.session_state.sender)
with col2:
    subject = st.text_input("Subject:", placeholder="Meeting Request", value=st.session_state.subject)

body = st.text_area("Email Body:", height=200, placeholder="Enter the email content here...", value=st.session_state.body)

# Clear form button
col1, col2 = st.columns([1, 4])
with col1:
    if st.button("Clear Form"):
        st.session_state.sender = ""
        st.session_state.subject = ""
        st.session_state.body = ""
        st.rerun()

process_button = st.button("Process Email", use_container_width=True)

# Results section
if process_button:
    if not sender or not subject or not body:
        st.error("Please fill in all email fields")
    else:
        with st.spinner("Alfred is analyzing the email..."):
            # Create email data structure
            email_data = {
                "sender": sender,
                "subject": subject,
                "body": body
            }
            
            # Process with agent
            result = run_agent(email_data)
            
            # Display results
            if result.get("is_spam") == True:
                st.subheader("🚫 Spam Detected")
                st.warning("This email has been identified as spam and moved to the spam folder.")
            else:
                st.subheader("✅ Legitimate Email")
                st.success("This appears to be a legitimate email that requires your attention.")
                
                st.markdown("### Draft Response")
                st.info(result.get("draft_response", "No draft response generated."))

if __name__ == "__main__":
    print("Starting Alfred's Email Assistant...")
    # Streamlit handles server initialization when running the script 