import base

def copier_donnees():
    db=base.connecter()
    cursor = db.cursor()
    # Exécuter la requête INSERT INTO
    cursor.execute("""
        INSERT INTO user (matricule, nom)
        SELECT matricule, nom
        FROM etudiant;
    """)
    db.commit()
    cursor.close()
    db.close()
    return "Données copiées avec succès!"