=================
Prima di Iniziare
=================

Virtual Machine
---------------

L'organizzazione di foss4g-it 2010 mette a disposizione una VM per VirtualBox con tutto l'ambiente necessario a seguire il tutorial. Si riportano le caratteristiche di tale VM in maniera tale da poter replicare lo stesso ambiente e seguire in maniera ottimale il tutorial se non si avesse a disposizione la VM in questione.

Sistema operativo: Ubuntu 9.10 x86 Desktop

Segue un elenco del software installato.

Software installato dagli official sources:

* apache 2.2.12
* python-virtualenv
* subversion
* ipython 0.10
* postgres 8.4.2
* pgadmin III 1.10
* postgis 1.4.0
* psycopg 2.0.8
* cgi-mapserver 5.6.1
* python-mapscript

Software installato da ubuntugis-unstable:

* qgis 1.4
* libgdal1-1.6.0
* libgeos-3.1.1
* proj 4.7.0

Software installato dai source e compilando:

* libspatialite 2.3.1
* spatialite-tools 2.3.1
* pysqlite2 2.5.6
* geoip 1.4.4
* GeoIP-Python-1.2.2

Altre tipologie di software installato:

* Plugin Firefox: sqlite manager, webdeveloper e firebug

Configurazioni
--------------

Ubuntu
++++++

Usare queste credenziali per entrare nella virtual machine:
user: geodjango
password: geodjango

Postgres/PostGis
++++++++++++++++

L'utente amministrativo di postgres ha queste credenziali:
user: postgres
password: postgres

L'utente utilizzato nel tutorial e in tutte le applicazioni django/geodjango disponibili sulla VM ha queste credenziali:
user: geodjango
password: geodjango

gfoss4-it GeoDjango Tutorial
----------------------------

Per provare immediatamente il tutorial, si può procedere in questo modo.
Sulla VM esiste un virtualenv con django 1.2 collocato in: /home/geodjango/tutorial/django-1.2-alpha-1-env.
Attivare il virtualenv (basato su django 1.2-alpha1 e python 2.6) e lanciare l'applicazione, che è già configurata per girare su PostGis (il database è già stato creato).

Utente e password dell'utente di amministrazione di django sono:
user: admin
pwd: admin

C'è un WMS basato su mapserver in caso non ci sia connessione internet.
Il mapfile si trova qui e viene chiamato da openlayer:
/home/geodjango/tutorial/django-1.2-alpha-1-env/foss4git/mapserver/italia.map

GeoDjango-basic-apps
--------------------

Vedere: http://code.google.com/p/geodjango-basic-apps/

Sono tre demo che mostrano l'uso di GeoDjango, tutte configurate per accedere a postgres su locahost.
Tutte e tre si trovano in: /home/geodjango/tutorial/django-1.2-alpha-1-env/geodjango-basic-apps/projects
In tutti i casi utente e password dell'admin di django sono:
user: admin
pwd: admin

In particolare:

* geographic_admin mostra l'utilizzo delle application Django Admin e Databrowse abilitate spazialmente con GeoDjango (utilizzando OpenLayers)
(todo)

Per provare immediatamente le basic-apps, si può procedere in questo modo.
Sulla VM si trovano nel virtualenv con django 1.0 collocato in: /home/geodjango/tutorial/django-1.0-env/geodjango-basic-apps.
Attivare il virtualenv (basato su django 1.0 e python 2.5) e lanciare le applicazioni. Sono già configurate per girare su PostGis (i database sono già stati creati).

C'è un WMS basato su mapserver in caso non ci sia connessione internet.
Il mapfile si trova qui e viene chiamato da openlayer:
/home/geodjango/software/mapserver-stuff/cape.map

