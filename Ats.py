
import os
import streamlit as st
import pandas as pd
import re
import numpy as np
import matplotlib.pyplot as plt
from tabulate import tabulate
import subprocess
import openpyxl
from PIL import Image


data = pd.read_excel("DPSD- Comprehensive vaiva Quiz details.xlsx")
# data[:]

ques=[]
students=len(data["First name"].value_counts())
percent = (30/100)
to_calculate = int(students*percent)
regex = "Q\. ([1-9]|[1-9][0-9]{1,2}|1000)(.+)\.00$"
v=data.columns.ravel()
for i in v:
    match = re.match(regex, i)
    if match:
        ques.append(i)
# print(ques)

dict_questions = {}

for ques_val in ques:
        lst=[]
        s=data.loc[:students, ques_val]
        s=np.array(s.values)

        for filter_none in s:
            filter_none = str(filter_none)
            if filter_none.isdigit():
                lst.append(int(filter_none))
            else:
                lst.append(0)
        dict_questions[ques_val]=lst

# print(dict_questions)

Fascilation_index = []
Descrimination_index = []

for ques_no in ques:
    sum_first = sum(dict_questions[ques_no][:to_calculate])
    sum_last = sum(dict_questions[ques_no][-to_calculate:])

    fac = ((sum_first+sum_last)/(2*to_calculate*max(dict_questions[ques_no])))
    Fascilation_index.append(fac)

    Des = ((sum_first-sum_last)/to_calculate*max(dict_questions[ques_no]))
    Descrimination_index.append(Des)


total_indices = [sum(pair) for pair in zip(Fascilation_index, Descrimination_index)]

output_data = pd.DataFrame({
    "Questions": ques,
    "Fascilitation_index": Fascilation_index,
    "Discrimination_index": Descrimination_index,
    "total_indices": total_indices
})

# Limit Total Indices to two decimal places
output_data['total_indices'] = output_data['total_indices'].round(2)

# Display the table
# print(tabulate(output_data, headers="keys", tablefmt='fancy_grid', numalign='center', stralign='left', colalign=('center', 'center', 'center')))

# Save plots to a file (optional)
for i, lst in enumerate([Fascilation_index, Descrimination_index, total_indices]):
    fig, ax = plt.subplots()
    ax.plot(lst)
    ax.set_title(f"Index graph {i + 1}")
    ax.set_ylabel("Question")
    ax.set_xlabel("Index")
    # plt.savefig(f"C:\\Users\\syed\\OneDrive\\Desktop\\Final Project\\index_graph_{i + 1}.png")
    # Show the plots
    # plt.show()
  
data = None 

def main():
    st.title("Excel Data Analyzer")

    uploaded_file = st.file_uploader("Upload an Excel file", type=["xlsx", "xls"])

    if uploaded_file is not None:
        data = pd.read_excel(uploaded_file)
        st.success("Data loaded successfully!")
        analyze_data(data)
    st.markdown("Thank you for using my app! 👋")

st.header("Test Item Analaysis")

def get_unique_terms(data):
    unique_terms = []

    for column in data.columns:
        unique_values = data[column].unique()
        if len(unique_values) > 1:
            unique_terms.append(column)

    return unique_terms

def analyze_data(data):
    unique_terms = get_unique_terms(data)

    if not unique_terms:
        st.warning("No unique terms found in the data.")
        return

    selected_term = st.selectbox("Select a term for analysis:", unique_terms)
    selected_value = st.selectbox(f"Select {selected_term}:", data[selected_term].unique())

    result_data = data[data[selected_term] == selected_value]
    st.subheader(f"{selected_term} - {selected_value} Analysis")

     # Print Fascilation_index, Descrimination_index, and total_indices
    # st.write("Fascilation Index:", Fascilation_index)
    # st.write("Discrimination Index:", Descrimination_index)
    # st.write("Total Indices:", total_indices)
    st.write(output_data.style.format({'Total Indices': "{:.2f}"}))

    st.dataframe(result_data)
img = Image.open("C:\\Users\\syed\\Downloads\\A picture of a cat playing.jpg")
#Proceed with processing the image
st.image(img, caption="Welcome to Ats app!", width=700, channels="RGB")
st.header("Test Item Analaysis")
if __name__ == "__main__":
    main()
