import dash_bootstrap_components as dbc
from dash import Dash, html, dcc, Output, Input
import dash_leaflet as dl
import dash_leaflet.express as dlx
from dash.dependencies import ClientsideFunction
from dash_extensions.javascript import assign

app = Dash(
    __name__,
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        dbc.icons.FONT_AWESOME],
    assets_folder='assets',
    suppress_callback_exceptions=True)

classes = [0, 20, 40, 60, 80, 100, 200, 300, 745]
skala_kolorow = ['#FFEDA0', '#FED976', '#FEB24C', '#FD8D3C', '#FC4E2A', '#E31A1C', '#BD0026', '#800026', '#830000']
style = dict(weight=2, opacity=1, color='white', dashArray='3', fillOpacity=0.7)

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

def pobierz_info(feature=None):
    header = [html.H4("Ilość budynków na km²")]
    if not feature:
        return header + [html.P("Najedź na kwadrat")]
    return header + [
        html.B(f"Kwadrat: {feature['properties'].get('id', '')}"), html.Br(),
        html.B(f"Liczba budynków: {feature['properties'].get('NUMPOINTS', 0)}")]

miejsca = [dict(name="Aquapark", lat=51.978597, lon=17.509994),
          dict(name="Staw", lat=51.974335, lon=17.503632),
          dict(name="Centrum", lat=51.969285, lon=17.501506)]

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

info = html.Div(
    children=pobierz_info(),
    id="info",
    className="info-box",
    style={
        "position": "absolute",
        "top": "10px",
        "right": "10px",
        "zIndex": "1000",
        "background": "white",
        "padding": "10px",
        "borderRadius": "5px",
        "boxShadow": "0 2px 5px rgba(0,0,0,0.2)"
    })

app.layout = html.Div(className="wrapper", children=[
    dbc.Row(
        dbc.Col(
            html.Div([
                html.Div("Mapa Jarocin", className="header-title"),
                color_mode_switch
            ], className="header-container"),
            width=12
        )
    ),
    
    dbc.Row([
        dbc.Col(
            html.Div(
                "Strona przedstawiająca mapę internetową miasta Jarocin...",
                className="description"
            ),
            width=2,
            style={"order": 1}
        ),
        
        dbc.Col(
            dl.Map(
                id="mapa",
                children=[
                    dl.LayersControl(
                        position="bottomleft",
                        children=[
                            dl.BaseLayer(
                                dl.TileLayer(),
                                name="OpenStreetMap",
                                checked=True),
                            dl.FullScreenControl(),
                            dl.GestureHandling(),
                            dl.LocateControl(locateOptions={'enableHighAccuracy': True}),
                            dl.MeasureControl(position="topleft", primaryLengthUnit="kilometers", primaryAreaUnit="hectares", activeColor="#214097", completedColor="#972158"),
                            dl.ScaleControl(position="bottomleft"),
                            dl.BaseLayer(
                                dl.TileLayer(
                                    url="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
                                    attribution="Esri"),
                                name="Satelita",
                                checked=False),
                            dl.Overlay(
                                dl.LayerGroup([
                                    dl.GeoJSON(
                                        data=geojson,
                                        filter=geojson_filter,
                                        hideout=dd_defaults,
                                        id="markery",
                                        cluster=True),
                                    dl.GeoJSON(
                                        id="geojson-layer",
                                        url=None,
                                        style=style_handle,
                                        zoomToBounds=True,
                                        zoomToBoundsOnClick=True,
                                        hoverStyle=dict(weight=5, color='#666', dashArray=''),
                                        hideout=dict(
                                            skala_kolorow=skala_kolorow,
                                            classes=classes,
                                            style=style,
                                            colorProp="NUMPOINTS")
                                        ),
                                    dl.LayerGroup(id="dynamic-layers")
                                ]),
                                name="Warstwy dodatkowe",
                                checked=True)
                        ]
                    ),
                    info
                ],
                
                center=poczatkowe_centrum,
                zoom=12,
                className="map-container",
                style={'height': '70vh', 'position': 'relative'}
                
            ),
            
            width=6,
            style={"order": 2, "marginLeft": "auto"}
            ),
        
        dbc.Col([
            html.Div([
                html.H5("Warstwy"),
                dcc.Checklist(
                    options=[
                        {"label": "Granica", "value": "granice"},
                        {"label": "Podział na siatkę kwadratów 1 km²", "value": "kwadraty"},
                        {"label": "Drogi", "value": "drogi"},
                        {"label": "Obiekty wodne", "value": "woda"},
                        {"label": "Cieki", "value": "cieki"}],
                    value=[],
                    id="warstwy-checklist",
                    className="checkbox-group"
                )
            ]),
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
                    placeholder="Wybierz miejsca"
                    )
            ]),
            
            html.Hr(),
            html.Div([
                dcc.RadioItems(
                    id='miasto-wybor',
                    options=[
                        {'label': 'Aquapark', 'value': 'Aquapark'},
                        {'label': 'Staw', 'value': 'Staw'},
                        {'label': 'Centrum', 'value': 'Centrum'},
                        {'label': 'Powrót', 'value': 'Powrot'},
                    ],
                    value='Powrot',
                    className="radio-group")
            ])
        ], width=3, style={"order": 3, "marginLeft": "20px"})
    ], className="main-content"),
    
    html.Footer(
        dbc.Row(
            dbc.Col(
                html.Div("Marcel Tomczak 3 GI", className="footer-content")
                )
        ),
        className="footer"
    )
])

@app.callback(
    Output("geojson-layer", "url"),
    Input("warstwy-checklist", "value")
    )

def update_kwadraty(selected_layers):
    return "/assets/dane/poligony1000.geojson" if "kwadraty" in selected_layers else None

@app.callback(
    Output("info", "children"), 
    Input("geojson-layer", "hoverData")
    )
def info_hover(feature):
    return pobierz_info(feature)

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
        "woda": dl.GeoJSON(url="/assets/dane/water_a.geojson"),
        "cieki": dl.GeoJSON(url="/assets/dane/waterways.geojson")
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
    if selected_location == "Aquapark":
        return {"center": [51.978597, 17.509994], "zoom": 20}
    elif selected_location == "Staw":
        return {"center": [51.974335, 17.503632], "zoom": 20}
    elif selected_location == "Centrum":
        return {"center": [51.969285, 17.501506], "zoom": 16}
    return {"center": poczatkowe_centrum, "zoom": 12}

if __name__ == '__main__':
    app.run(debug=True)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    