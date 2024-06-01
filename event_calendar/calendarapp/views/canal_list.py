from django.views.generic import ListView

from calendarapp.models import CanalMarket
from accounts.decorators import staff_required
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required




@method_decorator(staff_required, name='dispatch')
@method_decorator(login_required, name='dispatch')
class AllCanalListView(ListView):
    """ All CanalMarket list views """

    template_name = "canal/canal_list.html"
    model = CanalMarket

    def get_queryset(self):
        return CanalMarket.objects.all()

