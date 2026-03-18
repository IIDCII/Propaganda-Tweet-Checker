FROM python:3.11-slim

# Install testing dependencies
RUN pip install pytest requests psycopg2-binary

WORKDIR /tests

# Copy only the test suite
COPY . .

# Wait for the API to be ready before starting
ENTRYPOINT ["pytest"]
