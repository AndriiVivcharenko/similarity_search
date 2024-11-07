
FROM python:3.11


WORKDIR /code


COPY ./requirements.txt /code/requirements.txt


RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
RUN pip install uvicorn
RUN pip install "fastapi[standard]"


COPY ./app /code/app
COPY ./ai_adoption_framework_whitepaper.pdf /code
COPY setup_env.sh /code

# Make the setup script executable and run it
RUN chmod +x /code/setup_env.sh && /code/setup_env.sh

# Copy the .env file if it exists in the context
COPY .env* /code/.env

CMD [ "python", "-m", "uvicorn", "app.main:app", "--port", "80", "--host", "0.0.0.0", "--timeout-keep-alive", "1200", "--timeout-graceful-shutdown", "1200" ]