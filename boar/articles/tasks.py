from celery.task import Task
import datetime

from boar.articles.models import Hit

class HitTask(Task):
    def run(self, article, date, user, ip_address, **kwargs):
        logger = self.get_logger(**kwargs)
        qs = Hit.objects.filter(article=article, date__gte=date-datetime.timedelta(hours=1))
        if user and not user.is_authenticated():
            user = None
        if user is None:
            qs = qs.filter(ip_address=ip_address)
        else:
            qs = qs.filter(user=user)
        if qs.count() == 0:
            return Hit.objects.create(article=article, date=date, user=user, ip_address=ip_address)

