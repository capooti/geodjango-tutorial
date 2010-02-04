#from django.db import models
from django.contrib.gis.db import models
from django.contrib import admin

# modelli
class Animale(models.Model):
    """Modello per rappresentare gli animali"""
    nome = models.CharField(max_length=50)
    foto = models.ImageField(upload_to='animali.foto')

    def __unicode__(self):
        return '%s' % (self.nome)

    def image_url(self):
        #return u'<img src="/tralerighe.media/%s" alt="%s" width="80"></img>' % (self.foto, self.nome)
        print '***%s****' % self.foto.url
        return u'<img src="%s" alt="%s" width="80"></img>' % (self.foto.url, self.nome)
    image_url.short_description = "Foto"
    image_url.allow_tags = True

    class Meta:
        ordering = ['nome']
        verbose_name_plural = "Animali"

class Avvistamento(models.Model):
    """Modello spaziale per rappresentare gli avvistamenti"""

    LIVELLI_INTERESSE = (
        (1, '*'),
        (2, '**'),
        (3, '***'),
        (4, '****'),
        (5, '*****'),
    )
    data = models.DateTimeField()
    note = models.TextField()
    interesse = models.IntegerField(choices=LIVELLI_INTERESSE)
    animale = models.ForeignKey(Animale)
    geometry = models.PointField(srid=4326) 
    objects = models.GeoManager()

    def __unicode__(self):
        return '%s' % (self.data)

    class Meta:
        ordering = ['data']
        verbose_name_plural = "Avvistamenti"

class Regione(models.Model):
    """Modello spaziale per rappresentare le regioni"""
    codice = models.IntegerField()
    nome = models.CharField(max_length=50)
    geometry = models.MultiPolygonField(srid=4326) 
    objects = models.GeoManager()

    def __unicode__(self):
        return '%s' % (self.nome)

class Provincia(models.Model):
    """Modello spaziale per rappresentare le regioni"""
    codice = models.IntegerField()
    nome = models.CharField(max_length=50)
    geometry = models.MultiPolygonField(srid=4326) 
    objects = models.GeoManager()

    def __unicode__(self):
        return '%s' % (self.nome)



