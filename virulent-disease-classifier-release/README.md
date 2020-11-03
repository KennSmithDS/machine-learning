# virulent-disease-classifier

**Folder Structure:**

1. exploration: various verions of notebooks and data files used in exploration and model building
2. ncbi_crawl: discontinued attempt at building Scrapy crawling service from NCBI database/webpage
3. service: stores the dockerfile as well as streamlit UI files


**File Description:**

**Data:** 

1. valid_non_virulent_sequences.csv
2. valid_virulent_sequences.csv
3. pathogenic_sequences_table.csv
4. non_pathogenic_sequences_table.csv

Generated File: virus_analysis.csv

**Code:**

exploration/virus_exploration_classification_tool.ipynb : Wholistic walk-through of the data exploration, preprocessing, and model building and performance evaluation/comparison.

sequence_preprocessing.py : Performs feature extraction from input nucleotide or protein sequence.

structures.py : Basic bioinformatic structures defined.

style.css: CSS for UI

virus_app.py : UI generation

misclassification_log.json: Log file for misclassified data

**Model:**

virus_extra_trees_model.joblib : Classifier Model

**Docker Files:**

Dockerfile : performs docker operations

requirements.txt: specifies library requirements for docker image.


**Execution steps:**

http://www.inteligems.com/virus-prediction-app

If service is down, go to folder where dockerFile is located using cmd or Powershell

1. docker build . -t virus_app
2. docker run -p 8501:8501 virus_app:latest
3. docker ps : Check the image 
4. docker tag <tagname> dockerhubname/imagename:tagname
5. docker push  dockerhubname/imagename:tagname

**Test:**

1. ui_samples.fasta (Fasta File Upload)
2. testingtext.csv (CSV File Upload)
