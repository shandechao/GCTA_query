from api import models;
from django.utils import timezone;
import requests;
import xmltodict;
import time;
import zstandard as zstd
import requests;
import re;
import numpy as np;
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as patches

from intervaltree import Interval, IntervalTree

import io;
import base64;
matplotlib.use('Agg')

def compress_string_to_bytes(s: str) -> bytes:
    compressor = zstd.ZstdCompressor()
    return compressor.compress(s.encode("utf-8"))

def decompress_bytes_to_string(b: bytes) -> str:
    decompressor = zstd.ZstdDecompressor()
    return decompressor.decompress(b).decode("utf-8")



def search_existing_sequences(query_list):
    existing = models.CompletedSequence.objects.filter(id__in=query_list);  #.exclude(accession="N/A");
    #accession="N/A",
    existing.update(processed_time=timezone.now())
    existing_ids = set(existing.values_list('id', flat=True))
    
    missing_ids = list(set(query_list) - existing_ids)

    return {"existing_ids": list(existing_ids), "missing_ids": missing_ids}



def download_nucleotide_sequences_by_id(seq_id):
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
        return xmldata['TSeq']['TSeq_sequence'];

    else:
        return "";


def download_sequences(missing_ids):
    """
    Download sequences for the given missing IDs.
    This function should implement the actual downloading logic.
    For now, we just simulate the download process.
    """
    #response2 = requests.post(url, data=params)
    efetch_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi";

    # Simulate downloading sequences
    for seq_id in missing_ids:
        #start = time.perf_counter();
        try:
            seq_id_str = seq_id.split("_");
        
            params = {
                "db": seq_id_str[0],
                "id": seq_id_str[2],
                "rettype": seq_id_str[1],
                "retmode": "xml"
            }
            response = requests.get(efetch_url, params=params);

            if not (response.status_code == 200 or response.status_code == 400):
                raise Exception(f"Failed to fetch sequence {seq_id}: HTTP {response.status_code}");
        
            
            xmlstr = response.text;
            if response.status_code==200 and "<TSeq>" in xmlstr:
                xmldata = xmltodict.parse(xmlstr)['TSeqSet']
                i = xmldata['TSeq'];
                
                record = models.CompletedSequence(
                    id=seq_id,
                    accession=i.get('TSeq_accver'),
                    seqtype="nucleotide",
                    tax_id=int(i['TSeq_taxid']) if i.get('TSeq_taxid') else None,
                    organism_name=i.get('TSeq_orgname'),
                    description=i.get('TSeq_defline'),
                    length=int(i['TSeq_length']) if i.get('TSeq_length') else None,
                    sequence_compressed=compress_string_to_bytes(i['TSeq_sequence']),
                    other_info={
                        "sid": i.get("TSeq_sid") if i.get('TSeq_sid') else None, 
                    }
                )
                record.save()

            else:
                record = models.CompletedSequence(
                    id=seq_id,
                    accession="N/A",
                    seqtype="nucleotide",
                    length=0,
                )
                record.save()

        except requests.RequestException as e:
            
            continue

        #remaining = 0.4 - (time.perf_counter() - start)
        #time.sleep(max(0, remaining))

    return {"status": "1", "message": "Sequences downloaded successfully."};

       
def do_patterns_search(regex_pattern, seq_id):
    
    now_time = timezone.now()

    updated = models.SequencePatternSearch.objects.filter(
        sequence_id=seq_id,
        pattern=regex_pattern
    ).update(search_at=now_time)    

    if updated:
        models.CompletedSequence.objects.filter(id=seq_id).update(processed_time=now_time)
        print("record exists")
        return "record exists";
    #else;
    tcga = models.CompletedSequence.objects.filter(id=seq_id).first();
    if not(tcga and tcga.length) :
        return "seq empty";
    
    tcga = decompress_bytes_to_string(tcga.sequence_compressed);
    rp = re.compile(regex_pattern);
    matches = rp.finditer(tcga);
    matches = [ list(m.span()) for m in matches]

    if not matches:
        #insert empty result
        models.SequencePatternSearch.objects.create(
            sequence=seq,
            pattern=regex_pattern,
            result={
                "motif_counts":0,
                "starts":[],
                "ends":[],
                'overlap_counts':[],
                "seq_length":len(tcga),
            },
            others = {}
        )
        return "no matches";
    
    
    starts = np.array([s for s, e in matches])
    ends = np.array([e for s, e in matches])
    motif_lengths = ends - starts
    gaps = starts[1:] - ends[:-1] if len(starts) >= 2 else []
    sequence_length = len(tcga)

    result=dict();
    
    result["result"]={
        
        "starts": [int(x) for x in starts],
        "ends" :[int(x) for x in ends],
    }
    
    #addition works
    tree = IntervalTree()
    for idx, (start, end) in enumerate(matches):
        tree.add(Interval(start, end, idx))

    overlap_counts = []
    for start, end in matches:
        overlaps = tree.overlap(start, end)
        overlap_counts.append(len(overlaps) - 1)
    
    result["result"]["overlap_counts"] = overlap_counts;
    
    
    plot = addition_pattern_analysis(motif_lengths,gaps);
    
    plot["new"]  = addition_pattern_analysis2(sequence_length,starts,ends);
    seq = models.CompletedSequence.objects.get(id=seq_id)

    models.SequencePatternSearch.objects.create(
        sequence=seq,
        pattern=regex_pattern,
        result=result,
        others = {"info":{
                    "motif_counts" : len(starts),
                    "seq_length":sequence_length,
                    },
                    "plot":plot
                }
    )
    
    return "done"


def addition_pattern_analysis2(sequence_length,starts,ends):
    fig, ax = plt.subplots(figsize=(16, 4))


    if sequence_length <= 10_000:
        for s, e in zip(starts, ends):
            ax.add_patch(patches.Rectangle((s, 0), e - s, 1, facecolor="blue", edgecolor="black"))
        ax.set_xlim(0, sequence_length)
        ax.set_ylim(0, 1.2)
        ax.set_yticks([])
        ax.set_xlabel("Sequence Position (bp)")
        ax.set_title("Motif Feature Map")
    else:
        bin_size = 10_000
        if sequence_length <= 100_000:
            bin_size = 1000
        elif sequence_length <= 1_000_000:
            bin_size =  5000
        elif sequence_length <= 10_000_000:
            bin_size =  10_000
        elif sequence_length <= 100_000_000:
            bin_size =  50_000
        elif sequence_length <= 300_000_000:
            bin_size =  100_000
        else:
            bin_size =  500_000

        num_bins = sequence_length // bin_size + 1
        counts, bin_edges = np.histogram(starts, bins=num_bins, range=(0, sequence_length))
        ax.plot(bin_edges[:-1], counts, linewidth=0.8)
        ax.set_title(f"Motif Density across Sequence ({bin_size // 1000}kb bins)")
        ax.set_xlabel("Sequence Position (bp)")
        ax.set_ylabel("Motif Count per Bin")

    plt.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    base64_str = base64.b64encode(buf.read()).decode("utf-8")
    buf.close()
    plt.close()

    return base64_str;

def addition_pattern_analysis(motif_lengths,gaps):
    base64_images = {}
    plt.figure(figsize=(6, 4))
    plt.hist(motif_lengths, bins=range(min(motif_lengths), max(motif_lengths) + 2), edgecolor='black')
    plt.title("Motif Length Distribution")
    plt.xlabel("Motif Length (bp)")
    plt.ylabel("Count")
    plt.tight_layout()
    buf1 = io.BytesIO()
    plt.savefig(buf1, format='png')
    buf1.seek(0)
    base64_images["length_distribution"] = base64.b64encode(buf1.read()).decode('utf-8')
    buf1.close()
    plt.close()

    if len(gaps) > 0:
        plt.figure(figsize=(6, 4))
        plt.hist(gaps, bins=30, edgecolor='black')
        plt.title("Motif Gap Distribution")
        plt.xlabel("Gap between motifs (bp)")
        plt.ylabel("Count")
        plt.tight_layout()
        buf2 = io.BytesIO()
        plt.savefig(buf2, format='png')
        buf2.seek(0)
        base64_images["gap_distribution"] = base64.b64encode(buf2.read()).decode('utf-8')
        buf2.close()
        plt.close()
    return base64_images
