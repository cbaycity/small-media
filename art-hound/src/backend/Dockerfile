FROM python:3.12

# Copy source files to the container.
WORKDIR backend
COPY ./* .

RUN ls
RUN python -m pip install -r ./requirements.txt

EXPOSE 5000

CMD ["python", "main.py"]