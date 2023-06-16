FROM python:3.11-slim-buster

# Set the working directory in the container
WORKDIR /app

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN pip install --upgrade pip

# Copy the requirements file and other files to the container
COPY ./app /app
COPY ./requirements.txt /app

# Install dependencies
RUN pip3 install -r requirements.txt

# Expose the port that the application will be running on
EXPOSE 8000

# Run the application
CMD ["uvicorn", "main:app", "--host=0.0.0.0", "--reload"]