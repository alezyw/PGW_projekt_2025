# PGW_projekt_2025 - Interaktywna mapa gminy Jarocin wraz z podkładem statystyczno-historycznym
repozytorium zawiera dane projektu zaliczeniowego z przedmiotu "Programowanie geoserwisów webowych" z semestru letniego 2025.

## Spis
* [Autorzy](#autorzy)
* [Informacje o mapie, cel i idea stworzenia mapy](#informacje-o-mapie)
* [Dane (skąd pobrane dane, w jaki sposób przetworzone)](#dane)
* [Opis możliwości mapy oraz interfejsu użytkownika (np screen z opisem)](#opis-możliwości-mapy)
* [Struktura systemu w postaci graficznej wraz z opisem (warstwy, biblioteki, klasy wraz z powiązaniami)](#struktura-systemu)
* [Najważniejsze, najbardziej spektakularne fragmenty kodu wraz z opisem](#kod)

## Autorzy
- Aleksander Żywień
- Marcel Tomczak

## Informacje o mapie
Mapa interaktywna przedstawiająca zabytki i historyczny układ urbanistyczny gminy Jarocin, zagęszczenie zabudowy w formie siatki statystycznej 1 km², warstwy historyczne Messtischblatt. Możliwe zastosowania: planowanie tras turystycznych, analiza zmian przestrzennych, badanie struktury zabudowy.

## Dane
- Dane o drogach i budynkach zostały pobrane z BDOT10k z geoportal.gov.pl
- Granica miasta została pobrana z groportal.gov.pl
- Siatkę 1 km² i środki budynków utworzono na bazie warstwy budynków i granicy gminy poprzez podzielenie warstwy gminy na kwadrawy o bokach 1000m, następnie wyznaczenie centroidów budynków, na następnie zliczenie tych centroidów w utworzonych kwadratach.
- Historyczne mapy topograficzne - Messtischblatt

## Opis możliwości mapy
Tutaj pododawać screeny z numerkami
1. Interaktywna mapa
2. Przycisk odpowiadający za możliwość wyświetlania/chowania centroidów budynków
3. Lista z punktami oznaczającymi ciekawe miejsca, z możliwością włączenia/wyłączenia ich
4. Lista radiowa z możliwością nacisknięci, by przybliżyło nam widok w zaznaczone miejsce
5. Pola wyboru z możliwość wyświetlania wybranej ilości warstw na raz
6. Suwak czasowy z możliwością zmiany mapy podkładowej Messtischblatt
7. Interaktywny panel pokazujący numer kafelka i liczbę budynków znajdujących się na warstwie podział na siatkę kwadratów 1 km²
8. Suwak odpowiadający za tryb nocny
9. Kontrolki odpowiadające za przyliżenie, oddalanie i pełny ekran
10. Kontrolka odpowiadająca za lokalizacje na mapie
11. Kontrolka umożliwiająca rysowanie linii, poligonów i mierzenie odległości na mapie


# Struktura systemu
Dodać grafikę

Wykorzystane biblioteki:
os, dash_bootstrap_components, dash, dash_leaflet, dash_leaflet.express, dash.dependencies, dash_extensions.javascript

# Kod
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

```python
def pobierz_info(feature=None):
    header = [html.H4("Ilość budynków na km²")]
    if not feature:
        return header + [html.P("Najedź na kwadrat")]
    return header + [
        html.B(f"Kwadrat: {feature['properties'].get('id', '')}"), html.Br(),
        html.B(f"Liczba budynków: {feature['properties'].get('NUMPOINTS', 0)}")]
```
Ten fragment kodu dotyczy generowania treści okna informacyjnego wyświtelanego po najechaniu na kafelek. Jeśli funkcja zostanie wywołana bez parametru (feature=None) - zwraca komunikat "Najedź na kwadrat", lecz gdy użytkownik najedzie kursorem na kwadrat: feature['properties'] - dostęp do najechanego obiektu geograficznego, get('id', '') - pobieranie wartości id, a '' jeśli obiekt nie istnieje, dalej jest get('NUMPOINTS', 0) - tak samo, tylko dla liczby budynków, gdy nie ma informacji podaje 0

```python
dd_options = [dict(value=c["name"], label=c["name"]) for c in miejsca]
dd_defaults = [o["value"] for o in dd_options]
geojson = dlx.dicts_to_geojson([{**c, **dict(tooltip=c['name'], id=c['name'])} for c in miejsca])
geojson_filter = assign("function(feature, context){return context.hideout.includes(feature.properties.name);}")
```

W tym fragmencie najpier kod tworzy listę opcji dla komponentu dropdown, dla każdej pozycji w liście miejsca tworzy słownik z: value - wartość wewnętrzna i label - etykieta widoczna dla użytkownika. Następnie ustawia domyślnie zaznaczone wszystkie pozycje w dropdown i konwerstuje dane do formatu geojson. Na koniec tworzy funkcję filtrującą w JavaScript, gdzie context.hideout - wartości przekazane z dropdown, includes() - sprawdza czy nazwa miejsca jest na liście zaznaczonych, przez co finalnie pokazuje tylko zaznaczone miejsca.













