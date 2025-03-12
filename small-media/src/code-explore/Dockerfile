# Use an official Python 3.12 base image
FROM python:3.12

WORKDIR code-explore
COPY . .

# Install Jupyter and other common tools
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    && pip install --no-cache-dir \
    notebook \
    jupyterlab \
    numpy pandas matplotlib scipy seaborn scikit-learn

# Expose the notebook port
EXPOSE 8888

# Start Jupyter Notebook by default
CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root"]