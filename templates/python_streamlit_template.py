"""
{project_name} - Streamlit Application
Created: {date}
"""

import streamlit as st

def main():
    st.set_page_config(page_title="{project_name}", page_icon="🚀")

    st.title("{project_name}")
    st.write("Welcome to your new Streamlit application!")

    # Sidebar
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox("Choose a page", ["Home", "About"])

    if page == "Home":
        st.header("Home Page")
        st.write("This is the home page of your application.")

    elif page == "About":
        st.header("About")
        st.write("Created with ContextCraft - Enhanced AI Project Generator")

if __name__ == "__main__":
    main()
