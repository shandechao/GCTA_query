from django.core.management.base import BaseCommand, CommandError
from api.models import CompletedSequence,SequencePatternSearch;
from celery_tasks.logic import sequence_handler;
import re;

class Command(BaseCommand):
    help ='run command with seq id, and pattern you want to search'

    def add_arguments(self, parser):
        parser.add_argument('seq_id', type=str, help='length must > 1')
        parser.add_argument('pattern', type=str, help='length must >3')

    def handle(self, *args, **options):

        seq_id = options['seq_id']
        pattern = options['pattern']

        if len(seq_id) <= 1:
            raise CommandError('ength must > 1')
        
        if len(pattern) <= 1:
            raise CommandError('length must >3')
        
        db_seq_id = f"nucleotide_fasta_{seq_id}" ;

        seq="";
        try:
            
            result = sequence_handler.search_existing_sequences([db_seq_id]);
            if len(result["existing_ids"])>0:
                seq = CompletedSequence.objects.filter(id=db_seq_id).values_list("sequence_compressed", flat=True).first()
                seq = sequence_handler.decompress_bytes_to_string(seq);
        except:
            seq="";
        
        try:
            if seq=="":
                seq = sequence_handler.download_nucleotide_sequences_by_id(seq_id);
        except:
            seq = "";
        
        if seq =="":
            print("id not exists in NCBI")
            return 
        
        result=[]
        try:
            query_result = SequencePatternSearch.objects.filter(
                sequence_id=db_seq_id,
                pattern=pattern
            ).values("result").first()["result"]["result"]

            result=[]
            for a,b in zip(query_result["starts"],query_result["ends"]):
                result.append([a,b])

        except:
            result=[]

        if len(result) ==0:
            rp = re.compile(pattern);
            matches = rp.finditer(seq);
            result = [ list(m.span()) for m in matches]
            
        return str(result);