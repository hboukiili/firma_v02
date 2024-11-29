from eralchemy import render_er

# Define the ERD in a text format compatible with eralchemy
uml_description = """
[users] {
    first_name: CharField
    last_name: CharField
    email: EmailField (PK)
    password: CharField
}

[Farmer|USERNAME_FIELD;REQUIRED_FIELDS]
[Searcher]
[PolicyMaker]

[Farmer] > [users]
[Searcher] > [users]
[PolicyMaker] > [users]

[Field] {
    id: AutoField (PK)
    user_id: ForeignKey -> Farmer.id
    name: CharField
    boundaries: PolygonField
}

[Crop] {
    id: AutoField (PK)
    Crop: CharField
    Crop_planting_date: DateField
    Tree: CharField
    Tree_planting_date: DateField
    field_id: ForeignKey -> Field.id
}

[Soil] {
    id: AutoField (PK)
    soil_input_method: CharField
    soil_type: CharField
    sand_percentage: IntegerField
    silt_percentage: IntegerField
    clay_percentage: IntegerField
    field_id: ForeignKey -> Field.id
}

[Soil_analysis] {
    id: AutoField (PK)
    soil_id: ForeignKey -> Soil.id
    PH_eau: FloatField
    EC_ms_cm: FloatField
    EC_ms_cm_pate_saturée: FloatField
    Argile: FloatField
    Limon: FloatField
    Sable: FloatField
    MO: FloatField
    Nt: FloatField
    P205: FloatField
    K20: FloatField
    Na20: FloatField
    Na: FloatField
    Cao: FloatField
    Ca: FloatField
    MGo: FloatField
    Mg: FloatField
    SAR: FloatField
    Cu: FloatField
    Mn: FloatField
    Fe: FloatField
    Zn: FloatField
    NNH4: FloatField
    NO3: FloatField
    CI: FloatField
    BORE: FloatField
    Caco3: FloatField
    Caco3_actif_AXB: FloatField
}

[Data_source] {
    id: AutoField (PK)
    datetime: DateField
    field_id: ForeignKey -> Field.id
}

[Station]
[Lidar]
[Drone]

[Station] > [Data_source]
[Lidar] > [Data_source]
[Drone] > [Data_source]

[Ogimet_stations] {
    id: AutoField (PK)
    station_id: IntegerField
    lat: CharField
    long: CharField
    location_name: CharField
}

[Irrigation_system] {
    id: AutoField (PK)
    irrigation_type: CharField
    instalation_date: DateField
    field_id: ForeignKey -> Field.id
}

[Irrigation_amount] {
    id: AutoField (PK)
    amount: IntegerField
    date: DateField
    irrigation_system_id: ForeignKey -> Irrigation_system.id
}

[Surface_irrigation]
[Sprinkler_irrigation]
[Drip_Irrigation]

[Surface_irrigation] > [Irrigation_system]
[Sprinkler_irrigation] > [Irrigation_system]
[Drip_Irrigation] > [Irrigation_system]

[Maitenance_dates] {
    id: AutoField (PK)
    date: DateField
    irrigation_system_id: ForeignKey -> Irrigation_system.id
}

[Sol_Fao_Parametre] {
    id: AutoField (PK)
    sol: CharField
    REW_min: FloatField
    REW_max: FloatField
    thetaFC_min: FloatField
    thetaFC_max: FloatField
    thetaWP_min: FloatField
    thetaWP_max: FloatField
}

[Fao_Crop_Parametre] {
    id: AutoField (PK)
    crop: CharField
    Kcbini: FloatField
    Kcbmid: FloatField
    Kcbend: FloatField
    Lini: FloatField
    Ldev: FloatField
    Lmid: FloatField
    Lend: FloatField
    Zrini: FloatField
    zrmax: FloatField
    pbase: FloatField
    Ze: FloatField
}

[fao_output] {
    id: AutoField (PK)
    field: ForeignKey -> Field.id
    date: DateField
    kcb: RasterField
    fc: RasterField
    DB: RasterField
    E: RasterField
    ETcadj: RasterField
    ETref: RasterField
    Irrig: RasterField
    Kcadj: RasterField
    Ks: RasterField
    Rain: RasterField
    Runoff: RasterField
    T: RasterField
    Zr: RasterField
}

[Sentinel2] {
    id: AutoField (PK)
    path: CharField
    date: DateField
}

[Weather_date] {
    id: AutoField (PK)
    Date: DateTimeField
    Field_id: ForeignKey -> Field.id
    T2m: FloatField
    Ws: FloatField
    Et0: FloatField
    Rain: FloatField
    Rh: FloatField
    D2m: FloatField
}

[forcast_Weather_date] {
    id: AutoField (PK)
    Date: DateTimeField
    Field_id: ForeignKey -> Field.id
    T2m: FloatField
    Ws: FloatField
    Et0: FloatField
    Rain: FloatField
    Rh: FloatField
    D2m: FloatField
}

[aquacrop_output] {
    id: AutoField (PK)
    date: DateField
    field_id: ForeignKey -> Field.id
    IrrDay: FloatField
    Tr: FloatField
    DeepPerc: FloatField
    Es: FloatField
    Th1: FloatField
    Th2: FloatField
    th3: FloatField
    gdd_cum: FloatField
    canopy_cover: FloatField
    biomass: FloatField
    z_root: FloatField
    DryYield: FloatField
    FreshYield: FloatField
    harvest_index: FloatField
    ET: FloatField
}
"""

# Generate the UML diagram as a PNG file
render_er(uml_description, "./FIRMA_database_uml.png")
