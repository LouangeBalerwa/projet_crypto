from flask import Flask, render_template, request,redirect, url_for, flash, session
import math as m

import base
import chiffrement
import copier
 
app = Flask(__name__)

app.secret_key ="mesclefs"

# =====================Login=======================
@app.route("/", methods =['GET', 'POST'])
def login():
    return render_template('loginPage.html')


# ==========page d'accueil, il retourne la page index et touts les donnees existants dans le bd================
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
    return render_template('index.html',liste_etudiant = liste_etudiant)

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
        # sql = "SELECT * FROM etudiant WHERE nom = %s AND matricule = %s"
        sql = "SELECT * FROM user WHERE nom = %s AND matricule = %s"
        valeurs = ( nom, matricule)
        cur.execute(sql,valeurs) 
        record = cur.fetchone()
        print(record)
        if record:
            session['nom'] = record[0]
            session['matricule'] = record[1]
            return redirect(url_for('accueil'))
        else:
            msg = "Nom ou Matricule incorrect!"
            return render_template('loginPage.html', message = msg)

# ======================cette fonction fait appel au formulaire=========================
@app.route('/to_save_std')
def formulaire():
    return render_template('formulaires.html')

# =========cette fonction enregistre les donnees provenant du formulaire.============
@app.route('/save_etudiant', methods =["POST", "GET"])
def save_etudiant():
   # print(request.args)
   if(request.method == "POST"):
    # cet request.form recuperer le donnees entrees dans le foromulaire
        data  =  request.form
        matricule = data.get('matricule')
        nom = data.get('nom')
        matric_chif = chiffrement.rsa(matricule,33,3)
        postnom = data.get('postenom')
        faculte = data.get('faculte')
        date_ns = data.get("date_ns")
        # il faut se connecter au bc pour enregister les donnees
        db=base.connecter()
        sql_ins = "INSERT INTO etudiant(matricule, nom , poste_nom, faculte, date_naissance) VALUES(%s, %s, %s, %s, %s)"
        valeurs =(matric_chif,nom,postnom,faculte,date_ns)
        # copier les nom et la matricule non crypter dans la table user pour confirmer le login
        sql_rec ="INSERT INTO user(matricule, nom) VALUES(%s, %s)"
        valeur_user=(matricule,nom)
        # Creaction un objet curseur
        cur = db.cursor()
        cur.execute(sql_ins, valeurs)
        cur.execute(sql_rec,valeur_user)
        db.commit()
        cur.close()
        return redirect(url_for('accueil'))

# ======================== supprimer ==================================#

@app.route('/supprimer/<string:matricule>',methods =["POST", "GET"])
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
    # # suprimer l'utilisateur  user 
    # sql_rec ="DELETE FROM user WHERE matricule =%s" 
    # valeur_user =(matricule,)
    # Exécution de la requête SQL pour supprimer la ligne
    cur.execute(sql,valeur)
    # cur.execute(sql_rec,valeur_user)
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
    
        
if __name__ =="__main__":
    app.run(debug=True)
    