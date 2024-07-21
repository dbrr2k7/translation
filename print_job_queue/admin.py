from django.contrib import admin

from print_job_queue.models import PrintJob, PrintedDocument, Worker

admin.site.register(PrintJob)
admin.site.register(PrintedDocument, list_display=['id', 'file_path', 'print_count'])
admin.site.register(Worker, ordering=['name'])
