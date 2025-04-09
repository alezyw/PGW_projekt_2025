# PGW_projekt_2025 - Interaktywna mapa gminy Jarocin wraz z podkładem statystyczno-historycznym
repozytorium zawiera dane projektu zaliczeniowego z przedmiotu "Programowanie geoserwisów webowych" z semestru letniego 2025.

##Spis
*[Autorzy](#autorzy)
*[Informacje o mapie, cel i idea stworzenia mapy](#informacje_o_mapie)
*[Dane (skąd pobrane dane, w jaki sposób przetworzone)](#dane)
*[Opis możliwości mapy oraz interfejsu użytkownika (np screen z opisem)](#opis_możliwości_mapy)
*[Struktura systemu w postaci graficznej wraz z opisem (warstwy, biblioteki, klasy wraz z powiązaniami)](#struktura_systemu)
*[Najważniejsze, najbardziej spektakularne fragmenty kodu wraz z opisem](#kod)

##Autorzy
- Aleksander Żywień
- Marcel Tomczak

##Informacje o mapie
- Mapa interaktywna przedstawiająca informacje o zabytkach, pokdładzie historycznym i zagęszczeniu zabudowy w gminie Jarocin. Użytkownik może posłużyć się mapą do lokalizacji ciakawych miejsc, nauki historycznego układu gminy, badać układ zabudowy i planować wycieczki.

##Dane
- Dane o drogach i budynkach zostały pobrane z BDOT10k z geoportal.gov.pl
- Granica miasta została pobrana z groportal.gov.pl
- Siatkę 1 km² i środki budynków utworzono na bazie warstwy budynków i granicy gminy poprzez podzielenie warstwy gminy na kwadrawy o bokach 1000m, następnie wyznaczenie centroidów budynków, na następnie zliczenie tych centroidów w utworzonych kwadratach.
- Historyczne mapy topograficzne - Messtischblatt

##Opis możliwości mapy
Tutaj pododawać screeny z numerkami
- 1. Przycisk odpowiadający za możliwość wyświetlania/chowania centroidów budynków

#Struktura systemu


#Kod
```python
style_handle = assign("""function(feature, context){
    const {classes, skala_kolorow, style, colorProp} = context.hideout;
    const value = feature.properties[colorProp];
    for (let i = 0; i < classes.length; ++i) {
        if (value > classes[i]) {
            style.fillColor = skala_kolorow[i];
        }
    }
    return style;
}""")
```
Zaimplementowanie funkcji JavaScript do dynamicznego stylowania warstw GeoJSON na mapie. Jej funkcją jest przypisanie kolorów do poligonów na podstawie wartości liczbowych. Najpier pobiera dane z podanych wartości, a nastepnie funkcja iteruje przez wszystkie przedziały, następnie szuka ostatniego przedziału, który jest mniejszy niż wartość, a ostatecznie przypisuje odpowiedni kolor ze skali.



