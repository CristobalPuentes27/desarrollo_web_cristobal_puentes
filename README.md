# Desarrollo de Aplicaciones Web

Entrega de la **tarea 2**

# Uso

Primero crea un ambiente de python

Correr todas las queries de tarea2.sql luego las de region-comuna.sql y tabla-comentario.sql


Correr

    pip install -r requirements.txt
    


finalmente hacer     
    
    flask run 

esto abrira la pagina mostrando el lobby de la web (el template index.html)

# Formato


> database (archivos relacionados a la base de datos)

> myenv (hay que borrarlo)

> static 

> > graphs (fotos de los graficos)

> > uploads (donde se guardan las fotos)

> > archivos css 

> > fotos del sistema

> > archivo js

> templates (archivos modificados de los html originales)

# Sobre la entrega actual

**Graficos:**

- Generan datos aleatoreos en un periodo de tres meses hacia atras si no hay suficiente informacion en la base de datos, mezclando los dos tipos de datos

- Como no hay un login, cualquiera puede comentar las veces que quiera, puse en app.py un detector de patrones para que no hagan un ingreso de texto malisioso, realmente nose bien si funciona
