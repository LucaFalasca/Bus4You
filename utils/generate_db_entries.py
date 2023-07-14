if __name__ == "__main__":
    for i in range(50,100):
        print("insert into  b4y_user_db.percorso(id,scadenza, tmstmp, stato) values("+str(i)+",'2024-12-12', now(), 'confirmed');")