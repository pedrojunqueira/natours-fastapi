FROM python:3.8

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /backend

COPY ./requirements.txt /backend/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /backend/requirements.txt

# set timezone to adelaide
RUN unlink /etc/localtime \
    && ln -s /usr/share/zoneinfo/Australia/Adelaide /etc/localtime

COPY . /backend/

CMD ["uvicorn", "--app-dir=.", "natours.app:app", "--reload", "--host", "0.0.0.0", "--port", "80"]