FROM python:3.8

WORKDIR /code

ENV VIRTUAL_ENV=/venv
RUN python3 -m venv $VIRTUAL_ENV

ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY requirements.txt /code/requirements.txt

RUN  pip install -r /code/requirements.txt

COPY app.py /code/app.py

EXPOSE 8000

CMD [ "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--reload" ]