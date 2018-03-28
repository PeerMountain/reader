FROM python:3.6 as base

# Bug in pipenv, where it does not find python in the PATH 
RUN ln -sf $(which python) /bin/python

WORKDIR /usr/src/app
COPY Pipfile* ./
COPY himalaya-models himalaya-models/

RUN pip install pipenv==9.0.1
RUN pipenv install --system

from base as production
COPY reader reader/
CMD ["python", "reader/main.py"]

FROM production as development
RUN pipenv install --system --dev
CMD ["python", "reader/main.py"]
