FROM --platform=linux/amd64 public.ecr.aws/lambda/python:3.9

COPY requirements.txt .

RUN python3.9 -m pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY *.py .

CMD ["lambda_handler.get_voices"]