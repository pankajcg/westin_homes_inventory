FROM python:3.9

RUN mkdir /scratch
WORKDIR /scratch
COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./entrypoint.sh .
COPY ./env_file .
COPY ./main.py .
RUN chmod -R 755 /scratch

CMD ["./entrypoint.sh"]