FROM python:alpine3.7
WORKDIR /app
COPY . /app/
RUN python setup.py install
COPY app.py /app
EXPOSE 5000
CMD ["python", "app.py"]