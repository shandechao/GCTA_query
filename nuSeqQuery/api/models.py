from django.db import models
# Create your models here.
"""
class WaitingQuery(models.Model):
    
    STATUS_CHOICES = [(s, s.capitalize()) for s in ['waiting', 'loading', 'done', 'failed']]

    id = models.CharField(max_length=40, primary_key=True)
    status = models.CharField(max_length=20,choices=STATUS_CHOICES, default='waiting')
    queue_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['queue_time']

    def __str__(self):
        return f"{self.id} - {self.status}"
"""


class CompletedSequence(models.Model):
    id = models.CharField(max_length=40, primary_key=True)
    accession = models.CharField(max_length=50, null=True, blank=True)
    seqtype = models.CharField(max_length=20, null=True, blank=True)
    tax_id = models.IntegerField(null=True, blank=True)
    organism_name = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    length = models.IntegerField(null=True, blank=True)
    sequence_compressed = models.BinaryField(null=True, blank=True)
    processed_time = models.DateTimeField(auto_now=True)
    other_info = models.JSONField(null=True, blank=True)

    def __str__(self):
        return self.id
    

class SequencePatternSearch(models.Model):
    sequence = models.ForeignKey(CompletedSequence, on_delete=models.CASCADE, related_name='pattern_analyses')
    pattern = models.TextField(null=False, blank=False)
    result = models.JSONField(default=dict)
    others=models.JSONField(default=dict)
    search_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-search_at']
        constraints = [
            models.UniqueConstraint(fields=['sequence', 'pattern'], name='unique_pattern_per_sequence')
        ]

    def __str__(self):
        return f"{self.sequence.id} - {self.pattern}"