import pandas as pd
from django.shortcuts import render
from django.core.mail import send_mail
from .forms import UploadFileForm

def upload_file(request):
    summary = None
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            df = pd.read_excel(file)

            # Generate summary: count and sum of DPD per state
            summary_df = df.groupby('Cust State').agg({'DPD': ['count', 'sum']}).reset_index()
            summary_str = summary_df.to_string(index=False)

            # Email the summary
            send_mail(
                subject='Python Assignment - Your Name',
                message=summary_str,
                from_email='',
                recipient_list=[],
            )

            summary = summary_str

    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form, 'summary': summary})
