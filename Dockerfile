FROM python:3.6
EXPOSE 5000
WORKDIR /app
COPY . /app/
RUN python setup.py install
COPY app.py /app
CMD python app.py