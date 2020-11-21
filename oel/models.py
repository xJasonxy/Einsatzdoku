from django.contrib.auth import get_user_model
from django.db import models

class Einheiten(models.Model):
    Einsatz = models.ForeignKey('doku.Einsatz', on_delete=models.PROTECT)
    Name = models.CharField(max_length=50, null=False, blank=False)

    def __str__(self):
        return self.Name

    def getAnzahlEinsatzstellen(self):
        return Einsatzstellen.objects.filter(Einheit=self).filter(Abgeschlossen=None).count()


class Einsatzstellen(models.Model):
    Einsatz = models.ForeignKey('doku.Einsatz', on_delete=models.PROTECT)
    Ort = models.ForeignKey('doku.Ort', on_delete=models.PROTECT)
    OrtFrei = models.CharField(max_length=200, null=True)
    Name = models.CharField(max_length=50, null=False, blank=False)
    Einheit = models.ForeignKey('Einheiten', null=True, blank=True, on_delete=models.PROTECT)
    Anmerkungen = models.TextField(null=False, blank=True, default="")
    Gemeldet = models.DateTimeField(auto_now_add=True)
    Zugewiesen = models.DateTimeField(blank=True, null=True)
    Abgeschlossen = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ('Gemeldet', 'Ort')

    def __str__(self):
        if self.Ort.PLZ == 0:
            return self.Name + ", " + self.OrtFrei
        else:
            return self.Name + ", " + self.Ort.Langname

    def get_all_info(self):
        return Informationen.objects.filter(Einsatzstelle=self).order_by('Timestamp')

    def get_latest_info(self):
        try:
            return self.get_all_info()[0]
        except:
            return None



class Informationen(models.Model):
    Einsatzstelle = models.ForeignKey('Einsatzstellen', on_delete=models.PROTECT)
    Autor = models.ForeignKey(get_user_model(), on_delete=models.PROTECT, editable=False)
    Timestamp = models.DateTimeField(auto_now_add=True)
    Personal = models.IntegerField(default=0)
    Material = models.TextField(null=False, blank=True, default="")
    Freitext = models.TextField(null=False, blank=True, default="")
