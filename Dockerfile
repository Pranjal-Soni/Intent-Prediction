FROM alpine
COPY . /usr/app/
EXPOSE 8000
WORKDIR /usr/app/
RUN pip install -r requirments.txt
CMD python app.py
