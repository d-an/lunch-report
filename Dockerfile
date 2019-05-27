from python:3.7.3-stretch
workdir /home/lunch
copy ./flask/requirements.txt ./
run pip install -r requirements.txt
entrypoint ["python", "flask/app.py"]
