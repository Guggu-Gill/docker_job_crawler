




# Selenium Automation

![Blank diagram (4)](https://github.com/user-attachments/assets/132b6f9e-bb1f-4981-8960-c60ba5f4a920)


## Description
This code demonstrates how to use Docker SDK to run multiple Selenium sessions in parallel. It utilizes Docker containers, specifically a Selenium Standalone container, to handle parallel execution of automated web scraping tasks across multiple pages. The Docker SDK is used to manage container orchestration, ensuring efficient and isolated execution of each Selenium session.


## Prerequisites

- Python 3.9.6
- Docker Environment




## Installation

To get started, clone this repository to your local machine:

```bash
git clone https://github.com/Guggu-Gill/docker-job-crawler.git
cd docker-job-crawler
pip3 install -r requirements.txt
```

To run Docker SDK template:
```bash
pyhton3 infra.py
```

### Use below with Caution
To clean up your Docker environment (i.e., delete all containers, images, and networks):
```bash
./cleanup.sh
```


### Reference
- 1. https://github.com/SeleniumHQ/docker-selenium
- 2. https://docs.docker.com/reference/api/engine/sdk/
- 3. https://kubernetes.io/docs/home/


