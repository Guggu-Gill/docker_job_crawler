




# Selenium Automation IaC

![Blank diagram (4)](https://github.com/user-attachments/assets/132b6f9e-bb1f-4981-8960-c60ba5f4a920)


## Description
This code demonstrates how to use Docker SDK as Infrastructure as Code (IaC) to run multiple Selenium sessions in parallel. It utilizes Docker containers, specifically a Selenium Standalone Chrome container, to handle parallel execution of automated web scraping tasks across multiple pages. The Docker SDK is used to manage container orchestration, ensuring efficient and isolated execution of each Selenium session.

## Prerequisites

- Python 3.9.6
- Docker Environment


## Installation

To get started, clone this repository to your local machine:

```bash
git clone https://github.com/Guggu-Gill/docker-job-crawler.git
cd docker-job-crawler
pip3 install -r requirements.txt

pyhton3 infra.py
