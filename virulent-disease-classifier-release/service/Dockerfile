FROM continuumio/miniconda3

# Install python packages
RUN mkdir /opt/api
COPY requirements.txt /opt/api/
RUN pip install -r /opt/api/requirements.txt

# Copy files into container
COPY virus_extra_trees_model.joblib /opt/api/
COPY style.css /opt/api
COPY structures.py /opt/api
COPY sequence_preprocessing.py /opt/api
COPY misclassification_log.json /opt/api
COPY virus_app.py /opt/api/


# Set work directory and open the required port
WORKDIR /opt/api
EXPOSE 8501

# Run our service script
CMD streamlit run virus_app.py
