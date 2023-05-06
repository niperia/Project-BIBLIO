import tkinter as tk
from tkinter import messagebox
from tkinter import *
from tkinter import ttk
import os
from tkinter import filedialog
from tkinter.filedialog import askopenfile
import mysql.connector as mysql
from PIL import Image, ImageTk
import functools


db = mysql.connect(
    host="localhost",
    user="root",
    password="root",
    database="bibliotheque"
)


class personne():
    def __init__(self, Username, Password, Nom, Prenom, Adresse, Email, Numero):
        self.Username = Username
        self.Password = Password
        self.Nom = Nom
        self.Prenom = Prenom
        self.Adresse = Adresse
        self.Email = Email
        self.Numero = Numero

    def newframe(self):
        if self.tk:
            self.tk.destroy()

        self.tk = Tk()
        self.tk.title("BIBLIO")
        self.tk.geometry("1500x1500")
        img = Image.open("library.jpg")
        img = img.resize((1000, 300), Image.ANTIALIAS)
        # Store the image as an attribute
        self.bg_image = ImageTk.PhotoImage(img)
        bg_label = Label(self.tk, image=self.bg_image)
        bg_label.pack()
        frame = Frame(self.tk)
        frame.pack(pady=20)
        return frame

    def register(self):
        frame = self.newframe()

        Label(frame, text="Username: ").grid(row=0, column=0, padx=10, pady=5)
        self.Username = Entry(frame, textvariable=StringVar)
        self.Username.grid(row=0, column=1, padx=10, pady=5)

        Label(frame, text="Nom: ").grid(row=1, column=0, padx=10, pady=5)
        self.Nom = Entry(frame, textvariable=StringVar)
        self.Nom.grid(row=1, column=1, padx=10, pady=5)

        Label(frame, text="Prenom: ").grid(row=2, column=0, padx=10, pady=5)
        self.Prenom = Entry(frame, textvariable=StringVar)
        self.Prenom.grid(row=2, column=1, padx=10, pady=5)

        Label(frame, text="Adresse: ").grid(row=3, column=0, padx=10, pady=5)
        self.Adresse = Entry(frame, textvariable=StringVar)
        self.Adresse.grid(row=3, column=1, padx=10, pady=5)

        Label(frame, text="Email: ").grid(row=4, column=0, padx=10, pady=5)
        self.AdresseEmail = Entry(frame, textvariable=StringVar)
        self.AdresseEmail.grid(row=4, column=1, padx=10, pady=5)

        Label(frame, text="Numero: ").grid(row=5, column=0, padx=10, pady=5)
        self.Numero = Entry(frame, textvariable=StringVar)
        self.Numero.grid(row=5, column=1, padx=10, pady=5)

        Label(frame, text="Password: ").grid(row=6, column=0, padx=10, pady=5)
        self.Password = Entry(frame, textvariable=StringVar)
        self.Password.grid(row=6, column=1, padx=10, pady=5)

        Button(frame, text="Register", command=self.insert, bg="#008CBA", fg="white", font=("Arial", 14)).grid(
            row=7, column=0, columnspan=2, padx=10, pady=10)

    def insert(self):
        username = self.Username.get()
        nom = self.Nom.get()
        prenom = self.Prenom.get()
        adresse = self.Adresse.get()
        email = self.AdresseEmail.get()
        numero = self.Numero.get()

        if (username == "" or nom == "" or prenom == "" or adresse == "" or email == "" or numero == ""):
            return messagebox.showerror("ERROR", "veuillez remplir les champs :) ")

        mycursor = db.cursor()
        mycursor.execute("INSERT INTO personne(username,Nom,Prenom,Adresse,AdresseEmail,Numero,password) VALUES (%s,%s,%s,%s,%s,%s,%s)",
                         (self.Username.get(), self.Nom.get(), self.Prenom.get(), self.Adresse.get(), self.AdresseEmail.get(), self.Numero.get(), self.Password.get()))
        db.commit()
        self.menu1()

    def menu1(self):
        frame = self.newframe()
        frame.configure(bg='#FFFFFF')

        label_menu = Label(frame, text="Menu", font=(
            'Arial', 18, 'bold'), bg='#FFFFFF', fg='#282c34')
        label_menu.pack(pady=20)

        btn_afficher = Button(frame, text="Afficher les livres", command=self.AfficherLivres_user, font=(
            'Arial', 12), bg='#0078d7', fg='#FFFFFF', padx=20, pady=10)
        btn_afficher.pack(pady=10)

        btn_chercher = Button(frame, text="Chercher un livre", command=self.recherche_user_livre, font=(
            'Arial', 12), bg='#0078d7', fg='#FFFFFF', padx=20, pady=10)
        btn_chercher.pack(pady=10)

        btn_emprunter = Button(frame, text="Emprunter un livre", command=self.Emprunter_livre, font=(
            'Arial', 12), bg='#0078d7', fg='#FFFFFF', padx=20, pady=10)
        btn_emprunter.pack(pady=10)

    def Emprunter_livre(self):
        frame = self.newframe()
        Label(frame, text="Saisir le titre du livre à rechercher:",
              font=("Arial", 18), fg="brown").pack()
        self.recher = Entry(frame, textvariable=StringVar,
                            font=("Arial", 16), bg="#F0F0F0")
        self.recher.pack(pady=10)
        b1 = Button(frame, text="Chercher", command=self.chercher_livre, font=(
            "Arial", 16), bg="#4CAF50", fg="white")
        b1.pack(pady=10)
        Button(frame, text="Retour au menu", command=self.menu1, font=(
            "Arial", 16), bg="#F44336", fg="white").pack(pady=10)

    def chercher_livre(self):
        global img
        r = self.recher.get()
        self.iduser = " "
        if (r == ""):
            return messagebox.showinfo("Erreur", "la barre de recherche est vide")
        elif (r != ""):
            mycursor = db.cursor()
            mycursor.execute(
                "SELECT empruntpar FROM livre WHERE Titre= '" + r + "'")
            livrees = mycursor.fetchall()
            print(livrees)
            if (livrees == None):
                return messagebox.showerror("erreur", "table emprumt est vide")
            for livre in livrees:
                liv = self.convertTuple(livre)
                if (liv != ""):
                    return messagebox.showerror("erreur", "livre deja empunter")

            mycursor = db.cursor()
            mycursor.execute(
                "SELECT idpersonne FROM personne WHERE username= '" + g + "'")
            titres = mycursor.fetchall()
            for t in titres:
                self.iduser = (t)
                break
            mycursor = db.cursor()
            mycursor.execute("SELECT Titre FROM livre")
            livres = mycursor.fetchall()
            for a in livres:
                if (self.convertTuple(a) == r):
                    mycursor = db.cursor()
                    mycursor.execute(
                        "SELECT idLivre FROM livre WHERE Titre= '" + r + "' ")
                    titres = mycursor.fetchall()
                    for e in titres:
                        self.idlivre = e
                        break
                    messagebox.showinfo("Message", "livre existe")
                    Button(text="Emprunter un livre",
                           command=self.Emprunter).pack()
                    return 1

            return messagebox.showerror("erreur", "Le livre n'a pas été trouvé")

    def Emprunter(self):
        frame = self.newframe()
        Label(frame, text="Saisir la date d'emprunt de ce livre: ", font=('Arial', 12),
              background='white').pack()

        self.date_emp = Entry(frame, textvariable=StringVar, font=('Arial', 12),
                              background='white')
        self.date_emp.pack()

        btn = Button(frame, text="Emprunter un livre", font=('Arial', 12),
                     foreground='white', background='#0078d7', padx=10, pady=5, command=self.inserer_emp)
        btn.pack()
        button_menu = Button(frame, text="Retour au menu", font=(
            "Arial", 12), fg="white", bg="#0078d7", padx=10, pady=5, command=self.menu1)
        button_menu.pack(pady=10)

    def inserer_emp(self):

        if self.date_emp.get() == "":
            messagebox.showerror("Erreur", "Champ de date vide")
        else:
            self.a1 = functools.reduce(
                lambda sub, ele: sub * 10 + ele, self.idlivre)
            self.a2 = functools.reduce(
                lambda sub, ele: sub * 10 + ele, self.iduser)
            print("***")
            print(self.a1)
            print(self.a2)
            mycursor = db.cursor()
            mycursor.execute("INSERT INTO emprunte(idlivre,idpersonne,date_emp) VALUES (%s,%s,%s)",
                             ((self.a1), (self.a2), self.date_emp.get()))
            print(g)

            mycursor.execute("UPDATE livre SET empruntpar = '" +
                             g + "' WHERE (`idLivre` = '" + str(self.a1) + "')")
            db.commit()

    def recherche_user_livre(self):
        frame = self.newframe()
        frame.configure(bg='#282c34')

        label_title = Label(frame, text="Rechercher un livre", font=(
            "Arial", 16), fg="white", bg='#282c34')
        label_title.pack(pady=20)

        label_search = Label(frame, text="Titre du livre: ", font=(
            "Arial", 12), fg="white", bg='#282c34')
        label_search.pack()

        self.recher = Entry(frame, textvariable=StringVar, font=(
            "Arial", 12), fg="#282c34", bg="white")
        self.recher.pack(pady=10)

        b1 = Button(frame, text="Chercher", font=("Arial", 12), fg="white",
                    bg="#0078d7", padx=10, pady=5, command=self.chercher_livre2)
        b1.pack(pady=10)

        button_menu = Button(frame, text="Retour au menu", font=(
            "Arial", 12), fg="white", bg="#0078d7", padx=10, pady=5, command=self.menu1)
        button_menu.pack(pady=10)

    def chercher_livre2(self):
        global img
        r = self.recher.get()

        if r == "":
            messagebox.showinfo("Erreur", "La barre de recherche est vide555")
        else:
            mycursor = db.cursor()
            mycursor.execute("SELECT Titre FROM livre")
            titres = mycursor.fetchall()

            for t in titres:
                if self.convertTuple(t) == r:
                    frame = self.newframe()
                    mycursor.execute(
                        "SELECT * FROM livre WHERE Titre = '" + r + "'")
                    lists = mycursor.fetchall()
                    Headstr = [mycursor.column_names]
                    Hrows = len(Headstr)
                    Hcolumns = len(Headstr[0])
                    rows = len(lists)
                    columns = len(lists[0])

                    for i in range(Hrows):
                        for j in range(Hcolumns):
                            self.e = Entry(frame, fg='brown',
                                           font=('Arial', 16, 'bold'))
                            self.e.grid(row=i, column=j)
                            self.e.insert(END, Headstr[i][j])

                    for i in range(rows):
                        for j in range(4):
                            b1 = tk.Label(
                                frame, text=lists[i][j], fg='blue', font=('Arial', 16))
                            b1.grid(row=i+1, column=j)
                            b1 = tk.Label(frame, text=lists[i][5], fg='blue', font=(
                                'Arial', 16), bg='white', width=15)
                            b1.grid(row=i+1, column=5)
                            path = str(lists[i][4])
                            img = ImageTk.PhotoImage(Image.open(
                                r"C:\Users\hp\Desktop\Projet\images/"+path))
                            b2 = tk.Button(frame, image=img,
                                           height=100, width=100)
                            b2.image_names = img
                            b2.grid(row=i+1, column=4)

                        b3 = tk.Button(frame, text="vers menu",
                                       command=self.menu1, background='red')
                        b3.grid(row=i+2, column=0)

                    return 1

            return messagebox.showerror("Erreur", "Le livre n'a pas été trouvé")

    def AfficherLivres_user(self):

        frame = self.newframe()
        mycursor = db.cursor()
        global img
        canvas = Canvas(self.tk, width=1500, height=1500)
        scrollbar = Scrollbar(self.tk, orient=VERTICAL, command=canvas.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        canvas.configure(yscrollcommand=scrollbar.set)

        frame = Frame(canvas)
        canvas.create_window((0, 0), window=frame, anchor=NW)
        frame.bind("<Configure>", lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")))

        canvas.pack()
        mycursor.execute("SELECT * FROM livre")
        Headstr = [mycursor.column_names]
        Hrows = len(Headstr)
        Hcolumns = len(Headstr[0])
        lists = mycursor.fetchall()
        rows = len(lists)
        # columns = len(lists[0])

        for i in range(Hrows):
            for j in range(5):
                self.e = tk.Entry(frame, fg='brown', font=(
                    'Arial', 16, 'bold'), borderwidth=0, bg='#f2f2f2')
                self.e.grid(row=i, column=j)
                self.e.insert(END, Headstr[i][j])

        for i in range(rows):
            for j in range(4):
                b1 = tk.Label(frame, text=lists[i][j], fg='blue', font=(
                    'Arial', 16), borderwidth=0, bg='#f2f2f2')
                b1.grid(row=i+1, column=j)
                path = str(lists[i][4])
                img = ImageTk.PhotoImage(Image.open(
                    r"C:\Users\hp\Desktop\Projet\images/"+path))
                b2 = tk.Button(frame, image=img, height=100,
                               width=100, borderwidth=0, bg='#f2f2f2')
                b2.image_names = img
                b2.grid(row=i+1, column=4)

        b3 = tk.Button(frame, text="vers menu", command=self.menu1, background='#ed6663', font=(
            'Arial', 16), borderwidth=0, fg='white', activebackground='#ffa372', padx=10, pady=5)
        b3.grid(row=i+2, column=0, columnspan=5, pady=20)

    def convertTuple(self, tup):

        str = ''
        for item in tup:
            if (item != None):
                str = str + item
        return str


class Livre():
    def __init__(self, idlivre, Titre, datePublication, Auteur, image):
        self.idlivre = idlivre
        self.Titre = Titre
        self.datePublication = datePublication
        self.Auteur = Auteur
        self.image = image

    def newframe(self):
        if self.tk:
            self.tk.destroy()

        self.tk = Tk()
        self.tk.title("BIBLIO")
        self.tk.geometry("1000x500")
        img = Image.open("library.jpg")
        img = img.resize((1000, 500), Image.ANTIALIAS)

        self.bg_image = ImageTk.PhotoImage(img)
        bg_label = Label(self.tk, image=self.bg_image)
        bg_label.pack()

        frame = Frame(self.tk)
        frame.pack(pady=100)

        return frame

    def ajouterlivre(self):
        frame = self.newframe()

        Label(frame, text="idLivre:", font=("Arial", 14)).pack(pady=5)
        self.idLivre = Entry(frame, textvariable=StringVar, font=("Arial", 14))
        self.idLivre.pack(pady=5)

        Label(frame, text="Titre:", font=("Arial", 14)).pack(pady=5)
        self.Titre = Entry(frame, textvariable=StringVar, font=("Arial", 14))
        self.Titre.pack(pady=5)

        Label(frame, text="Auteur:", font=("Arial", 14)).pack(pady=5)
        self.Auteur = Entry(frame, textvariable=StringVar, font=("Arial", 14))
        self.Auteur.pack(pady=5)

        Label(frame, text="datePublication:", font=("Arial", 14)).pack(pady=5)
        self.datePublication = Entry(
            frame, textvariable=StringVar, font=("Arial", 14))
        self.datePublication.pack(pady=5)

        Label(frame, text="image:", font=("Arial", 14)).pack(pady=5)

        Button(frame, text="Upload Image", command=self.upload_file,
               font=("Arial", 14), bg="gray", fg="white").pack(pady=10)
        Button(frame, text="Ajouter", command=self.insertlivre, font=(
            "Arial", 14), bg="green", fg="white").pack(pady=10)
        Button(frame, text="Vers Menu", command=self.menu, font=(
            "Arial", 14), bg="red", fg="white").pack(pady=10)

    def upload_file(self):

        f_types = [('Png files', '.png'), ('Jpg Files', '.jpg')]
        filename = filedialog.askopenfile(mode="r", filetypes=f_types)
        print(filename.name)
        with Image.open(filename.name) as f:
            f.save(r"C:\Users\hp\Desktop\Projet\images" +
                   os.path.basename(filename.name))

        self.imagefile = os.path.basename(filename.name)

    def insertlivre(self):
        mycursor = db.cursor()
        mycursor.execute("INSERT INTO livre(idLivre,Titre,Auteur,datePublication,image,empruntpar) VALUES (%s,%s,%s,%s,%s,%s)",
                         (self.idLivre.get(), self.Titre.get(), self.Auteur.get(), self.datePublication.get(), self.imagefile, None))
        db.commit()

    def AfficherLivres(self):

        global img
        frame = self.newframe()

        canvas = Canvas(self.tk, width=1500, height=1500)
        scrollbar = Scrollbar(self.tk, orient=VERTICAL, command=canvas.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        canvas.configure(yscrollcommand=scrollbar.set)

        frame = Frame(canvas)
        canvas.create_window((0, 0), window=frame, anchor=NW)

        frame.bind("<Configure>", lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")))

        canvas.pack()
        mycursor = db.cursor()
        mycursor.execute("SELECT * FROM livre")
        lists = mycursor.fetchall()
        Headstr = [mycursor.column_names]
        Hrows = len(Headstr)
        Hcolumns = len(Headstr[0])

        rows = len(lists)
        columns = len(lists[0])

        for i in range(Hrows):
            for j in range(Hcolumns):
                self.e = Entry(frame, fg='brown', font=(
                    'Arial', 16, 'bold'), bg='white', width=15)
                self.e.grid(row=i, column=j, padx=5, pady=5)
                self.e.insert(END, Headstr[i][j])

        for i in range(rows):
            for j in range(4):
                b1 = tk.Label(frame, text=lists[i][j], fg='blue', font=(
                    'Arial', 16), bg='white', width=20)
                b1.grid(row=i+1, column=j, padx=5, pady=5)
                b1 = tk.Label(frame, text=lists[i][5], fg='blue', font=(
                    'Arial', 16), bg='white', width=20)
                b1.grid(row=i+1, column=5, padx=5, pady=5)

                # Display book cover
                path = str(lists[i][4])
                img = ImageTk.PhotoImage(Image.open(
                    r"C:\Users\hp\Desktop\Projet\images/"+path))
                b2 = tk.Button(frame, image=img, height=200,
                               width=200, bg='white')
                b2.image_names = img
                b2.grid(row=i+1, column=4, padx=5, pady=5)

        b3 = tk.Button(frame, text="Vers Menu",
                       command=self.menu, bg='red', fg='white')
        b3.grid(row=i+2, column=0, padx=5, pady=5)

    def menu(self):
        frame = self.newframe()
        Label(frame, text="Menu: ").pack()
        Button(frame, text="Afficher Les livres", command=self.AfficherLivres,
               height=3, width=20, bg='lightblue', fg='black').pack()
        Button(frame, text="Ajouter un livre", command=self.ajouterlivre,
               height=3, width=20, bg='lightgreen', fg='black').pack()
        Button(frame, text="chercher un livre", command=self.recherche,
               height=3, width=20, bg='orange', fg='black').pack()
        Button(frame, text="Supprimer un livre", command=self.Suppr,
               height=3, width=20, bg='red', fg='white').pack()

    def Suppr(self):
        frame = self.newframe()
        Label(frame, text="Saisir titre du livre à supprimer",
              font=("Helvetica", 16)).pack(pady=10)
        self.supp = Entry(frame, textvariable=StringVar,
                          font=("Helvetica", 14))
        self.supp.pack(pady=10)
        Button(frame, text="Supprimer", command=self.supprimer_livre, font=(
            "Helvetica", 16), bg='#0077CC', fg='white', width=15).pack(pady=10)
        Button(frame, text="Vers menu", command=self.menu, font=(
            "Helvetica", 16), bg='#ff0000', fg='white', width=15).pack(pady=10)

    def supprimer_livre(self):
        suppr = self.supp.get()
        mycursor = db.cursor()
        mycursor.execute("SELECT Titre FROM livre")
        titres = mycursor.fetchall()
        for t in titres:
            if (self.convertTuple(t) == suppr):
                mycursor = db.cursor()
                mycursor.execute(
                    "DELETE FROM livre WHERE (Titre='" + suppr + "')")
                db.commit()

                return messagebox.showinfo("Message", "Livre supprimer")

        return messagebox.showinfo("Erreur", "Livre introuvable")

    def recherche(self):
        frame = self.newframe()
        Label(frame, text="Saisir le titre du livre à rechercher:",
              font=("Arial", 18), fg="brown").pack()
        self.recher = Entry(frame, textvariable=StringVar,
                            font=("Arial", 16), bg="#F0F0F0")
        self.recher.pack(pady=10)
        b1 = Button(frame, text="Chercher", command=self.chercher_livre1, font=(
            "Arial", 16), bg="#4CAF50", fg="white")
        b1.pack(pady=10)
        Button(frame, text="Retour au menu", command=self.menu, font=(
            "Arial", 16), bg="#F44336", fg="white").pack(pady=10)

    def convertTuple(self, tup):

        str = ''
        for item in tup:
            str = str + item
        return str

    def chercher_livre1(self):
        global img
        r = self.recher.get()

        if r == "":
            messagebox.showinfo("Erreur", "La barre de recherche est vide555")
        else:
            mycursor = db.cursor()
            mycursor.execute("SELECT Titre FROM livre")
            titres = mycursor.fetchall()

            for t in titres:
                if self.convertTuple(t) == r:
                    frame = self.newframe()
                    mycursor.execute(
                        "SELECT * FROM livre WHERE Titre = '" + r + "'")
                    lists = mycursor.fetchall()
                    Headstr = [mycursor.column_names]
                    Hrows = len(Headstr)
                    Hcolumns = len(Headstr[0])
                    rows = len(lists)
                    columns = len(lists[0])

                    for i in range(Hrows):
                        for j in range(Hcolumns):
                            self.e = Entry(frame, fg='brown',
                                           font=('Arial', 16, 'bold'))
                            self.e.grid(row=i, column=j)
                            self.e.insert(END, Headstr[i][j])

                    for i in range(rows):
                        for j in range(4):
                            b1 = tk.Label(
                                frame, text=lists[i][j], fg='blue', font=('Arial', 16))
                            b1.grid(row=i+1, column=j)
                            b1 = tk.Label(frame, text=lists[i][5], fg='blue', font=(
                                'Arial', 16), bg='white', width=15)
                            b1.grid(row=i+1, column=5)
                            path = str(lists[i][4])
                            img = ImageTk.PhotoImage(Image.open(
                                r"C:\Users\hp\Desktop\Projet\images/"+path))
                            b2 = tk.Button(frame, image=img,
                                           height=100, width=100)
                            b2.image_names = img
                            b2.grid(row=i+1, column=4)

                        b3 = tk.Button(frame, text="vers menu",
                                       command=self.menu, background='red')
                        b3.grid(row=i+2, column=0)

                    return 1

            return messagebox.showerror("Erreur", "Le livre n'a pas été trouvé")


class Mainpage(personne, Livre):

    def __init__(self):
        self.tk = None
        frame = self.newframe()
        Label(frame, text="Welcome!").pack(pady=10)
        Button(frame, text="Login as User", command=self.loguser, font=(
            "Arial", 14), fg="white", bg="blue").pack(pady=10, padx=50)
        Button(frame, text="Login as Admin", command=self.logadmin, font=(
            "Arial", 14), fg="white", bg="red").pack(pady=10, padx=50)

    def loguser(self):
        frame = self.newframe()

        Label(frame, text="Username:", font=("Arial", 14)).pack(pady=(20, 5))
        self.user1 = Entry(frame, textvariable=StringVar, font=("Arial", 14))
        self.user1.pack(pady=5)

        Label(frame, text="Password:", font=("Arial", 14)).pack(pady=(20, 5))
        self.user_password = Entry(
            frame, textvariable=StringVar, font=("Arial", 14), show="*")
        self.user_password.pack(pady=5)

        Button(frame, text="Login", command=self.verifuser, font=(
            "Arial", 14), bg="blue", fg="white").pack(pady=(20, 5), padx=10, side="left")
        Button(frame, text="Register", command=self.register, font=(
            "Arial", 14), bg="green", fg="white").pack(pady=(20, 5), padx=10, side="left")
        Button(frame, text="Admin", command=self.logadmin, font=(
            "Arial", 14), bg="red", fg="white").pack(pady=(20, 5), padx=10, side="left")

    def verifuser(self):
        global g
        username = self.user1.get()
        user_password = self.user_password.get()
        mycursor = db.cursor()
        if (username == "" or user_password == ""):
            return messagebox.showinfo("error", "champ(s) vide(s)")

        mycursor.execute(
            f"SELECT * FROM bibliotheque.personne WHERE username='{username}' and password='{user_password}'")
        myresult = mycursor.fetchall()
        if len(myresult) > 0:
            messagebox.showinfo("NICE", "connexion etablie")
            self.menu1()
            g = username

        else:
            messagebox.showinfo("error", "user introuvable!!")

    def logadmin(self):
        frame = self.newframe()

        Label(frame, text="Admin Username:", font=("Arial", 16)).pack(pady=10)
        self.username = Entry(
            frame, textvariable=StringVar, font=("Arial", 16))
        self.username.pack()

        Label(frame, text="Admin Password:", font=("Arial", 16)).pack(pady=10)
        self.password = Entry(frame, textvariable=StringVar,
                              font=("Arial", 16), show="*")
        self.password.pack()

        Button(frame, text="Admin Login", font=("Arial", 16),
               command=self.verifadmin).pack(pady=10)
        Button(frame, text="Login as User", font=(
            "Arial", 16), command=self.loguser).pack()

    def verifadmin(self):
        admin_username = self.username.get()
        admin_password = self.password.get()
        mycursor = db.cursor()
        mycursor.execute(
            f"SELECT * FROM bibliotheque.user WHERE user='{admin_username}' and pass='{admin_password}'")
        myresult = mycursor.fetchall()
        if len(myresult) > 0:
            messagebox.showinfo("NICE", "connexion etablie!")
            self.menu()
        else:
            if (admin_username == "" or admin_password == ""):
                messagebox.showinfo("error", "champ(s) vide(s)")
            else:
                messagebox.showinfo("error", "username or password non valid")


Mainpage()
tk.mainloop()
