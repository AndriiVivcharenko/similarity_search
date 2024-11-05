
FROM python:3.11


WORKDIR /code


COPY ./requirements.txt /code/requirements.txt


RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
RUN pip install uvicorn
RUN pip install "fastapi[standard]"


COPY ./app /code/app
COPY ./ai_adoption_framework_whitepaper.pdf /code
COPY ./.env /code


CMD ["python", "-m", "uvicorn", "app.main:app", "--port", "80", "--host", "0.0.0.0"]