
Kapitel aus der anderen Datei
=============================

Dieses Kapitel wurde als *diplomarbeit2.md* geschrieben und dann 
mit *pandoc* in \TeX\ umgewandelt.

```bash
pandoc --listings -s diplomarbeit2.md -o diplomarbeit2.tex 
```

Wie man sieht ist das ganz einfach, sogar Listings sind möglich. 
Und nun zu einem Bild. 

![Der Text steht unterhalb](HTL3RLogo.png)

Achtung: Pandoc skaliert die Bilder nicht! Hier hilft nur eine vorhergehende 
Skalierung des Bildes. Oder nachträgliches Editieren -- ganz einfach die passende 
Breite in der  *.tex* Datei ausbessern. 

Man kann auch die Breite aber auch durch La\TeX\ Befehle angeben -- das ändert aber 
die Standardbreite aller folgenden Bilder!

\setkeys{Gin}{width=0.6\textwidth,}

![Das kleinere Bild](HTL3RLogo.png)

\setkeys{Gin}{width=2cm}

![Das ganz kleine Bild](HTL3RLogo.png)

Auch Listen sind kein Problem, wichtig sind nur Leerzeilen zwischen den Listenpunkten. 
Hier sieht man eine einfache Aufzählung.

*  wichtig
*  auch ganz lange Texte können bei Listen
    geschrieben werden.
  
    Sogar mehrere Absätze sind möglich.

* Ende der Liste.

Welches Zeichen am Anfang der Liste steht ist dabei leicht einzustellen, im *pandoc* Manual gibt es nähere Infos:

1.  eins
2.  zwei

    i.  zwei eins -- Mindestens 4 Zeichen eingerückt
    i.  zwei zwei
   
1.  drei. *Pandoc* zählt richtig, das Zeichen am Anfang der Zeile ist nur ein Muster!

