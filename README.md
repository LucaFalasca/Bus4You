# Bus4You
Per poter usare l'applicazione sono necessari alcuni passi preliminari

### Scaricare il progetto
Come prima cosa bisogna clonare il progetto tramite git, oppure scaricarsi lo zip dell'applicazione. 

### Open Route Service Map
E' necessario scaricare la [mappa locale del centro italia](http://download.geofabrik.de/europe/italy/centro-latest.osm.pbf) 
ed inserirla nella cartella ors nei file dell'applicazione. 
Se la cartella non è presente, bisogna crearla.

![immagine](https://github.com/LucaFalasca/Bus4You/assets/30274870/1485bb77-febb-486a-b981-79999d8c9c62)

Gli altri file presenti nell'immagine verranno creati automaticamente una volta avviata l'applicazione, 
quindi non è necessario aggiungerli manualmente

### Avvio dell'applicazione
Per avviare l'applicazione è sufficiente posizionarsi nella cartella principale dell'applicazione,
aprire un terminale ed eseguire il comando
`docker compose up --build`



