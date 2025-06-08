# nuSeqQuery
### Nucleotide Sequence Query

## 1. Project Overview
This project leverages NCBI's **EFetch** web-based retrieval tool to fetch and process nucleotide sequence data.  
**At last params**:  
● db: use the “nucleotide” database  
● id: use “30271926” (~30KB)  
● rettype: use a retrieval type of “fasta”  
● retmode: use a retrieval mode of “xml”  

django management command/script  stdout or write them to an output file.

## 2. Development Plan
Milestones:
- [x] Review and Understand Requirements
- [x] Explore and Test NCBI EFetch API
      1. use demo eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nucleotide&id=30271926&rettype=fasta&retmode=xml
      2. Request Limitations , 3 request/second;
- [x] System Desing
- [x] Project Development
- [ ] Deployment

## 3. System Design
3.1 tech stack
  **Backend**  Django + celery + postgreSQL
  **Frontend** Django Templete + bootstrap + jQuery

3.2 Architecture Diagram	


## 4. Live Demo

## 5. Tutorial

  ### 5.1 python version and packages install
    python 3.12
    virtualenv setup
    python3.12 -m venv venv
    source venv/bin/activate

    pip install -r requirements.txt

  ### 5.2 postgresql setup
    
    Make sure PostgreSQL is installed and running on the default port 5432.

    CREATE DATABASE nsq_cache;
    CREATE USER admin WITH PASSWORD 'iamadmin';
    GRANT ALL PRIVILEGES ON DATABASE nsq_cache TO admin;

  ## 5.3 Redis setup
    **Redis Install **
    sudo apt update
    sudo apt install redis-server
    sudo systemctl enable redis
    sudo systemctl start redis
    
    **check**
    redis-cli ping
    should return PONG



  ### 5.2 launch app
    # 1 single celery worker for sequence download. (To avoid IP blocking by NCBI )
    celery -A your_project worker -Q sequence --concurrency=1 --pool=solo --loglevel=info

    watchmedo auto-restart \
     --directory=./ \
     --pattern="*.py" \
     --recursive \
     -- celery -A nuSeqQuery worker \
     --loglevel=WARNING \
     --concurrency=1 \
     --max-tasks-per-child=100 \
     --hostname=sequence_worker@%h \
     --queues=sequence \
     --pool=solo


    # you can use multiple celery workers for analysis like pattern match
    watchmedo auto-restart \
     --directory=./ \
     --pattern="*.py" \
     --recursive \
     -- celery -A nuSeqQuery worker \
     --loglevel=info \
     --concurrency=1 \
     --max-tasks-per-child=100 \
     --hostname=analysis_worker2@%h \
     --queues=analysis \
     --pool=solo



     watchmedo auto-restart \
     --directory=./ \
     --pattern="*.py" \
     --recursive \
     -- celery -A nuSeqQuery worker \
     --loglevel=info \
     --concurrency=2 \
     --max-tasks-per-child=2 \
     --hostname=analysis_worker2@%h \
     --queues=analysis \
    


     pkill -f 'celery'
