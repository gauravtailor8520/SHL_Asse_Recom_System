import streamlit as st
import pandas as pd
from subfolder.query_functions import query_handling_using_LLM_updated# Assuming this import is correct

# Function to set background image
def set_background(image_url):
    """
    Sets a background image for the Streamlit app.
    """
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("{image_url}");
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        /* Adjust text & element backgrounds for better readability on an image */
        .stTextInput > div > div > input {{
            background-color: rgba(0, 0, 0, 0.7); /* Black semi-transparent background for search input */
            color: #FFFFFF; /* White text for search input */
        }}
        .stTextInput > div > div > input::placeholder {{
            color: #CCCCCC; /* Lighter placeholder text for dark background */
        }}
        .stButton > button {{
            background-color: rgba(255, 255, 255, 0.8); /* Original background for button */
            color: #333; /* Original text color for button */
        }}
        /* Ensure Streamlit's default text color is readable */
        body, .stMarkdown, .stText, .stAlert  {{
            color: #FFFFFF; /* Default to white text if background is dark */
        }}
        /* Specific overrides if needed, e.g., for warnings or errors */
        .st-emotion-cache-1wmy9hl e1nzilvr5, .st-emotion-cache-rptjb5 e1nzilvr5 {{ /* Selectors for st.warning/st.error text */
            color: #333 !important; /* Or a color that contrasts with their specific backgrounds */
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

st.set_page_config(page_title="SHL Assessment Recommendation System", layout="centered")

# --- SET BACKGROUND IMAGE ---
# IMPORTANT: Replace this URL with your desired background image URL
BG_IMAGE_URL = "https://images.unsplash.com/photo-1531297484001-80022131f5a1?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1770&q=80" # Example dark abstract background
set_background(BG_IMAGE_URL)

st.markdown(
    """
    <div style='background-color: rgba(0, 0, 0, 0.5); padding: 15px; border-radius: 10px;'>
        <h2 style='text-align: center; color: #66C2FF;'>Assessment Recommendation System</h2>
        <h3 style='text-align: center; color: #66C2FF;'>SHL</h3>
        <h4 style='text-align: center; color: #E0E0E0;'>Find the best assessments based on your query using AI!</h4>
    </div>
    <hr style="border: 1px solid #555; margin-top: 20px; margin-bottom: 20px;">
    """,
    unsafe_allow_html=True
)

query = st.text_input("🔍 Enter your search query here:", placeholder="e.g. Python SQL coding test")

# Center the button using columns
col1, col_button, col3 = st.columns([2, 1.5, 2]) # Adjust ratios as needed for centering

with col_button:
    search_clicked = st.button("Search", use_container_width=True)

# On search
if search_clicked:
    if query.strip() == "":
        st.warning("Please enter a valid query.")
    else:
        with st.spinner("🤖 Thinking... Fetching the best matches for you!"):
            try:
                # Get results
                df = query_handling_using_LLM_updated(query)

                if isinstance(df, pd.DataFrame) and not df.empty:
                    if 'Score' in df.columns:
                        df = df.drop(columns=['Score'])

                    if "Duration" in df.columns:
                        df = df.rename(columns={"Duration": "Duration in mins"})

                    display_cols = ["Assessment Name", "Skills", "Test Type", "Description", "Remote Testing Support", "Adaptive/IRT", "Duration in mins", "URL"]
                    # Use .copy() to avoid SettingWithCopyWarning
                    df_display = df[[col for col in display_cols if col in df.columns]].copy()

                    # Make URLs clickable
                    if 'URL' in df_display.columns:
                        df_display.loc[:, 'URL'] = df_display['URL'].apply(
                            lambda x: f"<a href='{x}' target='_blank' style='color: #87CEFA;'>🔗 View</a>" if pd.notna(x) else ""
                        )

                    st.success("✅ Here are your top assessment recommendations:")

                    # Build styled HTML table (adjusted for background image)
                    table_html = """
                    <style>
                        table.custom-table {
                            width: 100%;
                            border-collapse: collapse;
                            font-family: Arial, sans-serif;
                            background-color: rgba(20, 20, 20, 0.85); /* Darker semi-transparent background */
                            border-radius: 8px;
                            overflow: hidden; /* Ensures border-radius clips content */
                            box-shadow: 0 4px 8px rgba(0,0,0,0.3);
                        }
                        table.custom-table thead {
                            background-color: rgba(0, 0, 0, 0.9); /* Even darker header */
                            color: #E0E0E0;
                        }
                        table.custom-table th, table.custom-table td {
                            border: 1px solid #555;
                            padding: 12px;
                            text-align: left;
                            vertical-align: top;
                            color: #D0D0D0; /* Light gray text */
                        }
                        table.custom-table tr:nth-child(even) {
                            background-color: rgba(40, 40, 40, 0.8);
                        }
                        table.custom-table tr:nth-child(odd) {
                            background-color: rgba(50, 50, 50, 0.8);
                        }
                        table.custom-table a {
                            color: #87CEFA; /* Light blue for links */
                            text-decoration: none;
                        }
                        table.custom-table a:hover {
                            text-decoration: underline;
                        }
                    </style>
                    <table class="custom-table">
                        <thead>
                            <tr>
                    """

                    for col in df_display.columns:
                        table_html += f"<th>{col}</th>"
                    table_html += "</tr></thead><tbody>"

                    for _, row in df_display.iterrows():
                        table_html += "<tr>"
                        for cell in row:
                            table_html += f"<td>{cell}</td>"
                        table_html += "</tr>"

                    table_html += "</tbody></table>"

                    st.markdown(table_html, unsafe_allow_html=True)

                else:
                    st.warning("😕 No assessments matched your query. Try rephrasing it!")

            except Exception as e:
                st.error(f"🚨 Something went wrong: {e}")
