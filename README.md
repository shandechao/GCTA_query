# GCTA_query

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


