import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os
import json
import joblib
from enum import Enum
from io import BytesIO, StringIO
from typing import Union


from Bio import SeqIO
from Bio.SeqUtils.ProtParam import ProteinAnalysis
from sequence_preprocessing import Virus
from structures import *
# To ensure dataframe is loaded
input_accepted = False
#FILE_TYPES = ["text", "py", "png", "jpg","fasta","csv"]


class FileType(Enum):
    """Used to distinguish between file types"""

    IMAGE = "Image"
    TEXT = "text"
    PYTHON = "Python"
    FASTA = "fasta"
    CSV = "csv"

st.title('Virus DNA/RNA Testing Service')
st.subheader('\n\nIt is estimated that there are millions of viruses that exist on Earth, of which hundreds of thousands possible infect mammals.\
      However, the list of known viruses is substantially smaller than all the viruses that exists that are pathogenic to humans.\
      To further complicate this issue, many viruses can jump between species after a period of lying dormant and mutating.\
      \n\nIn the advent of our current recent pandemic from COVID-19, there is an urgency to develop technology that can identify if a virus will be dangerous to humans in advance.\
      This app allows you to upload a virus sequence(s) - either DNA or RNA and in either nucleotide or protein format - to test for such virulency.')
st.markdown('---')

@st.cache(allow_output_mutation=True)
def load_virus_data_test():
    test_file = 'ui_samples.fasta'
    test_virus = Virus()
    virus_df = test_virus.build_virus_dataframe(test_file, 'nucleotide', 'fasta',True)
    input_accepted = True
    return virus_df

@st.cache(allow_output_mutation=True)
def load_virus_data(input_file, sequence_type, file_type):
    test_virus = Virus()
    virus_df = test_virus.build_virus_dataframe(input_file, sequence_type, file_type, True )
    input_accepted = True
    return virus_df


@st.cache(allow_output_mutation=True)
def load_virus_data_text(input_file, sequence_type):
    test_virus = Virus()
    virus_df = test_virus.build_virus_dataframe(input_file, sequence_type, 'text', False )
    input_accepted = True
    return virus_df

# @st.cache(allow_output_mutation=True)
def predict_virus_class(df):
    etc = joblib.load('virus_extra_trees_model.joblib')
    predictions = etc.predict(virus_df[model_cols])
    return predictions

@st.cache(allow_output_mutation=True)
def load_misclassification():
    log_file = open('misclassification_log.json', 'r')
    log_data = json.load(log_file)
    return log_data

def log_misclassification(logs, change):
    updated = False
    if len(logs['Data'])==0:
        logs['Data'].append(change)
        updated = True
    else:
        log_ids = [x['id'] for x in logs['Data']]
        if change['id'] not in log_ids:
                logs['Data'].append(change)
                updated = True
    if updated == True:
        with open('misclassification_log.json', 'w') as out_file:
            json.dump(logs, out_file)

# https://discuss.streamlit.io/t/are-you-using-html-in-markdown-tell-us-why/96/30
# https://discuss.streamlit.io/t/colored-boxes-around-sections-of-a-sentence/3201/2
@st.cache(allow_output_mutation=True)
def set_data_loaded():
    input_accepted = False

def check_file(file,file_type):
    if file == None:
        st.warning('No file selected.')
    # elif file.empty():
    #     st.warning('Blank File selected.')
    else:
        content = file.getvalue()
        if not content:
            st.warning('Blank File selected.')
        else:  
            type = get_file_type(file).value
            if(type == file_type):
                return True
            else:
                st.warning('Uploaded file type and FileType don\'t match.')  
    return False

#Validating fileType
def get_file_type(file: Union[BytesIO, StringIO]) -> FileType:
    content = file.getvalue()
    if isinstance(file, BytesIO) and content:
        return FileType.IMAGE
    elif (
        content.startswith('"""')
        or "import" in content
        or "from " in content
        or "def " in content
        or "class " in content
        or "print(" in content
    ):
        return FileType.PYTHON
    elif (content.startswith('>')):
        return FileType.FASTA
    else:
        return FileType.CSV


def local_css(file_name):
    with open(file_name) as f:
        st.markdown('<style>{}</style>'.format(f.read()), unsafe_allow_html=True)

def display_aa_chart(df):
    amino_cols = [col for col in virus_df.columns.tolist() if col.__contains__('amino')]
    t_virus_df = df[df['id']==virus_select][amino_cols].T
    st_virus_df = t_virus_df.stack().reset_index()
    st_virus_df.columns = ['amino_acid','id','value']

    amino_fig = px.bar(st_virus_df, x='amino_acid', y='value', height=300)
    # amino_fig.update_layout(yaxis=dict(range=[0,1]))
    st.plotly_chart(amino_fig)

def display_sunburst(df):
    sun_group = pd.DataFrame(df.groupby(by=['class','id','sequence_length','gc_content'])['nucleotide_sequence'].size())
    sun_group.reset_index(inplace=True)
    sun_group.rename(columns={'nucleotide_sequence':'count'}, inplace=True)
    sun_fig = px.sunburst(sun_group, path=['class', 'id'], values='count',
                    color='sequence_length', hover_data=['class'],
                    color_continuous_scale='RdBu',
                    color_continuous_midpoint=np.average(sun_group['sequence_length'], weights=sun_group['count']))
    st.plotly_chart(sun_fig)
    # sun_fig.show()    


local_css('style.css')

# SPECIFY COLUMNS USED BELOW
model_cols = ['gc_content','molecular_weight','aromaticity','instability_index','amino_acid_A','amino_acid_C','amino_acid_D',
'amino_acid_E','amino_acid_F','amino_acid_G','amino_acid_H','amino_acid_I','amino_acid_K','amino_acid_L','amino_acid_M','amino_acid_N',
'amino_acid_P','amino_acid_Q','amino_acid_R','amino_acid_S','amino_acid_T','amino_acid_V','amino_acid_W','amino_acid_Y']
ms_cols = ['id', 'description', 'gc_content', 'molecular_weight', 'aromaticity', 'instability_index', 'nucleotide_sequence', 'protein_sequence', 'sequence_length', 'class']
metric_cols = ['gc_content','molecular_weight','aromaticity','instability_index', 'sequence_length']

# UPLOAD DATA AND CLASSIFY VIRULENCY - TEST CASE
# virus_df = load_virus_data_test()
# virus_df['class'] = predict_virus_class(virus_df)
# amino_cols = [col for col in virus_df.columns.tolist() if col.__contains__('amino')]
logs = load_misclassification()

# ALLOW USER TO SELECT SPECIFIC VIRUS FROM UPLOAD
# FILE UPLOAD CODE BLOCK HERE
st.sidebar.subheader('Please provide Input')
input_type = st.sidebar.radio("Input Type", options=["File upload","Text"])

if input_type == 'File upload':
    st.sidebar.subheader('Virus Sequence Type')
    sequence_type = st.sidebar.radio("Sequence Type", options=["nucleotide","protein"])
    st.sidebar.subheader('Virus Upload')
    uploaded_file = st.sidebar.file_uploader("Choose a file", type=[FileType.FASTA.value, FileType.CSV.value])
    file_type = st.sidebar.radio("File Type", options=[FileType.FASTA.value, FileType.CSV.value])
    type_check = check_file(uploaded_file,file_type)
    if uploaded_file is not None and file_type and sequence_type and type_check:
        virus_df = load_virus_data(uploaded_file, sequence_type, file_type)
        if virus_df is not None:
            st.write('File successfully uploaded!')
            virus_df['class'] = predict_virus_class(virus_df)
            input_accepted = True
        else:
            st.warning(f'Sequence file contents and sequence type {sequence_type} do not match')
    else:
        set_data_loaded()

elif input_type == 'Text':
    st.sidebar.subheader('Text Input')
    user_input = st.sidebar.text_area("Enter sequence")
    st.sidebar.subheader('Virus Sequence Type')
    sequence_type = st.sidebar.radio("Sequence Type", options=["nucleotide","protein"])
    if user_input and sequence_type:
        virus_df = load_virus_data_text(user_input,sequence_type)
        if virus_df is not None:
            virus_df['class'] = predict_virus_class(virus_df)
            input_accepted = True
    else:
        st.warning('Enter sequence in textbox and click outside the box!')
        set_data_loaded()
else: 
    set_data_loaded()

if input_accepted:
    st.sidebar.markdown('---')
    st.sidebar.subheader('Virus Selection')
    virus_select = st.sidebar.selectbox('Which virus would you like to inspect?',virus_df['id'].sort_values().values)
    st.sidebar.markdown('---')

    # ALLOW USER TO SELECT SPECIFIC VISUALS
    st.sidebar.subheader('Visual Components')
    show_sunburst = st.sidebar.checkbox('Show Virus Sunburst')
    show_aa_chart = st.sidebar.checkbox('Show Amino Acid %')
    show_prot_scale = st.sidebar.checkbox('Show Protein Scale')
    #st.write(show_prot_scale)
    if show_prot_scale:
        wsl = st.sidebar.slider("Window Length", 1, 10, 7)
        esl = st.sidebar.slider("Edge Weight", .1, 1.0, .1)
    show_df = st.sidebar.checkbox('Show Raw Data')

    # BEGIN DISPLAYING GLOBAL INFORMATION FROM UPLOADED FILE (E.G. SUNBURST CHART)
    if show_sunburst:
        st.subheader('Classification Diagram of Uploaded Sequences')
        display_sunburst(virus_df)
        st.markdown('---')

    # BEGIN DISPLAYING INFORMATION RELATED TO SELECTED VIRUS (E.G. METRICS AND AMINO ACIDS)
    st.subheader('Virus Details')
    st.markdown(f"<div><span class='bold'>Name/ID:</span> {virus_select}</div>", unsafe_allow_html=True)
    temp_desc = virus_df[virus_df['id']==virus_select]['description'].iloc[0]
    st.markdown(f"<div><span class='bold'>Description:</span> {temp_desc}</div>", unsafe_allow_html=True)
    temp_gc = virus_df[virus_df['id']==virus_select]['gc_content'].iloc[0]
    st.markdown(f"<div><span class='bold'>GC Content:</span> {temp_gc}</div>", unsafe_allow_html=True)
    temp_arom = virus_df[virus_df['id']==virus_select]['aromaticity'].iloc[0]
    st.markdown(f"<div><span class='bold'>Aromaticity:</span> {temp_arom}</div>", unsafe_allow_html=True)
    temp_ii = virus_df[virus_df['id']==virus_select]['instability_index'].iloc[0]
    st.markdown(f"<div><span class='bold'>Instability Index:</span> {temp_ii}</div>", unsafe_allow_html=True)
    temp_mw = virus_df[virus_df['id']==virus_select]['molecular_weight'].iloc[0]
    st.markdown(f"<div><span class='bold'>Molecular Weight:</span> {temp_mw}</div>", unsafe_allow_html=True)
    st.write('')

    class_swap = {'virulent': 'non-virulent', 'non-virulent': 'virulent'}
    log_ids = [x['id'] for x in logs['Data']]

    if virus_select in log_ids:
        temp_class = class_swap[virus_df[virus_df['id']==virus_select]['class'].iloc[0]]
    else:
        temp_class = virus_df[virus_df['id']==virus_select]['class'].iloc[0]

    if temp_class == 'virulent':
        tc = f"<div><span class='bold'>Virulency:</span><span class='highlight red'>{temp_class}</span></div>"
    else:
        tc = f"<div><span class='bold'>Virulency:</span><span class='highlight green'>{temp_class}</span></div>"
    st.markdown(tc, unsafe_allow_html=True)

    temp_seq = virus_df[virus_df['id']==virus_select]['nucleotide_sequence'].iloc[0]

    st.write('')
    mis_class = st.button('Click if misclassified')
    if mis_class:
        change_dict = {'id': virus_select, 'class': temp_class, 'sequence': temp_seq}
        log_misclassification(logs, change_dict)
        st.write('Thank you for your feedback, it has been recorded!')
    st.markdown('---')

    if show_aa_chart:
        st.subheader('Breakdown of Virus Amino Acids')
        display_aa_chart(virus_df)
        st.markdown('---')

    if show_prot_scale:
        st.subheader('Protein Scale of Virus Sequence (Hydropathicity Amino Acid Scale)')
        analysis = ProteinAnalysis(virus_df[virus_df['id']==virus_select]['protein_sequence'].iloc[0])
        prot_scale = analysis.protein_scale(param_dict=hydropathicity, window=wsl, edge=esl)
        scale_fig = go.Figure(data=go.Scatter(x=np.arange(1,len(prot_scale)), y=np.array(prot_scale)))
        scale_fig.update_layout(xaxis_title='Position', yaxis_title='Hydropathicity')
        st.plotly_chart(scale_fig)
        st.markdown('---')

    if show_df:
        st.subheader('Raw Data')
        st_ms = st.multiselect("Columns", virus_df.columns.tolist(), default=ms_cols)
        # row_limit = st.sidebar.slider("Dataframe rows:", 1, 10, 1)
        st.dataframe(virus_df[virus_df['id']==virus_select][st_ms].head())
        st.markdown('---')

    