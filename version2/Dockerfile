FROM python:3-stretch
COPY requirements.txt /tmp/requirements.txt 
RUN apt-get update
RUN apt-get upgrade -y
RUN pip install --no-cache-dir -r /tmp/requirements.txt
RUN python -m textblob.download_corpora
CMD ["python3", "/crypto-predicto/TrainingDatasetBuilder.py"]
