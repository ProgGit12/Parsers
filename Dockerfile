FROM python:3.7

RUN mkdir -p /usr/src/app/
WORKDIR /usr/src/app/

COPY . /usr/src/app/
RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt


CMD ["python", "/Sites_pars/rttf(tennis)/Play.py"]