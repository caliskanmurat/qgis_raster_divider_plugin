# QGIS Raster Divider Plugin

This plugin allows user to divide raster into equal sized grids depend on desired size.The plugin consists of two section. In first section, footprints of output grids are generated. In second section, raster is splitted based on footprints file. Three types of output formats are available (GeoTiff, VRT, Numpy).
<br/><br/>

### 1-) Generate Footprints

<img width="800" src="./images/image_1.png">
<i>Generate Footprints</i> section is first part of the analysis. In this section a <i><b>Geopackage (GPKG)</b></i> file is created. This file contains informations about the tiles to be generated such as "<i>col_id, row_id, overlap_col, overlap_row, etc.</i>". Tiles that are not desired should be deleted from the attribute table of the GPKG file.
  
  
  
  <p>
    <img width="600" src="./images/image_2.png">
  </p>

<table style="border-collapse: collapse; border:1px solid red;" cellpadding="0" cellspacing="0" >
  <tr>
    <td rowspan="2"><img width="450" src="./images/image_4.png"></td>
    <td><img width="225" src="./images/image_6_1.png"></td>    
    <td><img width="225" src="./images/image_6_3.png"></td>
  </tr>
  <tr>
    <td><img width="225" src="./images/image_6_2.png"></td>
    <td><img width="225" src="./images/image_6_4.png"></td>
  </tr>
</table>

<br/>

<table style="border-collapse: collapse; border:1px solid red;" cellpadding="0" cellspacing="0" >
  <tr>
    <td rowspan="2"><img width="450" src="./images/image_5.png"></td>
    <td><img width="225" src="./images/image_7_1.png"></td>    
    <td><img width="225" src="./images/image_7_3.png"></td>
  </tr>
  <tr>
    <td><img width="225" src="./images/image_7_2.png"></td>
    <td><img width="225" src="./images/image_7_4.png"></td>
  </tr>
</table>

<table style="border-collapse: collapse; border:1px solid red;" cellpadding="0" cellspacing="0" >
  <tr>
    <td><img width="950" src="./images/overview.PNG"></td>
  </tr>  
</table>
