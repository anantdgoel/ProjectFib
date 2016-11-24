FROM python:3.5.2-alpine
MAINTAINER Micheal Waltz <ecliptik@gmail.com>

#Set environment vars
ENV APP_DIR=/app

#App port
EXPOSE 5000

# Setup app dir
WORKDIR ${APP_DIR}
RUN mkdir -p ${APP_DIR}
COPY requirements.txt ${APP_DIR}/

# Install build packages, python dependencies, and clean up
RUN apk --no-cache add \
        --virtual build-dependencies \
          build-base && \
    pip install -U -r requirements.txt && \
    apk del build-dependencies

# Copy the app after installing dependencies
COPY *.py ${APP_DIR}/

#Run app
ENTRYPOINT ["python"]
CMD ["Server.py", "--log-file", "-"]
