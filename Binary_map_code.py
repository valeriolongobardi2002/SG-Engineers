raster1_path = "C:\\Users\\angel\\Desktop\\QGIS\\risized\\Termica_2.tif"
raster2_path = "C:\\Users\\angel\\Desktop\\QGIS\\risized\\Humidity.tif"
raster3_path = "C:\\Users\\angel\\Desktop\\QGIS\\risized\\Altitude_cut.tif"
raster4_path = "C:\\Users\\angel\\Desktop\\QGIS\\risized\\land_cut.tif"


raster1 = QgsRasterLayer(raster1_path, "TIR map")
raster2 = QgsRasterLayer(raster2_path, "Humidity")
raster3 = QgsRasterLayer(raster3_path, "Altitude")
raster4 = QgsRasterLayer(raster4_path, "Land")

if not raster2.isValid() or not raster3.isValid():
    print("Errore nel caricamento dei raster")
else:
    print("Tutti i raster caricati correttamente")
    #QgsProject.instance().addMapLayer(raster1)
    #QgsProject.instance().addMapLayer(raster2)
    #QgsProject.instance().addMapLayer(raster3)
    #QgsProject.instance().addMapLayer(raster4)


    soglia1 = 230#only green band, eliminate orange areas which are above 303.15K
    soglia2 = 0#only red band, eliminte red and ornage areas which don't have an accetable humidity'
    soglia3 = 180#only red band, eliminate yellow areas which are above 650 m

    entries = []

    raster1_entry = QgsRasterCalculatorEntry()
    raster1_entry.ref = 'raster1@1'
    raster1_entry.raster = raster1
    raster1_entry.bandNumber = 2
    entries.append(raster1_entry)

    raster2_entry = QgsRasterCalculatorEntry()
    raster2_entry.ref = 'raster2@1'
    raster2_entry.raster = raster2
    raster2_entry.bandNumber = 1
    entries.append(raster2_entry)

    raster3_entry = QgsRasterCalculatorEntry()
    raster3_entry.ref = 'raster3@1'
    raster3_entry.raster = raster3
    raster3_entry.bandNumber = 1
    entries.append(raster3_entry)

    formula = f"({raster1_entry.ref} > {soglia1}) AND ({raster2_entry.ref} = {soglia2}) AND ({raster3_entry.ref} < {soglia3})"
     
    output_raster_path = "C:\\Users\\angel\\Desktop\\QGIS\\risized\\Wine_map.tif"

    calc = QgsRasterCalculator(
        formula,
        output_raster_path,
        'GTiff',
        raster3.extent(),
        raster3.width(),
        raster3.height(),
        entries
    )

    calc.processCalculation()

    result_raster = QgsRasterLayer(output_raster_path, "Risultato Heatmap")

    if result_raster.isValid():
        QgsProject.instance().addMapLayer(result_raster)
        print("Nuovo raster creato e caricato correttamente!")
    else:
        print("Errore nel caricamento del nuovo raster!")
