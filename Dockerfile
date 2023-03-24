# renovate: datasource=docker depName=python
ARG PYTHON_VERSION=3.9.4
FROM --platform=$BUILDPLATFORM python:${PYTHON_VERSION} AS deps

# renovate: datasource=pypi depName=poetry
ARG POETRY_VERSION=1.4.1
RUN pip install poetry==${POETRY_VERSION}

ADD pyproject.toml poetry.lock /app/
RUN cd /app && poetry export --without-hashes >requirements.txt

FROM python:${PYTHON_VERSION}

ADD . /app
WORKDIR /app
COPY --from=deps /app/requirements.txt /app/
RUN pip install -r requirements.txt

ENTRYPOINT [ "python" ] 
CMD [ "-m", "twitterdedupe" ]
