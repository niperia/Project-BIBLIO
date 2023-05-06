# Project-BIBLIO
Gestion de bibliotheque Projet

on a cree une class 'Mainpage' qui herite de la classe livre la classe personne

dans "MAINPAGE" on a cree des fonction d authentification et de verificaton des donnees entree par la personne et l admin aussi (dans la frame 'admin')



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
        
Cette fonction permet de creer une nouvelle frame et détruit frame existante

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

cette focntion permet de vérifier 3 cas :
cas 1:
  si la barre le recherche est vide un message sera afficher comme quoi la barre de recherche est vide 
cas 2:
  si l'utilisateur a saisit un un titre d'un livre qui est déja emprunté avec un message qui sera afficher
cas 3:
  si le livre existe alors l'utilisateur a le choix de l'emprunter; en appuiant sur le button (Emprunter un livre) l'utilisateur sera dérigé vers une autre frame où il peux sasir la date et il aura un autre button (Emprunter un livre) et les données seront saisies dans la base de données 
cas 3:
  si l'utilisateur a sasit un titre d'un livre qui n'existe pas avec un message 
  

def upload_file(self):

        f_types = [('Png files', '.png'), ('Jpg Files', '.jpg')]
        filename = filedialog.askopenfile(mode="r", filetypes=f_types)
        print(filename.name)
        with Image.open(filename.name) as f:
            f.save(r"C:\Users\hp\Desktop\Projet\images" +
                   os.path.basename(filename.name))

        self.imagefile = os.path.basename(filename.name)
        
cette focntion permet à l'utlisateur de télécharger une image et stocker le path du image dans une variable qui sera par la suite stocker dans notre base de donées



  
