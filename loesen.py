#feld[x][y] initiiert mit -1 auf leeren feldern
import time
class Sudoku_loeser:
    def __init__(self,feld,block_groesse):
        self.feld = feld
        self.block_groesse = block_groesse
        self.x_groesse = len(feld)
        self.y_groesse = len(feld[0])
        print("anfang:\n")
        self.printfeld()

        self.leere_kaestchen = self.bestimme_leere_kaestchen()
        self.moeglichkeiten_liste_erstellen()
        [weiter,[neues_x,neues_y,neue_zahl]] = self.finde_und_fuelle_singularitaet()
        while(weiter):
            if not self.moeglichkeiten_liste_erstellen():
                break
            [weiter,[neues_x,neues_y,neue_zahl]] = self.finde_und_fuelle_singularitaet()
            print("verbleibende kästchen:",len(self.leere_kaestchen))
        print("fertig:\n")
        self.printfeld()


        

    def printfeld(self):
        for zeile in range(self.y_groesse):
            zeilenstring = ""
            for spalte in range(self.x_groesse):
                zeilenstring +=str(self.feld[spalte][zeile])+","
            print(zeilenstring[:-1])

    ######################################################################
    # mögliche Zahlen feststellen
    ######################################################################

    def bestimme_leere_kaestchen(self):
        leere_felder = []
        for x in range(self.x_groesse):
            for y in range(self.y_groesse):
                if self.feld[x][y] == 0:
                    leere_felder.append({"koordinaten":[x,y],"moeglichkeiten":[]})
        return leere_felder

    def zahlen_aus_zeile(self, zeile):
        zahlen = []
        for x in range(self.y_groesse):
            for y in range(self.x_groesse):
                if y == zeile:
                    zahlen.append(feld[x][y])
        return zahlen
    def zahlen_aus_spalte(self,spalte):
        zahlen = []
        for x in range(self.y_groesse):
            for y in range(self.x_groesse):
                if x == spalte:
                    zahlen.append(feld[x][y])
        return zahlen

    def zahlen_aus_block(self,x_ziel,y_ziel):
        blocknummer_x = int(x_ziel/self.block_groesse)
        blocknummer_y = int(y_ziel/self.block_groesse)
        block_start_x = blocknummer_x*self.block_groesse
        block_start_y = blocknummer_y*self.block_groesse
        zahlenmenge = []
        for x in range(block_start_x,block_start_x+self.block_groesse):
            for y in range(block_start_y,block_start_y+self.block_groesse):
                zahlenmenge.append(self.feld[x][y])
        return zahlenmenge

    def moegliche_zahlen(self,feld_koordinaten):
        moegliche_zahlen = (1,2,3,4,5,6,7,8,9)
        x = feld_koordinaten[0]
        y = feld_koordinaten[1]
        spalten_zahlen = self.zahlen_aus_spalte(x)
        zeilen_zahlen = self.zahlen_aus_zeile(y)
        block_zahlen = self.zahlen_aus_block(x,y)
        moegliche_zahlen = self.zahlen_rausschmeissen(moegliche_zahlen,spalten_zahlen)
        moegliche_zahlen = self.zahlen_rausschmeissen(moegliche_zahlen,zeilen_zahlen)
        moegliche_zahlen = self.zahlen_rausschmeissen(moegliche_zahlen,block_zahlen)
        return moegliche_zahlen

    def zahlen_rausschmeissen(self,moegliche_zahlen,schon_vorhandene_zahlen):
        arbeitskopie = list(moegliche_zahlen)
        for zahl in moegliche_zahlen:
            if zahl in schon_vorhandene_zahlen:
                arbeitskopie.remove(zahl)
        return arbeitskopie
    
    def moeglichkeiten_liste_erstellen(self):
        if(len(self.leere_kaestchen)<0):
            return False
        for kaestchen in self.leere_kaestchen:
            kaestchen["moeglichkeiten"] = self.moegliche_zahlen(kaestchen["koordinaten"])
        return True
    ######################################################################
    # Singularitätensuche
    ######################################################################
    def finde_und_fuelle_singularitaet(self):
        for spalte in range(self.x_groesse):
            #suche spaltensingularität
            leere_kaestchen = self.leere_kaestchen_aus_spalte(spalte)
            [index,zahl,gibt_singularitaet] = self.singularitaet_in_liste(leere_kaestchen)
            if gibt_singularitaet:
                [x,y] = leere_kaestchen[index]["koordinaten"]
                self.trage_zahl_ein(x,y,zahl)
                return [True,[x,y,zahl]]
        for zeile in range(self.y_groesse):
            #suche zeilensingularität
            leere_kaestchen = self.leere_kaestchen_aus_zeile(zeile)
            [index,zahl,gibt_singularitaet] = self.singularitaet_in_liste(leere_kaestchen)
            if gibt_singularitaet:
                [x,y] = leere_kaestchen[index]["koordinaten"]
                self.trage_zahl_ein(x,y,zahl)
                return [True,[x,y,zahl]]
        anzahl_bloecke_pro_zeile = int(self.x_groesse/self.block_groesse)#anzahl zeilenblöcke = anzahl spaltenblöcke 
        for block_x in range(anzahl_bloecke_pro_zeile):
            for block_y in range(anzahl_bloecke_pro_zeile):
                #suche blocksingularität
                leere_kaestchen = self.leere_kaestchen_aus_block(block_x,block_y)
                [index,zahl,gibt_singularitaet] = self.singularitaet_in_liste(leere_kaestchen)
                if gibt_singularitaet:
                    [x,y] = leere_kaestchen[index]["koordinaten"]
                    self.trage_zahl_ein(x,y,zahl)
                    return [True,[x,y,zahl]]
        return [False,[-1,-1,-1]]
    
    def singularitaet_in_liste(self,liste): # return wert: index in der liste, zahl die zu setzen ist, true wenn eine singularität gefunden wurde, false wenn nicht
        #entweder  nur eine möglichkeit in möglichkeitenliste
        for index in range(len(liste)):
            if(len(liste[index]["moeglichkeiten"])==1):
                return [index,liste[index]["moeglichkeiten"][0],True]
        #oder zahl nur einmal in menge(zeile, spalte, block)
        for zahl in range(1,10):
            [anzahl,index] = self.zaehle_moeglichkeiten(liste,zahl)
            if anzahl == 1:
                return [index, zahl, True] 
        #ansonsten keine singularitäten mehr vorhanden
        return [-1,-1,False]
                  
    def zaehle_moeglichkeiten(self,kaestchenliste,zahl):
        anzahl = 0
        ziel_index = -1
        for index in range(len(kaestchenliste)):
            if zahl in kaestchenliste[index]["moeglichkeiten"]:
                anzahl +=1
                if(anzahl == 1):
                    ziel_index = index
                elif anzahl > 0:
                    break
        return [anzahl, ziel_index]

    def leere_kaestchen_aus_spalte(self,spalte):
        liste = []
        for kaestchen in self.leere_kaestchen:
            if kaestchen["koordinaten"][0]==spalte:
                liste.append(kaestchen)
        return liste

    def leere_kaestchen_aus_zeile(self, zeile):
        liste = []
        for kaestchen in self.leere_kaestchen:
            if kaestchen["koordinaten"][1]==zeile:
                liste.append(kaestchen)
        return liste

    def koordinate_in_block(self,block_x,block_y,koordinate_x,koordinate_y):
        if( koordinate_x >= block_x*self.block_groesse 
        and koordinate_x < self.block_groesse*(block_x+1)
        and koordinate_y >=block_y* self.block_groesse
        and koordinate_y < self.block_groesse*(block_y+1)):
            return True
        else:
            return False

    def leere_kaestchen_aus_block(self,block_x,block_y):
        liste = []
        for kaestchen in self.leere_kaestchen:
            if self.koordinate_in_block(block_x,block_y,kaestchen["koordinaten"][0],kaestchen["koordinaten"][1]):
                liste.append(kaestchen)
        return liste

    def trage_zahl_ein(self,x,y,zahl):
        self.feld[x][y] = zahl
        for index in range(len(self.leere_kaestchen)):
            if self.leere_kaestchen[index]["koordinaten"]==[x,y]:
                self.leere_kaestchen.pop(index)
                break


if __name__ == '__main__':
    spalte1 = [0,7,0 ,0,9,3 ,0,0,5]
    spalte2 = [0,0,0 ,4,0,0 ,6,0,0]
    spalte3 = [0,2,0 ,0,0,7 ,0,0,8]
    spalte4 = [7,0,0 ,0,0,0 ,0,8,0]
    spalte5 = [1,0,9 ,0,0,0 ,0,7,0]
    spalte6 = [0,0,0 ,6,0,4 ,0,0,0]
    spalte7 = [5,0,1 ,0,0,0 ,0,0,0]
    spalte8 = [0,0,8 ,9,5,0 ,0,0,0]
    spalte9 = [0,0,0 ,0,0,0 ,2,0,3]
    feld = [spalte1,spalte2,spalte3,spalte4,spalte5,spalte6,spalte7,spalte8,spalte9]
    loeser = Sudoku_loeser(feld,3)
    