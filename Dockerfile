FROM python:3.12-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
ENTRYPOINT ["python3"]
CMD ["deployment/app.py"]
EXPOSE 5000