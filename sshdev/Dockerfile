FROM nfs.k8s:8080/k8s/python:3.7
MAINTAINER zhaohlsky
ADD ./app /var/app
WORKDIR /var/app
#RUN pip3 install -r /var/app/requirements.txt
RUN pip install paramiko
RUN pip install pymysql
CMD ["python", "/var/app/ssh_tool_pod.py"]

