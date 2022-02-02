FROM python:3.7 AS builder
COPY requirements.txt .

# install requirements in the local directory -  user (e.g., /root/.local)
RUN pip install --user -r requirements.txt

FROM python:3.7-slim
WORKDIR /app

# copying only installed requirements from the first step image build
COPY --from=builder /root/.local/bin /root/.local
COPY . .

# update environment variable PATH
ENV PATH=/root/.local:$PATH

CMD [ "python", "./main.py" ]