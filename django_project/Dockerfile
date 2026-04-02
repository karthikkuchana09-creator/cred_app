FROM python:3.12-slim
WORKDIR /usr/src/app
COPY ../requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN chmod +x /usr/src/app/startup.sh
EXPOSE 8000
CMD ["/usr/src/app/startup.sh"]
