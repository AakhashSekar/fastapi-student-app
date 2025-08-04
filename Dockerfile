FROM Python:3.9
WORKDIR /app
COPY requirement.txt
RUN pip install --no chache dir --upgrade -r requirement.txt
COPY ./app /app
CMD ["uvicorn', "main:app", "--host", "0.0.0", "-port", "80"]
