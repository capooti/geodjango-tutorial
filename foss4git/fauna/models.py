from django.db import models
from django.contrib.gis.db import models as gismodels

# modelli
class Animale(models.Model):
    """Modello per rappresentare gli animali"""
    nome = models.CharField(max_length=50)
    foto = models.ImageField(upload_to='animali.foto')

    def __unicode__(self):
        return '%s' % (self.nome)

    def image_url(self):
        print '***%s****' % self.foto.url
        return u'<img src="%s" alt="%s" width="80"></img>' % (self.foto.url, self.nome)
    image_url.short_description = "Foto"
    image_url.allow_tags = True

    class Meta:
        ordering = ['nome']
        verbose_name_plural = "Animali"

class Avvistamento(gismodels.Model):
    """Modello spaziale per rappresentare gli avvistamenti"""

    LIVELLI_INTERESSE = (
        (1, '*'),
        (2, '**'),
        (3, '***'),
        (4, '****'),
        (5, '*****'),
    )
    data = gismodels.DateTimeField()
    note = gismodels.TextField()
    interesse = gismodels.IntegerField(choices=LIVELLI_INTERESSE)
    animale = gismodels.ForeignKey(Animale)
    geometry = gismodels.PointField(srid=4326) 
    objects = gismodels.GeoManager()

    def __unicode__(self):
        return '%s' % (self.data)

    class Meta:
        ordering = ['data']
        verbose_name_plural = "Avvistamenti"

class Regione(gismodels.Model):
    """Modello spaziale per rappresentare le regioni"""
    codice = gismodels.IntegerField()
    nome = gismodels.CharField(max_length=50)
    geometry = gismodels.MultiPolygonField(srid=4326) 
    objects = gismodels.GeoManager()

    def __unicode__(self):
        return '%s' % (self.nome)

class Provincia(gismodels.Model):
    """Modello spaziale per rappresentare le regioni"""
    codice = gismodels.IntegerField()
    nome = gismodels.CharField(max_length=50)
    geometry = gismodels.MultiPolygonField(srid=4326) 
    objects = gismodels.GeoManager()

    def __unicode__(self):
        return '%s' % (self.nome)

class SandboxLayer(gismodels.Model):
    """Modello spaziale per effettuare test con l'API GeoDjango"""
    nome = gismodels.CharField(max_length=50)
    geometry = gismodels.GeometryField(srid=3395) # WGS84 mercatore
    objects = gismodels.GeoManager()

    def __unicode__(self):
        return '%s' % (self.nome)



