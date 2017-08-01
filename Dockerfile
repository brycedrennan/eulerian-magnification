FROM jjanzic/docker-python3-opencv:contrib
WORKDIR /code
COPY requirements.txt setup.py /code/
RUN mkdir eulerian_magnification
RUN pip3.6 install -r requirements.txt
COPY . /code/
RUN pip3.6 install -r requirements.txt
