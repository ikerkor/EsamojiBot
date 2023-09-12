# Choosing an image for you container.
FROM --platform=$BUILDPLATFORM python:3.10-alpine

# Setting your working directory
WORKDIR /app
# This command would copy EVERY FILE from your project folder into your container, so be careful.
COPY . .
#Installing lxml before python requirements
RUN apk add --update --no-cache g++ gcc libxslt-dev
# Installing needed packages and dependencies.**
RUN pip install -r requirements.txt
# This command basically executes your main file with Python.
CMD ["python", "main.py"]
EXPOSE 8443/tcp