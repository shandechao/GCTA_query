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
- [x] System Design
- [x] Project Development
- [x] Deployment and Test

## 3. System Design
3.1 tech stack
**Simple Script Version**  
Python 3 only  

**Web App Version**  
**Backend:** Django + Redis + Celery + PostgreSQL  
**Frontend:** Django Template + Bootstrap + jQuery

3.2 Architecture and Design
[🗺️ Architecture and Design](./ARCHITECTURE_AND_DESIGN.md)

## 4. Live Demo
www.shandechao.com (might or might not be online — TBD 😅)
 
## 5. Tutorial

  ### 5.1 python version and packages install
  python 3.11+ ( Other Python 3 versions are expected to work, but they have not been tested )
  virtualenv setup
  python3.11 -m venv venv
  source venv/bin/activate

  pip install -r requirements.txt

  ### 5.2 Run the single-script version (this version does not require setting up a database or Celery).
  python seq_pattern_search_no_cache.py 30271926 "(AATCGA|GGCAT)"
  or 
  python seq_pattern_search_no_cache.py 30271926 "(AATCGA|GGCAT)" > pattern_location.txt

  ### 5.3 postgresql setup
    
  Make sure PostgreSQL is installed and running on the default port 5432.

  CREATE DATABASE nsq_cache;
  CREATE USER admin WITH PASSWORD 'iamadmin';
  GRANT ALL PRIVILEGES ON DATABASE nsq_cache TO admin;

  ## 5.4 Redis setup
  **Redis Install **
  sudo apt update
  sudo apt install redis-server
  sudo systemctl enable redis
  sudo systemctl start redis
    
  **check**
  redis-cli ping
  should return PONG

  ### 5.5 use django management test function
  python manage.py run_seq_pattern_search 30271926 "(AATCGA|GGCAT)"
  or
  python manage.py run_seq_pattern_search 30271926 "(AATCGA|GGCAT)" > match_arr.txt

  ### 5.6 launch app
  **step 1:**  
    cd nuSeqQuery
    ***option 1. one button lanuch***
    supervisord -c supervisord.conf

    ***option 2. step by step lanuch***
    celery for fetch: 
    celery -A nuSeqQuery worker --loglevel=WARNING --concurrency=1 --max-tasks-per-child=1 --hostname=sequence_worker@%h --queues=sequence --pool=solo &

    celery for analysis/pattern match: 
    celery -A nuSeqQuery worker --loglevel=WARNING --concurrency=1 --max-tasks-per-child=1 --hostname=analysis_worker@%h --queues=analysis --pool=solo &

    lanuch django app
    uvicorn nuSeqQuery.asgi:application --host 0.0.0.0 --port 8000

  **step 2:**
    Open the browser
    localhost:8000 or yourhost:8000

  ### User Toturial
  [📘 User Guide](./USER_GUIDE.md)
    
  ## 📫 Contact
  Feel free to reach out at my email if you have any questions or feedback.
    
  