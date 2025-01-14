import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF

# Function to load dataset
def load_data(file):
    return pd.read_csv(file)

# Function to generate summary statistics
def generate_summary(data):
    return data.describe(include='all')

# Function to report missing values
def report_missing_values(data):
    return data.isnull().sum()

# Function to plot histogram
def plot_histogram(data, column):
    plt.figure(figsize=(8, 6))
    data[column].hist(bins=20)
    plt.title(f'Histogram for {column}')
    plt.xlabel(column)
    plt.ylabel('Frequency')
    plt.tight_layout()
    plt.savefig(f'{column}_hist.png')  # Save plot as an image
    st.image(f'{column}_hist.png')  # Display plot in Streamlit
    plt.close()

# Function to create a PDF report
def create_pdf_report(data, summary, missing_values, file_name="report.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # Title
    pdf.cell(200, 10, txt="Data Analysis Report", ln=True, align='C')
    
    # Summary Statistics
    pdf.cell(200, 10, txt="Summary Statistics", ln=True, align='L')
    for col in summary.columns:
        pdf.cell(200, 10, txt=f'{col}: {summary[col].to_dict()}', ln=True)
    
    # Missing Values
    pdf.add_page()
    pdf.cell(200, 10, txt="Missing Values Report", ln=True, align='L')
    for col, val in missing_values.items():
        pdf.cell(200, 10, txt=f'{col}: {val} missing values', ln=True)
    
    # Save the PDF
    pdf.output(file_name)
    return file_name

# Streamlit App
st.title("Data Analysis and Reporting Tool")

# Upload CSV File
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    # Load data
    data = load_data(uploaded_file)
    st.write("Dataset Preview", data.head())
    
    # Generate summary statistics
    summary = generate_summary(data)
    st.write("Summary Statistics", summary)
    
    # Report missing values
    missing_values = report_missing_values(data)
    st.write("Missing Values", missing_values)
    
    # Generate histograms for numeric columns
    st.write("Histograms for Numeric Columns")
    for col in data.select_dtypes(include=['number']).columns:
        plot_histogram(data, col)
    
    # Generate PDF report
    if st.button("Generate PDF Report"):
        report_file = create_pdf_report(data, summary, missing_values)
        with open(report_file, "rb") as file:
            st.download_button(
                label="Download PDF Report",
                data=file,
                file_name="report.pdf",
                mime="application/pdf"
            )
        st.success("Report generated successfully!")
