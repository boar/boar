import datetime
from django.contrib.auth.models import User
from django.db import models
from ordered_model.models import OrderedModel

class Position(OrderedModel):
    email = models.EmailField(blank=True, null=True)
    
    def get_name(self):
        return self.positionname_set.latest()
    
    def get_members(self):
        return self.positionmember_set.filter(
            start_date__lte=datetime.date.today(),
            end_date__gte=datetime.date.today(),
        )
    
    def __unicode__(self):
        return self.get_name().name
    
    class Meta(OrderedModel.Meta):
        pass

class PositionName(models.Model):
    position = models.ForeignKey(Position)
    name = models.CharField(max_length=100)
    slug = models.SlugField()
    start_date = models.DateField(default=datetime.date.today, unique=True)
    
    class Meta:
        get_latest_by = 'start_date'
    

class PositionMember(models.Model):
    position = models.ForeignKey(Position)
    user = models.ForeignKey(User)
    start_date = models.DateField(default=datetime.date.today)
    end_date = models.DateField(null=True, blank=True)

