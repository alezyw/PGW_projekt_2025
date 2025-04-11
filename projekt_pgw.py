import os
import dash_bootstrap_components as dbc
from dash import Dash, html, dcc, Output, Input
import dash_leaflet as dl
import dash_leaflet.express as dlx
from dash.dependencies import ClientsideFunction
from dash_extensions.javascript import assign

'''
to-do list: 
 - naprawić suwak i umiejscowienia
 - rozkmina czy zostawić podkład OSM wbudowany czy w suwaku
 '''


#--------!1!! WAŻNE !!!!---------------
# POTRZEBNE DO ŁADOWANIA PSUEDO-KAFELKÓW
# script_path = os.path.abspath('__file__') #jeżeli bezpośrednio w intepreterze
script_path = os.getcwd() # dla IDE
# -----------------------------------

# granice zdjęć (kafelków)
img_bounds = [
    [[51.9, 17.5], [51.8, 17.666]], # dobrzyca
    [[52.0, 17.333], [51.9, 17.5]], # góra
    [[52.0, 17.5], [51.9, 17.666]], # jarocin
    [[51.9, 17.333], [51.8, 17.5]], # kożmin wlkp.
    [[52.1, 17.333], [52.0, 17.5]], # nmnw
    [[52.1, 17.5], [52.0, 17.666]] # żerków
    ]
 
app = Dash(
    __name__,
    external_stylesheets=[
        dbc.themes.SANDSTONE,
        dbc.icons.FONT_AWESOME],
    assets_folder='assets',
    suppress_callback_exceptions=True)

classes = [0, 20, 40, 60, 80, 100, 200, 300, 745]
skala_kolorow = ['#FFEDA0', '#FED976', '#FEB24C', '#FD8D3C', '#FC4E2A', '#E31A1C', '#BD0026', '#800026', '#830000']
style = dict(weight=2, opacity=1, color='white', dashArray='3', fillOpacity=1)

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


miejsca = [dict(name="Glan", lat=51.972963, lon=17.504089),
          dict(name="Pałac Radoliński", lat=51.975617, lon=17.503320),
          dict(name="Staw", lat=51.974335, lon=17.503632),
          dict(name="Ruiny Kościoła Św Ducha", lat=51.974473, lon=17.506106),
          dict(name="Amfiteatr", lat=51.974650, lon=17.505374),
          dict(name="Stadion Miejski", lat=51.979215, lon=17.509113),
          dict(name="Wieża Ciśnień", lat=51.976196, lon=17.512431),
          dict(name="Historyczny Samolot MIG-15", lat=51.977755, lon=17.507902),
          dict(name="Spichlerz", lat=51.973855, lon=17.500544),
          dict(name="Kolejowa Wieża Ciśnień", lat=51.966721, lon=17.495384),
          dict(name="JOK (Jarociński Ośrodek Kultury", lat=51.968079, lon=17.499246),
          dict(name="Kamienie Księcia Radolnia", lat=51.969103, lon=17.471578),
          dict(name="Kościół Św Marcina", lat=51.973273, lon=17.501745),
          dict(name="Kościół Rzymskokatolicki Pw. Sw. Jerzego", lat=51.971360, lon=17.501362),
          dict(name="Kościół Pw. Chrystusa Króla", lat=51.970422, lon=17.499082),
          dict(name="Dworzec Kolejowy Jarocin", lat=51.968938, lon=17.494745),
          dict(name="Dwór z przeł. XVIII-XIX wieku", lat=51.963916, lon=17.453284),
          dict(name="Muzeum Napoleońskie", lat=51.942701, lon=17.562387),
          dict(name="Ruiny Pałacu Opalińskich", lat=52.027901, lon=17.510430),
          dict(name="Ratusz", lat=51.972357, lon=17.501538)]

dd_options = [dict(value=c["name"], label=c["name"]) for c in miejsca]
dd_defaults = [o["value"] for o in dd_options]
geojson = dlx.dicts_to_geojson([{**c, **dict(tooltip=c['name'], id=c['name'])} for c in miejsca])
geojson_filter = assign("function(feature, context){return context.hideout.includes(feature.properties.name);}")

poczatkowe_centrum = [51.969285, 17.501506]

color_mode_switch = html.Div(
    [
        dbc.Label(className="fas fa-moon", html_for="switch"),
        dbc.Switch(id="switch", value=True, className="d-inline-block mx-1", persistence=True),
        dbc.Label(className="fas fa-sun", html_for="switch"),
    ],
    className="theme-switcher",
    style={"position": "absolute", "right": "20px", "top": "20px", "zIndex": 1001})

app.layout = html.Div(className="wrapper", children=[
    dbc.Row(
        dbc.Col(
            html.Div([
                html.Div("Mapa Jarocin", className="header-title"),
                color_mode_switch
            ], className="header-container"),
            width=12,
        )
    ),
    
    dbc.Row([
        dbc.Col(
            html.Div([
                html.H5("Warstwy"),
                dcc.Checklist(
                    options=[
                        {"label": "Granica", "value": "granice"},
                        {"label": "Drogi", "value": "drogi"},
                        {"label": "Budynki", "value": "budynki"}],
                    value=[],
                    id="warstwy-checklist",
                    className="checkbox-group"
                )
            ]),
            width=2,
            style={"order": 1}
        ),
        
        dbc.Col(
            html.Div([
                dl.Map([
                    dl.TileLayer(),
                    dl.FullScreenControl(),
                    dl.GestureHandling(),
                    dl.LocateControl(locateOptions={'enableHighaccuracy': True}),
                    dl.MeasureControl(position="topleft", primaryLengthUnit="kilometers", primaryAreaUnit="hectares"),
                    dl.ScaleControl(position="bottomleft"),
                    dl.LayerGroup([
                        dl.GeoJSON(
                            data=geojson,
                            filter=geojson_filter,
                            hideout=dd_defaults,
                            id="markery",
                            cluster=True),
                        dl.GeoJSON(
                            id="geojson-layer",
                            style=style_handle,
                            hideout=dict(
                                skala_kolorow=skala_kolorow,
                                classes=classes,
                                style=style,
                                colorProp="NUMPOINTS")),
                        dl.LayerGroup(id="dynamic-layers"),
                        dl.LayerGroup(id="historical-layers")
                    ]),
                ],
                center=poczatkowe_centrum,
                zoom=13,
                id='mapa',
                className="map-container",
                style={'height': '60vh'}),
                
                html.Div(
                    dcc.Slider(
                        1889, 2024,
                        step=None,
                        marks={
                            1889: '1889',
                            1911: '1911', 
                            1940: '1940'
                            },
                        value=1889,
                        id='year-selector'
                    ),
                    style={"padding": "20px", "backgroundColor": "white", "borderRadius": "10px"}
                )
            ]),
            width=6,
            style={"order": 2}
        ),
        
        
        dbc.Col([
            html.Hr(),
            html.Div([
                dbc.Button(
                    [html.I(className="fas fa-building me-2"), "Środki budynków"],
                    id="btn-budynki",
                    color="primary",
                    className="w-100",
                    n_clicks=0)
            ]),
            html.Hr(),
            html.Div([
                dcc.Dropdown(
                    id="dd-miejsca",
                    options=dd_options,
                    value=dd_defaults,
                    multi=True,
                    clearable=False,
                    placeholder="Wybierz miejsca",
                    className="dropdown-group"
                    )
            ]),
            
            html.Hr(),
            html.Div([
                dcc.RadioItems(
                    id='miasto-wybor',
                    options=[
                        {'label': 'Powrót', 'value': 'Powrot'},
                        {'label': 'Glan', 'value': 'Glan'},
                        {'label': 'Pałac Radoliński', 'value': 'Rado'},
                        {'label': 'Ruiny Kościoła Św Ducha', 'value': 'Ruiny_K'},
                        {'label': 'Amfiteatr', 'value': 'Amfiteatr'},
                        {'label': 'Stadion Miejski', 'value': 'Stadion'},
                        {'label': 'Wieża Ciśnień', 'value': 'Wieza_C'},
                        {'label': 'Historyczny Samolot MIG-15', 'value': 'Samolot'},
                        {'label': 'Spichlerz', 'value': 'Spichlerz'},
                        {'label': 'Kolejowa Wieża Ciśnień', 'value': 'Wieza_C_K'},
                        {'label': 'JOK (Jarociński Ośrodek Kultury)', 'value': 'JOK'},
                        {'label': 'Kamienie Księcia Radolnia', 'value': 'Kamienie'},
                        {'label': 'Kościół Św Marcina', 'value': 'K1'},
                        {'label': 'Kościół Rzymskokatolicki Pw. Sw. Jerzego', 'value': 'K2'},
                        {'label': 'Kościół Pw. Chrystusa Króla', 'value': 'K3'},
                        {'label': 'Dworzec Kolejowy Jarocin', 'value': 'Dworzec'},
                        {'label': 'Dwór z przeł. XVIII-XIX wieku', 'value': 'Dwor'},
                        {'label': 'Muzeum Napoleońskie', 'value': 'Muzeum'},
                        {'label': 'Ruiny Pałacu Opalińskich', 'value': 'Ruiny_Palacu'},
                        {'label': 'Staw', 'value': 'Staw'},
                        {'label': 'Ratusz', 'value': 'Ratusz'},
                    ],
                    value='Powrot',
                    className="radio-group")
            ])
        ], width=3, style={"order": 3, "marginLeft": "20px"})
    ], className="main-content"),
    
    html.Footer(
        dbc.Row(
            dbc.Col(
                html.Div("Marcel Tomczak & Aleksander Żywień III GINF DI", className="footer-content")
                )
        ),
        className="footer"
    )
])

# callback jest uruchamiany po każdej zmianie paska
@app.callback(
    Output('historical-layers', 'children'),
    Input('year-selector', 'value')
    )

def ChooseYear(value):
    # ładuje psuedo-kafelki dla wybranego roku
    png_scan = [os.path.join('assets','skany',str(value),p) for p in 
                os.listdir(os.path.join('assets','skany',str(value)))]
    png_scan.sort() # sortuje alfabetycznie w celu lepszego zarządzania
    # lista składana tworząca obiekty dla nich
    overlay = *[dl.ImageOverlay(opacity=1, url=p, bounds=img_bounds[e])
     for e,p in enumerate(png_scan)],
    return overlay

@app.callback(
    [Output("dynamic-layers", "children"),
     Output("btn-budynki", "color"),
     Output("btn-budynki", "children")],
    [Input("warstwy-checklist", "value"),
     Input("btn-budynki", "n_clicks")]
    )

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

app.clientside_callback(
    ClientsideFunction(
        namespace='clientside',
        function_name='switchTheme'
    ),
    Output("switch", "id"),
    Input("switch", "value"),
    )

app.clientside_callback(
    """function(x){return x || [];}""",
    Output("markery", "hideout"),
    Input("dd-miejsca", "value")
    )

@app.callback(
    Output("mapa", "viewport"),
    Input("miasto-wybor", "value")
    )

def update_map_center(selected_location):
    if selected_location == "Glan":
        return {"center": [51.972963, 17.504089], "zoom": 20}
    elif selected_location == "Rado":
        return {"center": [51.975617, 17.503320], "zoom": 20}
    elif selected_location == "Ruiny_K":
        return {"center": [51.974473, 17.506106], "zoom": 20}
    elif selected_location == "Amfiteatr":
        return {"center": [51.974650, 17.505374], "zoom": 20}
    elif selected_location == "Stadion":
        return {"center": [51.979215, 17.509113], "zoom": 20}
    elif selected_location == "Wieza_C":
        return {"center": [51.976196, 17.512431], "zoom": 20}
    elif selected_location == "Samolot":
        return {"center": [51.977755, 17.507902], "zoom": 20}
    elif selected_location == "Spichlerz":
        return {"center": [51.973855, 17.500544], "zoom": 20}
    elif selected_location == "Wieza_C_K":
        return {"center": [51.966721, 17.495384], "zoom": 20}
    elif selected_location == "JOK":
        return {"center": [51.968079, 17.499246], "zoom": 20}
    elif selected_location == "Kamienie":
        return {"center": [51.969103, 17.471578], "zoom": 20}
    elif selected_location == "K1":
        return {"center": [51.973273, 17.501745], "zoom": 20}
    elif selected_location == "K2":
        return {"center": [51.971360, 17.501362], "zoom": 20}
    elif selected_location == "K3":
        return {"center": [51.970422, 17.499082], "zoom": 20}
    elif selected_location == "Dworzec":
        return {"center": [51.968938, 17.494745], "zoom": 20}
    elif selected_location == "Dwor":
        return {"center": [51.963916, 17.453284], "zoom": 20}
    elif selected_location == "Muzeum":
        return {"center": [51.942701, 17.562387], "zoom": 20}
    elif selected_location == "Ruiny_Palacu":
        return {"center": [52.027901, 17.510430], "zoom": 20}
    elif selected_location == "Staw":
        return {"center": [51.974335, 17.503632], "zoom": 20}
    elif selected_location == "Ratusz":
        return {"center": [51.972357, 17.501538], "zoom": 20}
    return {"center": poczatkowe_centrum, "zoom": 12}

if __name__ == '__main__':
    app.run(debug=True)
    
    
    

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    