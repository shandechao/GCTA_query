import sys 
import requests;
import re;
import xmltodict;


def main():
    if len(sys.argv) != 3:
        print("how to use: python seq_pattern_search_no_cache.py <ID> <REGEX_PATTERN>");
        sys.exit(1)
    
    seq_id = sys.argv[1]
    pattern = re.compile(sys.argv[2])


    efetch_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi";
    params = {
        "db": "nucleotide",
        "id": seq_id,
        "rettype": "fasta",
        "retmode": "xml"
    }
    response = requests.get(efetch_url, params=params);

    if not (response.status_code == 200 or response.status_code == 400):
        raise Exception(f"Failed to fetch sequence {seq_id}: HTTP {response.status_code}");
    xmlstr = response.text;
    if response.status_code==200 and "<TSeq>" in xmlstr:
        xmldata = xmltodict.parse(xmlstr)['TSeqSet']
        xmldata = xmldata['TSeq']['TSeq_sequence'];


    else:
        raise Exception(f"ID not exist");

    seq = xmldata
    matches = pattern.finditer(seq);
    result = [ list(m.span()) for m in matches]
    print(result)
    return ;


if __name__ == "__main__":
    main()