from django.views.generic import ListView

from calendarapp.models import Status
from accounts.decorators import staff_required
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


@method_decorator(login_required, name='dispatch')
@method_decorator(staff_required, name='dispatch')
class AllStatusListView(ListView):
    """ All status list views """

    template_name = "status/status_list.html"
    model = Status

    def get_queryset(self):
        return Status.objects.all()

