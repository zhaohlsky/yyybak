FROM nfs.k8s:8080/k8s/python:3.7
MAINTAINER zhaohlsky
WORKDIR /share/app
RUN pip install paramiko
RUN pip install pymysql
CMD ["python", "/share/app/app.py"]

