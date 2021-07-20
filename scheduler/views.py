from django.shortcuts import render

# Create your views here.

def show_jobs(request):
    if (request.user.is_superuser):
        jobs = getScheduledJobs()
        context = {
            'jobs': jobs
        }
        print(jobs)
        return render(request, 'scheduler/showjobs.html', context)

    else:
        raise Http404