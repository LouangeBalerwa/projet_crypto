from flask import Flask, render_template, request,redirect, url_for, flash, session
import math as m

import base
 
app = Flask(__name__)

app.secret_key ="mesclefs"

# page d'accueil, il retourne la page index et touts les donnees existants dans le bd
@app.route('/accueil')
def accueil():
    # appel du fonction base.py qui contient la connection du bd
    db=base.connecter()
    sql = "SELECT * FROM etudiant"
    cur = db.cursor()
    cur.execute(sql)
    # cette fonction fetchall() recuper tout les donnees du db apres l'execution du commande
    liste_etudiant = cur.fetchall()
    
    db.commit()
    cur.close()
    flash("Ajouter avec succe!")
    return render_template('index.html',liste_etudiant = liste_etudiant)

# ======================cette fonction fait appel au formulaire=========================
@app.route('/to_save_std')
def formulaire():
    return render_template('formulaires.html')

# cette fonction enregistre les donnees provenant du formulaire.
@app.route('/save_etudiant', methods =["POST", "GET"])
def save_etudiant():
   # print(request.args)
   if(request.method == "POST"):
    # cet request.form recuperer le donnees entrees dans le foromulaire
        data  =  request.form
        matricule = data.get('matricule')
        nom = data.get('nom')
        postnom = data.get('postenom')
        faculte = data.get('faculte')
        date_ns = data.get("date_ns")
        # il faut se connecter au bc pour enregister les donnees
        db=base.connecter()
        sql_ins = "INSERT INTO etudiant(matricule, nom , poste_nom, faculte, date_naissance) VALUES(%s, %s, %s, %s, %s)"
        valeurs =(matricule,nom,postnom,faculte,date_ns)

        # Creaction un objet curseur
        cur = db.cursor()
        cur.execute(sql_ins, valeurs)
        sql_celect = "SELECT * FROM etudiant"
        cur.execute(sql_celect)
        liste_etudiant = cur.fetchall()
        db.commit()
        cur.close()
        return redirect(url_for('accueil'))

@app.route("/copier_donnees")
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

# ======================== supprimer ==================================#

@app.route('/supprimer/<int:matricule>',methods =["POST", "GET"])
def supprimer_etudiant(matricule):
    # Établir la connexion à la base de données
    db =base.connecter()
    # Creaction un objet curseur
    cur = db.cursor()
    # recuperation de donnees
    # matricule_s =matricule
    # data  =  request.form
    # matricule = data.get('matricule')
    sql = "DELETE FROM etudiant WHERE matricule =%s" 
    valeur =(matricule,)
    # Exécution de la requête SQL pour supprimer la ligne
    cur.execute(sql,valeur)
    # Valition de  la transaction
    db.commit()
    cur.close()
    return redirect(url_for('accueil'))

# ======================== modifier ==================================#

@app.route('/editer/<mat>',methods =["POST", "GET"])
def edit_etudiant(mat):
    # Établir la connexion à la base de données
    db =base.connecter()
    # Creaction un objet curseur
    cur = db.cursor()
    matricule = mat
    cur.execute('SELECT * FROM etudiant WHERE matricule = %s',(matricule,))
    data = cur.fetchall()
    return render_template('edit_affiche.html', etudiant_select = data[0])

# ======================== mise a jour ! ==================================#

@app.route('/mise_a_jour_etudiant/<matricule>',methods =["POST", "GET"])
def mise_a_jour_etudiant(matricule):
    db =base.connecter()
    # Creaction un objet curseur
    cur = db.cursor()
    if(request.method == "POST"):
    # cet request.form recuperer le donnees entrees dans le foromulaire
        data  =  request.form
        nom = data.get('nom')
        postnom = data.get('postenom')
        faculte = data.get('faculte')
        date_ns = data.get("date_ns")
        sql = "UPDATE etudiant SET nom = %s, poste_nom = %s,faculte = %s, date_naissance =%s WHERE matricule= %s"
        valuers =(nom,postnom,faculte,date_ns,matricule,)
        cur.execute(sql,valuers)    
        db.commit()
        cur.close()
        return redirect(url_for('accueil'))
    
# =====================Login=======================
@app.route("/", methods =['GET', 'POST'])
def login():
    return render_template('loginPage.html')

# =================Confirmation du Login ===========
@app.route('/confirmation', methods =['GET', 'POST'])
def confirmation():
    db =base.connecter()
    # Creaction un objet curseur
    cur = db.cursor()
    msg = ""
    if request.method == 'POST':
        nom = request.form.get('nom')
        matricule = request.form.get('matricule')
        sql = "SELECT * FROM etudiant WHERE nom = %s AND matricule = %s"
        # sql = "SELECT * FROM user WHERE nom = %s AND matricule = %s"
        valeurs = ( nom, matricule)
        cur.execute(sql,valeurs) 
        record = cur.fetchone()
        print(record)
        if record:
            session['nom'] = record[0]
            session['matricule'] = record[1]
            return redirect(url_for('accueil'))
        else:
            msg = "Nom ou Matricule inconus!!!"
            return render_template('loginPage.html', message = msg)
        
if __name__ =="__main__":
    app.run(debug=True)
    



# chiffrement avec RSA
# def rsa(texte,n,e):
#     cipherText = []
#     codeChart = "abcdefghijklmnopqrstuvwxyz"
    
#     for key in codeChart:
#         for i in texte:
#             if key == i:
#                 char = codeChart.index(key)
# #             print(char)
#                 c = int(m.pow(char,e)%n)
# #             print(c)
#                 cipherText.append(c)
#     return cipherText
        
# # message ="hi"
# print (rsa("hi",33,3))