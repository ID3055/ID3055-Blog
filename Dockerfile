FROM tiangolo/uwsgi-nginx-flask:python3.7

# If STATIC_INDEX is 1, serve / with /static/index.html directly (or the static URL configured)
# ENV STATIC_INDEX 1
#ENV STATIC_INDEX 0
#RUN pip install -r ./re.text
COPY re.txt /tmp/
RUN pip install --requirement /tmp/re.txt
COPY ./app /app
