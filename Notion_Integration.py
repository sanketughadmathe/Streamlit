import os

import streamlit as st
from dotenv import load_dotenv
from notion_client import Client

load_dotenv()

api_key = os.environ.get(
    "NOTION_INTEGRATIONV2_TOKEN"
)  # Set this as an environment variable for security

# Initialize Notion client
notion = Client(auth=api_key)


# Function to retrieve data from a page
def get_notion_page_content(page_id):
    response = notion.pages.retrieve(page_id=page_id)
    return response


# Example usage
page_id = "58d5f26367fb4197852a6546c10d9da0"  # Replace with your actual page ID
page_content = get_notion_page_content(page_id)


# Function to extract the page title
def extract_page_title(page_data):
    # Access the title from the properties
    title_property = page_data["properties"].get("title", {})
    if "title" in title_property:
        title = title_property["title"]
        if len(title) > 0:
            return title[0]["plain_text"]
    return "Untitled"


# Add custom CSS for styling
def add_custom_css():
    st.markdown(
        """
        <style>
        .header {
            background-color: #f4f4f4;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            margin-bottom: 20px;
        }
        .card {
            background-color: #ffffff;
            padding: 20px;
            margin-bottom: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }
        .expander {
            background-color: #e9e9e9;
            padding: 10px;
            border-radius: 5px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


# Streamlit UI
def main():
    # Set the page layout
    st.set_page_config(layout="wide", page_title="Notion Page Viewer")

    # Add custom CSS
    add_custom_css()

    # Create a header
    st.markdown(
        '<div class="header"><h1>Notion Page Viewer</h1></div>', unsafe_allow_html=True
    )

    # Display a sidebar for input
    with st.sidebar:
        st.title("Settings")
        page_id = st.text_input(
            "Enter Notion Page ID:", "58d5f26367fb4197852a6546c10d9da0"
        )

    # Main content area
    if page_id:
        # Fetch page content
        content = get_notion_page_content(page_id)

        # Extract and display the title
        title = extract_page_title(content)

        # Create a card to display the title
        st.markdown(
            f'<div class="card"><h2>Page Title: {title}</h2></div>',
            unsafe_allow_html=True,
        )

        # Additional info card
        st.markdown(
            f"""
            <div class="card">
                <p><strong>Created on:</strong> {content['created_time']}</p>
                <p><strong>Last edited:</strong> {content['last_edited_time']}</p>
                <p><strong>Page URL:</strong> <a href="{content['url']}" target="_blank">{content['url']}</a></p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Display full JSON for debugging (optionally hide it in a collapsible section)
        with st.expander("Show JSON Content"):
            st.json(content)


if __name__ == "__main__":
    main()
