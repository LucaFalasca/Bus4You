#Utente
insert into b4y_user_db.utente(mail,pwd,nome,cognome,username,data_nascita) 
values("prova@gmail.com", "1234", "prova", "prova", "prova", "2022-07-07");

#Itinerari richiesti
insert into b4y_user_db.itinerario_richiesto(ora_inizio, ora_fine, costo_max, distanza, utente, fermata_lat_partenza, 
fermata_lon_partenza, fermata_lat_arrivo, fermata_lon_arrivo) values ("2022-07-07 10:00:00", "2022-07-07 10:30:00", 5, 10, "prova@gmail.com",
 41.648593, 12.431090, 41.658425, 12.422922);
 insert into b4y_user_db.itinerario_richiesto(ora_inizio, ora_fine, costo_max, distanza, utente, fermata_lat_partenza, 
fermata_lon_partenza, fermata_lat_arrivo, fermata_lon_arrivo) values ("2022-07-07 12:00:00", "2022-07-07 12:30:00", 5, 10, "prova@gmail.com",
 41.660835, 12.411013, 41.665523, 12.404817);
 
 #Percorso pending
 insert into  b4y_user_db.percorso(id,scadenza, timestamp) values(1,"2024-12-12", now());
 
 #Relazione percorso fermata, cioè fermate che formano il percorso
insert into b4y_user_db.ordinamento(numero, percorso, fermata_lat, fermata_lon) values(1, 1, 41.648593, 12.431090);
insert into b4y_user_db.ordinamento(numero, percorso, fermata_lat, fermata_lon) values(3, 1, 41.658425, 12.422922);
insert into b4y_user_db.ordinamento(numero, percorso, fermata_lat, fermata_lon) values(2, 1, 41.660835, 12.411013);
insert into b4y_user_db.ordinamento(numero, percorso, fermata_lat, fermata_lon) values(4, 1, 41.665523, 12.404817);

#Itinerari proposti pending del percorso pending
insert into b4y_user_db.itinerario_proposto(id, costo, distanza, orario_partenza_proposto, orario_arrivo_proposto,
utente, itinerario_richiesto, percorso, fermata_lat_partenza, fermata_lon_partenza, fermata_lat_arrivo, fermata_lon_arrivo)
values(1, 5, 10, "2022-07-07 10:00:00", "2022-07-07 10:30:00", "prova@gmail.com", 3, 1, 41.648593, 12.431090, 41.658425, 12.422922);
insert into b4y_user_db.itinerario_proposto(id, costo, distanza, orario_partenza_proposto, orario_arrivo_proposto,
utente, itinerario_richiesto, percorso, fermata_lat_partenza, fermata_lon_partenza, fermata_lat_arrivo, fermata_lon_arrivo)
values(2, 5, 10, "2022-07-07 12:00:00", "2022-07-07 12:30:00", "prova@gmail.com", 4, 1,41.660835, 12.411013, 41.665523, 12.404817);


#Itinerari proposti scartati del percorso pending
insert into b4y_user_db.itinerario_proposto(id, costo, distanza, orario_partenza_proposto, orario_arrivo_proposto,
utente, itinerario_richiesto, percorso, fermata_lat_partenza, fermata_lon_partenza, fermata_lat_arrivo, fermata_lon_arrivo, stato)
values(3, 5, 10, "2022-07-07 12:00:00", "2022-07-07 12:30:00", "prova@gmail.com", 4, 1,41.660835, 12.411013, 41.665523, 12.404817, 'rejected');
insert into b4y_user_db.itinerario_proposto(id, costo, distanza, orario_partenza_proposto, orario_arrivo_proposto,
utente, itinerario_richiesto, percorso, fermata_lat_partenza, fermata_lon_partenza, fermata_lat_arrivo, fermata_lon_arrivo, stato)
values(4, 5, 10, "2022-07-07 12:00:00", "2022-07-07 12:30:00", "prova@gmail.com", 4, 1,41.660835, 12.411013, 41.665523, 12.404817, 'rejected');
insert into b4y_user_db.itinerario_proposto(id, costo, distanza, orario_partenza_proposto, orario_arrivo_proposto,
utente, itinerario_richiesto, percorso, fermata_lat_partenza, fermata_lon_partenza, fermata_lat_arrivo, fermata_lon_arrivo, stato)
values(5, 5, 10, "2022-07-07 12:00:00", "2022-07-07 12:30:00", "prova@gmail.com", 4, 1,41.660835, 12.411013, 41.665523, 12.404817, 'rejected');


#Itinerari proposti confermati del percorso pending
insert into b4y_user_db.itinerario_proposto(id, costo, distanza, orario_partenza_proposto, orario_arrivo_proposto,
utente, itinerario_richiesto, percorso, fermata_lat_partenza, fermata_lon_partenza, fermata_lat_arrivo, fermata_lon_arrivo, stato)
values(6, 5, 10, "2022-07-07 12:00:00", "2022-07-07 12:30:00", "prova@gmail.com", 4, 1,41.660835, 12.411013, 41.665523, 12.404817, 'confirmed');
insert into b4y_user_db.itinerario_proposto(id, costo, distanza, orario_partenza_proposto, orario_arrivo_proposto,
utente, itinerario_richiesto, percorso, fermata_lat_partenza, fermata_lon_partenza, fermata_lat_arrivo, fermata_lon_arrivo, stato)
values(7, 5, 10, "2022-07-07 12:00:00", "2022-07-07 12:30:00", "prova@gmail.com", 4, 1,41.660835, 12.411013, 41.665523, 12.404817, 'confirmed');
insert into b4y_user_db.itinerario_proposto(id, costo, distanza, orario_partenza_proposto, orario_arrivo_proposto,
utente, itinerario_richiesto, percorso, fermata_lat_partenza, fermata_lon_partenza, fermata_lat_arrivo, fermata_lon_arrivo, stato)
values(8, 5, 10, "2022-07-07 12:00:00", "2022-07-07 12:30:00", "prova@gmail.com", 4, 1,41.660835, 12.411013, 41.665523, 12.404817, 'confirmed');


#Percorso confermato presente
 insert into  b4y_user_db.percorso(id,scadenza, timestamp, stato) values(2,"2024-12-12", now(), 'confirmed');
 
 #Relazione percorso fermata, cioè fermate che formano il percorso
insert into b4y_user_db.ordinamento(numero, percorso, fermata_lat, fermata_lon) values(1, 2, 41.648593, 12.431090);
insert into b4y_user_db.ordinamento(numero, percorso, fermata_lat, fermata_lon) values(3, 2, 41.658425, 12.422922);
insert into b4y_user_db.ordinamento(numero, percorso, fermata_lat, fermata_lon) values(2, 2, 41.660835, 12.411013);
insert into b4y_user_db.ordinamento(numero, percorso, fermata_lat, fermata_lon) values(4, 2, 41.665523, 12.404817);

#Itinerari proposti pending del percorso 
insert into b4y_user_db.itinerario_proposto(id, costo, distanza, orario_partenza_proposto, orario_arrivo_proposto,
utente, itinerario_richiesto, percorso, fermata_lat_partenza, fermata_lon_partenza, fermata_lat_arrivo, fermata_lon_arrivo)
values(9, 5, 10, "2022-07-07 10:00:00", "2022-07-07 10:30:00", "prova@gmail.com", 3, 2, 41.648593, 12.431090, 41.658425, 12.422922);
insert into b4y_user_db.itinerario_proposto(id, costo, distanza, orario_partenza_proposto, orario_arrivo_proposto,
utente, itinerario_richiesto, percorso, fermata_lat_partenza, fermata_lon_partenza, fermata_lat_arrivo, fermata_lon_arrivo)
values(10, 5, 10, "2022-07-07 12:00:00", "2022-07-07 12:30:00", "prova@gmail.com", 4, 2,41.660835, 12.411013, 41.665523, 12.404817);


#Itinerari proposti scartati del percorso confermato
insert into b4y_user_db.itinerario_proposto(id, costo, distanza, orario_partenza_proposto, orario_arrivo_proposto,
utente, itinerario_richiesto, percorso, fermata_lat_partenza, fermata_lon_partenza, fermata_lat_arrivo, fermata_lon_arrivo, stato)
values(11, 5, 10, "2022-07-07 12:00:00", "2022-07-07 12:30:00", "prova@gmail.com", 4, 2, 41.660835, 12.411013, 41.665523, 12.404817, 'rejected');
insert into b4y_user_db.itinerario_proposto(id, costo, distanza, orario_partenza_proposto, orario_arrivo_proposto,
utente, itinerario_richiesto, percorso, fermata_lat_partenza, fermata_lon_partenza, fermata_lat_arrivo, fermata_lon_arrivo, stato)
values(12, 5, 10, "2022-07-07 12:00:00", "2022-07-07 12:30:00", "prova@gmail.com", 4, 2, 41.660835, 12.411013, 41.665523, 12.404817, 'rejected');
insert into b4y_user_db.itinerario_proposto(id, costo, distanza, orario_partenza_proposto, orario_arrivo_proposto,
utente, itinerario_richiesto, percorso, fermata_lat_partenza, fermata_lon_partenza, fermata_lat_arrivo, fermata_lon_arrivo, stato)
values(13, 5, 10, "2022-07-07 12:00:00", "2022-07-07 12:30:00", "prova@gmail.com", 4, 2, 41.660835, 12.411013, 41.665523, 12.404817, 'rejected');


#Itinerari proposti confermati del percorso confermato
insert into b4y_user_db.itinerario_proposto(id, costo, distanza, orario_partenza_proposto, orario_arrivo_proposto,
utente, itinerario_richiesto, percorso, fermata_lat_partenza, fermata_lon_partenza, fermata_lat_arrivo, fermata_lon_arrivo, stato)
values(14, 5, 10, "2022-07-07 12:00:00", "2022-07-07 12:30:00", "prova@gmail.com", 4, 2, 41.660835, 12.411013, 41.665523, 12.404817, 'confirmed');
insert into b4y_user_db.itinerario_proposto(id, costo, distanza, orario_partenza_proposto, orario_arrivo_proposto,
utente, itinerario_richiesto, percorso, fermata_lat_partenza, fermata_lon_partenza, fermata_lat_arrivo, fermata_lon_arrivo, stato)
values(15, 5, 10, "2022-07-07 12:00:00", "2022-07-07 12:30:00", "prova@gmail.com", 4, 2, 41.660835, 12.411013, 41.665523, 12.404817, 'confirmed');
insert into b4y_user_db.itinerario_proposto(id, costo, distanza, orario_partenza_proposto, orario_arrivo_proposto,
utente, itinerario_richiesto, percorso, fermata_lat_partenza, fermata_lon_partenza, fermata_lat_arrivo, fermata_lon_arrivo, stato)
values(16, 5, 10, "2022-07-07 12:00:00", "2022-07-07 12:30:00", "prova@gmail.com", 4, 2, 41.660835, 12.411013, 41.665523, 12.404817, 'confirmed');


#Percorso rejected
 insert into  b4y_user_db.percorso(id,scadenza, timestamp, stato, archiviato) values(3, "2024-12-12", now(), 'rejected', 1);
 
 #Relazione percorso fermata, cioè fermate che formano il percorso
insert into b4y_user_db.ordinamento(numero, percorso, fermata_lat, fermata_lon) values(1, 3, 41.648593, 12.431090);
insert into b4y_user_db.ordinamento(numero, percorso, fermata_lat, fermata_lon) values(3, 3, 41.658425, 12.422922);
insert into b4y_user_db.ordinamento(numero, percorso, fermata_lat, fermata_lon) values(2, 3, 41.660835, 12.411013);
insert into b4y_user_db.ordinamento(numero, percorso, fermata_lat, fermata_lon) values(4, 3, 41.665523, 12.404817);

#Itinerari proposti pending del percorso rejected
insert into b4y_user_db.itinerario_proposto(id, costo, distanza, orario_partenza_proposto, orario_arrivo_proposto,
utente, itinerario_richiesto, percorso, fermata_lat_partenza, fermata_lon_partenza, fermata_lat_arrivo, fermata_lon_arrivo)
values(17, 5, 10, "2022-07-07 10:00:00", "2022-07-07 10:30:00", "prova@gmail.com", 3, 3, 41.648593, 12.431090, 41.658425, 12.422922);
insert into b4y_user_db.itinerario_proposto(id, costo, distanza, orario_partenza_proposto, orario_arrivo_proposto,
utente, itinerario_richiesto, percorso, fermata_lat_partenza, fermata_lon_partenza, fermata_lat_arrivo, fermata_lon_arrivo)
values(18, 5, 10, "2022-07-07 12:00:00", "2022-07-07 12:30:00", "prova@gmail.com", 4, 3,41.660835, 12.411013, 41.665523, 12.404817);


#Itinerari proposti scartati del percorso rejected
insert into b4y_user_db.itinerario_proposto(id, costo, distanza, orario_partenza_proposto, orario_arrivo_proposto,
utente, itinerario_richiesto, percorso, fermata_lat_partenza, fermata_lon_partenza, fermata_lat_arrivo, fermata_lon_arrivo, stato)
values(19, 5, 10, "2022-07-07 12:00:00", "2022-07-07 12:30:00", "prova@gmail.com", 4, 3, 41.660835, 12.411013, 41.665523, 12.404817, 'rejected');
insert into b4y_user_db.itinerario_proposto(id, costo, distanza, orario_partenza_proposto, orario_arrivo_proposto,
utente, itinerario_richiesto, percorso, fermata_lat_partenza, fermata_lon_partenza, fermata_lat_arrivo, fermata_lon_arrivo, stato)
values(20, 5, 10, "2022-07-07 12:00:00", "2022-07-07 12:30:00", "prova@gmail.com", 4, 3, 41.660835, 12.411013, 41.665523, 12.404817, 'rejected');
insert into b4y_user_db.itinerario_proposto(id, costo, distanza, orario_partenza_proposto, orario_arrivo_proposto,
utente, itinerario_richiesto, percorso, fermata_lat_partenza, fermata_lon_partenza, fermata_lat_arrivo, fermata_lon_arrivo, stato)
values(21, 5, 10, "2022-07-07 12:00:00", "2022-07-07 12:30:00", "prova@gmail.com", 4, 3, 41.660835, 12.411013, 41.665523, 12.404817, 'rejected');


#Itinerari proposti confermati del percorso rejected
insert into b4y_user_db.itinerario_proposto(id, costo, distanza, orario_partenza_proposto, orario_arrivo_proposto,
utente, itinerario_richiesto, percorso, fermata_lat_partenza, fermata_lon_partenza, fermata_lat_arrivo, fermata_lon_arrivo, stato)
values(22, 5, 10, "2022-07-07 12:00:00", "2022-07-07 12:30:00", "prova@gmail.com", 4, 3, 41.660835, 12.411013, 41.665523, 12.404817, 'confirmed');
insert into b4y_user_db.itinerario_proposto(id, costo, distanza, orario_partenza_proposto, orario_arrivo_proposto,
utente, itinerario_richiesto, percorso, fermata_lat_partenza, fermata_lon_partenza, fermata_lat_arrivo, fermata_lon_arrivo, stato)
values(23, 5, 10, "2022-07-07 12:00:00", "2022-07-07 12:30:00", "prova@gmail.com", 4, 3, 41.660835, 12.411013, 41.665523, 12.404817, 'confirmed');
insert into b4y_user_db.itinerario_proposto(id, costo, distanza, orario_partenza_proposto, orario_arrivo_proposto,
utente, itinerario_richiesto, percorso, fermata_lat_partenza, fermata_lon_partenza, fermata_lat_arrivo, fermata_lon_arrivo, stato)
values(24, 5, 10, "2022-07-07 12:00:00", "2022-07-07 12:30:00", "prova@gmail.com", 4, 3, 41.660835, 12.411013, 41.665523, 12.404817, 'confirmed');


#Percorso confermato passato
 insert into  b4y_user_db.percorso(id,scadenza, timestamp, stato, archiviato) values(4, "2024-12-12", now(), 'confirmed', 1);
 
 #Relazione percorso fermata, cioè fermate che formano il percorso
insert into b4y_user_db.ordinamento(numero, percorso, fermata_lat, fermata_lon) values(1, 4, 41.648593, 12.431090);
insert into b4y_user_db.ordinamento(numero, percorso, fermata_lat, fermata_lon) values(3, 4, 41.658425, 12.422922);
insert into b4y_user_db.ordinamento(numero, percorso, fermata_lat, fermata_lon) values(2, 4, 41.660835, 12.411013);
insert into b4y_user_db.ordinamento(numero, percorso, fermata_lat, fermata_lon) values(4, 4, 41.665523, 12.404817);

#Itinerari proposti pending del percorso confermato passato
insert into b4y_user_db.itinerario_proposto(id, costo, distanza, orario_partenza_proposto, orario_arrivo_proposto,
utente, itinerario_richiesto, percorso, fermata_lat_partenza, fermata_lon_partenza, fermata_lat_arrivo, fermata_lon_arrivo)
values(25, 5, 10, "2022-07-07 10:00:00", "2022-07-07 10:30:00", "prova@gmail.com", 3, 4, 41.648593, 12.431090, 41.658425, 12.422922);
insert into b4y_user_db.itinerario_proposto(id, costo, distanza, orario_partenza_proposto, orario_arrivo_proposto,
utente, itinerario_richiesto, percorso, fermata_lat_partenza, fermata_lon_partenza, fermata_lat_arrivo, fermata_lon_arrivo)
values(26, 5, 10, "2022-07-07 12:00:00", "2022-07-07 12:30:00", "prova@gmail.com", 4, 4,41.660835, 12.411013, 41.665523, 12.404817);


#Itinerari proposti scartati del percorso confermato passato
insert into b4y_user_db.itinerario_proposto(id, costo, distanza, orario_partenza_proposto, orario_arrivo_proposto,
utente, itinerario_richiesto, percorso, fermata_lat_partenza, fermata_lon_partenza, fermata_lat_arrivo, fermata_lon_arrivo, stato)
values(27, 5, 10, "2022-07-07 12:00:00", "2022-07-07 12:30:00", "prova@gmail.com", 4, 4, 41.660835, 12.411013, 41.665523, 12.404817, 'rejected');
insert into b4y_user_db.itinerario_proposto(id, costo, distanza, orario_partenza_proposto, orario_arrivo_proposto,
utente, itinerario_richiesto, percorso, fermata_lat_partenza, fermata_lon_partenza, fermata_lat_arrivo, fermata_lon_arrivo, stato)
values(28, 5, 10, "2022-07-07 12:00:00", "2022-07-07 12:30:00", "prova@gmail.com", 4, 4, 41.660835, 12.411013, 41.665523, 12.404817, 'rejected');
insert into b4y_user_db.itinerario_proposto(id, costo, distanza, orario_partenza_proposto, orario_arrivo_proposto,
utente, itinerario_richiesto, percorso, fermata_lat_partenza, fermata_lon_partenza, fermata_lat_arrivo, fermata_lon_arrivo, stato)
values(29, 5, 10, "2022-07-07 12:00:00", "2022-07-07 12:30:00", "prova@gmail.com", 4, 4, 41.660835, 12.411013, 41.665523, 12.404817, 'rejected');


#Itinerari proposti confermati del percorso confermato passato
insert into b4y_user_db.itinerario_proposto(id, costo, distanza, orario_partenza_proposto, orario_arrivo_proposto,
utente, itinerario_richiesto, percorso, fermata_lat_partenza, fermata_lon_partenza, fermata_lat_arrivo, fermata_lon_arrivo, stato)
values(30, 5, 10, "2022-07-07 12:00:00", "2022-07-07 12:30:00", "prova@gmail.com", 4, 4, 41.660835, 12.411013, 41.665523, 12.404817, 'confirmed');
insert into b4y_user_db.itinerario_proposto(id, costo, distanza, orario_partenza_proposto, orario_arrivo_proposto,
utente, itinerario_richiesto, percorso, fermata_lat_partenza, fermata_lon_partenza, fermata_lat_arrivo, fermata_lon_arrivo, stato)
values(31, 5, 10, "2022-07-07 12:00:00", "2022-07-07 12:30:00", "prova@gmail.com", 4, 4, 41.660835, 12.411013, 41.665523, 12.404817, 'confirmed');
insert into b4y_user_db.itinerario_proposto(id, costo, distanza, orario_partenza_proposto, orario_arrivo_proposto,
utente, itinerario_richiesto, percorso, fermata_lat_partenza, fermata_lon_partenza, fermata_lat_arrivo, fermata_lon_arrivo, stato)
values(32, 5, 10, "2022-07-07 12:00:00", "2022-07-07 12:30:00", "prova@gmail.com", 4, 4, 41.660835, 12.411013, 41.665523, 12.404817, 'confirmed');
