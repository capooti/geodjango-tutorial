==================
Utilizzo di Django
==================

Creazione ed attivazione del virtualenv
---------------------------------------

Creare e attivare un virtualenv con django 1.2 alpha 1 e python 2.6 oppure utilizzare quello gia' disponibile sulla VM::

    geodjango@geodjango-laptop:~/tutorial/django-1.2-alpha-1-env$ source bin/activate
    
Creazione del progetto Django per il tutorial
---------------------------------------------

Creare il progetto Django::

    django-admin.py startproject foss4git
    cd foss4git/

Editing del file settings.py
----------------------------

a questo punto editare il file di configurazione settings.py::

    import os
    
    # aggiungere queste due righe che settano due variabili utilizzate poi nel seguito
    ROOT_PROJECT_FOLDER = os.path.dirname(__file__)
    STATIC_FILES = os.path.join(ROOT_PROJECT_FOLDER,'static')
    ...
    DATABASES = {
        'default': {
            'ENGINE': 'postgresql_psycopg2', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
            'NAME': 'tutorial',                      # Or path to database file if using sqlite3.
            'USER': 'geodjango',                      # Not used with sqlite3.
            'PASSWORD': 'geodjango',                  # Not used with sqlite3.
            'HOST': 'localhost',                      # Set to empty string for localhost. Not used with sqlite3.
            'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
        }
    } 
    ...
    LANGUAGE_CODE = 'it-IT' # setta in italiano la localizzazione
    ...
    # setta i path dei media files
    MEDIA_ROOT = STATIC_FILES
    MEDIA_URL = '/static/'
    ADMIN_MEDIA_PREFIX = '/media/'
    
Creiamo il db. Utilizzeremo PostGis, anche se e'./man possibile seguire il tutorial, con piccole differenze, con Spatialite (sqlite3)::

    (django-1.2-alpha-1-env)geodjango@geodjango-laptop:~/tutorial/django-1.2-alpha-1-env/foss4git$ psql -U geodjango template1
    psql (8.4.2)
    Type "help" for help.
    
    template1=> CREATE DATABASE tutorial WITH TEMPLATE=template_postgis ENCODING='UTF8';
    CREATE DATABASE
    template1=> \q
    
Sincronizziamo il db::

    (django-1.2-alpha-1-env)geodjango@geodjango-laptop:~/tutorial/django-1.2-alpha-1-env/foss4git$ ./manage.py syncdb
    Creating table django_content_type
    Creating table auth_permission
    Creating table auth_group_permissions
    Creating table auth_group
    Creating table auth_user_user_permissions
    Creating table auth_user_groups
    Creating table auth_user
    Creating table auth_message
    Creating table django_site
    Creating table django_session

    You just installed Django's auth system, which means you don't have any superusers defined.
    Would you like to create one now? (yes/no): yes
    Username (Leave blank to use 'geodjango'): admin
    E-mail address: pcorti@gmail.com
    Password: 
    Password (again): 
    Superuser created successfully.
    Installing index for auth.Permission model
    Installing index for auth.Message model
    
Abbiamo gia' le tabelle base per un'applicazione django create nel database::

    (django-1.2-alpha-1-env)geodjango@geodjango-laptop:~/tutorial/django-1.2-alpha-1-env/foss4git$ psql -U geodjango tutorial
    psql (8.4.2)
    Type "help" for help.

                             List of relations
     Schema |               Name                |   Type   |   Owner   
    --------+-----------------------------------+----------+-----------
     public | auth_group                        | table    | geodjango
     public | auth_group_id_seq                 | sequence | geodjango
     public | auth_group_permissions            | table    | geodjango
     public | auth_group_permissions_id_seq     | sequence | geodjango
     public | auth_message                      | table    | geodjango
     public | auth_message_id_seq               | sequence | geodjango
     public | auth_permission                   | table    | geodjango
     public | auth_permission_id_seq            | sequence | geodjango
     public | auth_user                         | table    | geodjango
     public | auth_user_groups                  | table    | geodjango
     public | auth_user_groups_id_seq           | sequence | geodjango
     public | auth_user_id_seq                  | sequence | geodjango
     public | auth_user_user_permissions        | table    | geodjango
     public | auth_user_user_permissions_id_seq | sequence | geodjango
     public | django_content_type               | table    | geodjango
     public | django_content_type_id_seq        | sequence | geodjango
     public | django_session                    | table    | geodjango
     public | django_site                       | table    | geodjango
     public | django_site_id_seq                | sequence | geodjango
     public | geometry_columns                  | table    | postgres
     public | spatial_ref_sys                   | table    | postgres
    (21 rows)
    \q
    
Primo avvio del progetto
------------------------

Usando il server di django::

    (django-1.2-alpha-1-env)geodjango@geodjango-laptop:~/tutorial/django-1.2-alpha-1-env/foss4git$ ./manage.py runserver
    Validating models...
    0 errors found

    Django version 1.2 alpha 1, using settings 'foss4git.settings'
    Development server is running at http://127.0.0.1:8000/
    Quit the server with CONTROL-C.

A questo punto andando su localhost:8000 dovrebbe presentarsi la schermata iniziale.

Creazione dell'applicazione del tutorial
----------------------------------------

Creeremo un'applicazione denominata fauna, con due modelli (Animale, Avvistamento)::

    (django-1.2-alpha-1-env)geodjango@geodjango-laptop:~/tutorial/django-1.2-alpha-1-env/foss4git$ ./manage.py startapp fauna
    
Notare la struttura iniziale del progetto e dell'applicazione::

    (django-1.2-alpha-1-env)geodjango@geodjango-laptop:~/tutorial/django-1.2-alpha-1-env/foss4git$ tree
    .
    |-- __init__.py
    |-- __init__.pyc
    |-- fauna
    |   |-- __init__.py
    |   |-- models.py
    |   |-- tests.py
    |   `-- views.py
    |-- manage.py
    |-- settings.py
    |-- settings.pyc
    |-- settings.py~
    `-- urls.py

    1 directory, 11 files
    
Installazione delle applicazioni
--------------------------------

Nel file settings.py installiamo l'applicazione fauna e contrib.admin::

    ...
    INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.admin',
    'foss4git.fauna',
    )
    ...
    
Creazione dei modelli
---------------------

Creiamo i due modelli nel file models.py::

    from django.db import models

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

        def __unicode__(self):
            return '%s' % (self.data)

        class Meta:
            ordering = ['data']
            verbose_name_plural = "Avvistamenti"
    
Prima di sincronizzare il db, verifichiamo che operazioni effettuera' la sincronizzazione::

    (django-1.2-alpha-1-env)geodjango@geodjango-laptop:~/tutorial/django-1.2-alpha-1-env/foss4git$ ./manage.py sql fauna
    BEGIN;
    CREATE TABLE "fauna_animale" (
        "id" serial NOT NULL PRIMARY KEY,
        "nome" varchar(50) NOT NULL,
        "foto" varchar(100) NOT NULL
    )
    ;
    CREATE TABLE "fauna_avvistamento" (
        "id" serial NOT NULL PRIMARY KEY,
        "data" timestamp with time zone NOT NULL,
        "note" text NOT NULL,
        "interesse" integer NOT NULL,
        "animale_id" integer NOT NULL REFERENCES "fauna_animale" ("id") DEFERRABLE INITIALLY DEFERRED
    )
    ;
    COMMIT;
    
Sincronizziamo il database::

    (django-1.2-alpha-1-env)geodjango@geodjango-laptop:~/tutorial/django-1.2-alpha-1-env/foss4git$ ./manage.py syncdb
    Creating table django_admin_log
    Creating table fauna_animale
    Creating table fauna_avvistamento
    Installing index for admin.LogEntry model
    Installing index for fauna.Avvistamento model
    
Utilizzo dell'applicazione contrib.admin
----------------------------------------

contrib.admin e' stata gia' installata, a questo punto e' sufficiente configuare la prima url nel file urls. Nello stesso file va anche impostata la url dei file statici::

    ...
    from settings import STATIC_FILES
    from django.contrib import admin
    admin.autodiscover()
    ...

        # Uncomment the next line to enable the admin:
        (r'^admin/', include(admin.site.urls)),
        # static files
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': STATIC_FILES, 'show_indexes': True}),
    )
    
Lanciando il server e andando sull'admin, pero' i due modelli non sono presenti. Creiamo un file fauna/admin.py cosi' costituito::

    from django.contrib import admin
    from models import *

    class AvvistamentoAdmin(admin.ModelAdmin):

        model = Avvistamento

        list_display = ['data', 'animale', 'interesse']
        list_filter = ['data', 'animale', 'interesse']
        date_hierarchy = 'data'
        fieldsets = (
          ('Location Attributes', {'fields': (('data', 'animale', 'note', 'interesse'))}),
        )

    class AnimaleAdmin(admin.ModelAdmin):

        model = Animale
        list_display = ['nome', 'image_url',]

    # registriamo per l'admin
    admin.site.register(Animale, AnimaleAdmin)
    admin.site.register(Avvistamento, AvvistamentoAdmin)

A questo punto e' possibile creare delle istanze dei modelli con l'admin. Inserire qualche record, ovviamente il database si aggiorna di conseguenza::

    geodjango@geodjango-laptop:~/tutorial/django-1.2-alpha-1-env/foss4git$ psql -U geodjango tutorial
    psql (8.4.2)
    Type "help" for help.

    tutorial=> select * from fauna_animale;
     id | nome  |          foto          
    ----+-------+------------------------
      1 | Lupo  | animali.foto/lupo.jpg
      2 | Volpe | animali.foto/volpe.jpg
    (2 rows)

    tutorial=> select * from fauna_avvistamento;
     id |          data          |  note   | interesse | animale_id 
    ----+------------------------+---------+-----------+------------
      1 | 2010-02-05 01:38:08+01 | note... |         3 |          1
    (1 row)

Uso della shell di Django
-------------------------

Usiamo la shell per dimostrare i metodi CRUD::

    >>> from fauna.models import *
    >>> animali = Animale.objects.all()
    >>> animali
    [<Animale: Lupo>, <Animale: Volpe>]
    >>> lupo.nome
    u'Lupo'
    >>> lupo.foto
    <ImageFieldFile: animali.foto/lupo.jpg>
    >>> a1 = Avvistamento.objects.get(id=1)
    >>> a1
    <Avvistamento: 2010-02-04 18:38:08>
    >>> a1.animale = lupo
    >>> a1.interesse = 5
    >>> a1.save()
    >>> for a in avvistamenti:
       ....:     print a.animale
       ....:     print a.interesse
       ....:     print a.data
    Lupo
    3
    2010-02-04 18:38:08
    Lupo
    3
    2010-02-04 18:46:23
    Volpe
    1
    2010-02-04 18:46:37
    >>> nuovo_avvistamento = Avvistamento(data=datetime.now(), animale=lupo, interesse=5)
    >>> nuovo_avvistamento.save()
    >>> avvistamenti.count()
    3
    >>> avv_interessanti = Avvistamento.objects.filter(interesse__gte=4)
    >>> avv_interessanti.count()
    2

Creazione di una vista e di un template
---------------------------------------

Proviamo a creare una vista ed un template che presentino, nel lato pubblico dell'applicativo, un elenco degli avvistamenti inseriti nel template.

Come prima cosa inseriamo la nuova url nel file urls.py, ricordandosi di importare fauna.views (dove inseriremo la nuova vista)::

    from django.conf.urls.defaults import *
    from settings import STATIC_FILES
    from fauna.views import *
    ...
        # Uncomment the next line to enable the admin:
        (r'^admin/', include(admin.site.urls)),
        # indirizzi non soggetti ad autenticazione
        (r'^avvistamenti/', avvistamenti),
    ...

Poi creaimo la vista nel file views.py::

    from django.shortcuts import render_to_response, get_object_or_404
    from django.contrib.gis.shortcuts import render_to_kml
    from fauna.models import *

    # vista per visualizzare tutti i punti di avvistamento
    def avvistamenti(request):
        avvistamenti  = Avvistamento.objects.all()
        return render_to_response("avvistamenti.html", {'avvistamenti' : avvistamenti})

Infine creiamo la directory fauna/templates ed al suo interno inseriamo il template avvistamenti.html::

    <html>
      <head></head>
      <body>
        <h3>Avvistamenti in Italia</h3>
        <ul>
        {% for avv in avvistamenti %}
            <li>{{avv.animale.image_url|safe}} {{avv.data|date:"d M Y"}}, Interesse: {{avv.interesse}}</li>
        {% endfor %}
        </ul>
      </body>
    </html>

Si può a questo punto raggiungere la pagina http://localhost:8000/avvistamenti che dovrebbe visualizzare l'elenco degli avvistamenti.



