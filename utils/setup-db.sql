insert into b4y_user_db.utente(mail,pwd,nome,cognome,username,data_nascita) 
values("prova@gmail.com", "1234", "prova", "prova", "prova", "2022-07-07");

insert into b4y_user_db.itinerario_richiesto(ora_inizio, ora_fine, costo_max, distanza, utente, fermata_lat_partenza, 
fermata_lon_partenza, fermata_lat_arrivo, fermata_lon_arrivo) values ("2022-07-07 10:00:00", "2022-07-07 10:30:00", 5, 10, "prova@gmail.com",
 41.648593, 12.431090, 41.658425, 12.422922);
 insert into b4y_user_db.itinerario_richiesto(ora_inizio, ora_fine, costo_max, distanza, utente, fermata_lat_partenza, 
fermata_lon_partenza, fermata_lat_arrivo, fermata_lon_arrivo) values ("2022-07-07 12:00:00", "2022-07-07 12:30:00", 5, 10, "prova@gmail.com",
 41.660835, 12.411013, 41.665523, 12.404817);
 
 
 insert into  b4y_user_db.percorso(id,scadenza, timestamp) values(1,"2024-12-12", now());
 
insert into b4y_user_db.ordinamento(numero, percorso, fermata_lat, fermata_lon) values(1, 1, 41.648593, 12.431090);
insert into b4y_user_db.ordinamento(numero, percorso, fermata_lat, fermata_lon) values(3, 1, 41.658425, 12.422922);
insert into b4y_user_db.ordinamento(numero, percorso, fermata_lat, fermata_lon) values(2, 1, 41.660835, 12.411013);
insert into b4y_user_db.ordinamento(numero, percorso, fermata_lat, fermata_lon) values(4, 1, 41.665523, 12.404817);

insert into b4y_user_db.itinerario_proposto(id, costo, distanza, orario_partenza_proposto, orario_arrivo_proposto,
utente, itinerario_richiesto, percorso, fermata_lat_partenza, fermata_lon_partenza, fermata_lat_arrivo, fermata_lon_arrivo)
values(1, 5, 10, "2022-07-07 10:00:00", "2022-07-07 10:30:00", "prova@gmail.com", 3, 1, 41.648593, 12.431090, 41.658425, 12.422922);
insert into b4y_user_db.itinerario_proposto(id, costo, distanza, orario_partenza_proposto, orario_arrivo_proposto,
utente, itinerario_richiesto, percorso, fermata_lat_partenza, fermata_lon_partenza, fermata_lat_arrivo, fermata_lon_arrivo)
values(2, 5, 10, "2022-07-07 12:00:00", "2022-07-07 12:30:00", "prova@gmail.com", 4, 1,41.660835, 12.411013, 41.665523, 12.404817);


