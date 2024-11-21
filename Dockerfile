FROM python:3.12.4

COPY ./practicas /practicas

RUN pip install -r /practicas/librerias_python.txt 
