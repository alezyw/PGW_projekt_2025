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
Mapa interaktywna przedstawiająca zabytki i historyczny układ urbanistyczny gminy Jarocin z warstwami historyczymi Messtischblatt. Możliwe zastosowania: planowanie tras turystycznych, analiza zmian przestrzennych, porównywnanie stanu zabudowy.

## Dane
- Dane o drogach i budynkach zostały pobrane z BDOT10k z geoportal.gov.pl
- Granica miasta została pobrana z groportal.gov.pl
- Środki budynków utworzono na bazie centroidów z warstwy budynków
- Historyczne mapy topograficzne - Messtischblatt

## Opis możliwości mapy
Tutaj pododawać screeny z numerkami
1. Interaktywna mapa
2. Przycisk odpowiadający za możliwość wyświetlania/chowania centroidów budynków
3. Lista z punktami oznaczającymi ciekawe miejsca, z możliwością włączenia/wyłączenia ich
4. Lista radiowa z możliwością wyboru miejsca, do którego widok zostanie przybliżony.
5. Pola wyboru z możliwość wyświetlania wybranej ilości warstw na raz
6. Suwak czasowy z możliwością zmiany mapy podkładowej Messtischblatt
7. Suwak odpowiadający za tryb nocny
8. Kontrolki odpowiadające za przyliżenie, oddalanie i pełny ekran
11. Kontrolka odpowiadająca za lokalizacje na mapie
12. Kontrolka umożliwiająca rysowanie linii, poligonów i mierzenie odległości na mapie


# Struktura systemu
Dodać grafikę

Wykorzystane biblioteki:
os, dash_bootstrap_components, dash, dash_leaflet, dash_leaflet.express, dash.dependencies, dash_extensions.javascript

# Kod

```python
dd_options = [dict(value=c["name"], label=c["name"]) for c in miejsca]
dd_defaults = [o["value"] for o in dd_options]
geojson = dlx.dicts_to_geojson([{**c, **dict(tooltip=c['name'], id=c['name'])} for c in miejsca])
geojson_filter = assign("function(feature, context){return context.hideout.includes(feature.properties.name);}")
```

W tym fragmencie najpier kod tworzy listę opcji dla komponentu dropdown, dla każdej pozycji w liście miejsca tworzy słownik z: value - wartość wewnętrzna i label - etykieta widoczna dla użytkownika. Następnie ustawia domyślnie zaznaczone wszystkie pozycje w dropdown i konwerstuje dane do formatu geojson. Na koniec tworzy funkcję filtrującą w JavaScript, gdzie context.hideout - wartości przekazane z dropdown, includes() - sprawdza czy nazwa miejsca jest na liście zaznaczonych, przez co finalnie pokazuje tylko zaznaczone miejsca.


```python
def toggle_layers(selected_layers, n_clicks):
    layer_mapping = {
        "granice": dl.GeoJSON(url="/assets/dane/granice.geojson"),
        "drogi": dl.GeoJSON(url="/assets/dane/roads.geojson"),
        "budynki": dl.GeoJSON(url="/assets/dane/budynki.geojson")
        }
    
    layers = [layer_mapping[layer] for layer in selected_layers if layer in layer_mapping]
    
    btn_color = "primary"
    btn_content = [html.I(), "Środki budynków"]
    
    if n_clicks % 2 == 1:
        layers.append(dl.GeoJSON(
            url="/assets/dane/budynki_cent.geojson",
            cluster=True,
            zoomToBoundsOnClick=True,
            superClusterOptions={"radius": 100}
        ))
        btn_color = "success"
        btn_content = [html.I(), "Ukryj budynki"]
    
    return layers, btn_color, btn_content
```

Ta funkcja jest callbackiem zarządzający warstwami mapy i stanem przycisku. Parametrami wejściowymi są: selected_layers - lista zaznaczonych warstw z checklisty i n_clicks - liczba kliknięć przycisku. Najpier w layer_mapping tworzy jest słownik przypisujący klucze warstw do komponentów GeoJSON. Następnie przechodzimy do filtrowania aktywnych warstw, kod dodaje tylko te warstwy, które zostały zaznaczone przez użytkownika w selected_layers oraz istnieją w layer_mapping. Następnie określana jest domyślna zawartość i kolor przysiku. Za if ustalona jest logika przełączania warstwy, gdzie pierwsze kliknięcie dodaje warstwę z centroidami budynków i zmienia kolor na zielony, a drugie kliknięcie usuwa warstwę, przywraca pierwotny stan, z kolei kolejne kliknięcia kontynuują przełączanie.








