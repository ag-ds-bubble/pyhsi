USGS EARTH OBSERVING-1 (EO-1)
HYPERION          

TABLE OF CONTENTS

INTRODUCTION
FORMAT FOR LEVEL 0, LEVEL 1R AND LEVEL 1GST (HDF)
FORMAT FOR LEVEL 1GST and LEVEL 1T (GEOTIFF)
ORGANIZATION FOR LEVEL 0 AND LEVEL 1R (HDF)
ORGANIZATION FOR LEVEL 1GST (HDF)
ORGANIZATION FOR LEVEL 1GST (GEOTIFF)
ORGANIZATION FOR LEVEL 1T (GEOTIFF)
DATA FILE NAMES
README
READING DATA
GENERAL INFORMATION AND DOCUMENTATION
CUSTOMER SUPPORT
DISCLAIMER


INTRODUCTION

This product was created by the United States Geological Survey (USGS) and  
contains EO-1 Hyperion data files in Hierarchical Data Format (HDF) or 
Geographic Tagged Image-File Format (GeoTIFF). EO-1 was launched as a 
one-year technology demonstration/validation mission. After the initial 
technology mission was completed, National Aeronautics and Space 
Administration (NASA) and the USGS agreed to the continuation of the 
EO-1 program as an extended mission. Information about the EO-1 satellite 
and the Hyperion sensor are available at the USGS and NASA web sites:
http://eo1.usgs.gov 
http://eo1.gsfc.nasa.gov


FORMAT FOR LEVEL 0, LEVEL 1R AND LEVEL 1GST (HDF)

The Hyperion data are provided in standard HDF Version 4.1 (release 5), 
written as band-interleaved-by-line (BIL) files stored in 16-bit signed 
integer radiance values. 

For more information on HDF structures, visit the HDF home page at:
http://www.hdfgroup.org


FORMAT FOR LEVEL 1GST AND LEVEL 1T (GEOTIFF)

The Hyperion data are provided in GeoTIFF format, written as band 
sequential (BSQ) files stored in 16-bit signed integer radiance values. 
GeoTIFF defines a set of publically available TIFF tags that describe 
cartographic and geodetic information associated with TIFF images. 
GeoTIFF is a format that enables referencing a raster image to a known 
geodetic model or map projection. By using the GeoTIFF format, both 
metadata and image data can be encoded into the same file.  
For more information on GeoTIFF, visit:
http://trac.osgeo.org/geotiff


ORGANIZATION FOR LEVEL 0 AND LEVEL 1R (HDF)

The Hyperion data product consists of a metadata file (.MET), a 
Federal Geographic Data Committee (FGDC) metadata file (.fgdc), 
a HDF datasets file (.L1R) and multiple auxiliary files.  The HDF 
auxiliary datasets file (.AUX) contains the data layers for spectral 
center wavelengths, spectral bandwidths, gain coefficients and the flag mask. 
Please note the product corner fields within the metadata files reflect 
the corners of the product including the presence of fill or background area. 


ORGANIZATION FOR LEVEL 1GST (HDF)

The Hyperion product includes a metadata file (_MTL.L1GST), a HDF 
header file (_HDF.L1GST), a Federal Geographic Data Committee (FGDC) 
metadata file (.fgdc) and multiple image bands (_B###.L1GST).


ORGANIZATION FOR LEVEL 1GST (GEOTIFF)

The Hyperion product includes a metadata file (_MTL_L1GST.TIF), a 
FGDC metadata file (.fgdc) and multiple image bands (_B###_L1GST.TIF).  
Please note the product corner fields within the metadata files reflect 
the corners of the product including the presence of fill or background area.  
The image corner fields within the metadata files reflect the corners of 
the image area.


ORGANIZATION FOR LEVEL 1T (GEOTIFF)

The Hyperion product includes a metadata file (_MTL_L1T.TIF) 
and multiple image bands (_B###_L1GST.TIF).  Please note the product corner 
fields within the metadata files reflect the corners of the product 
including the presence of fill or background area.  The image corner fields 
within the metadata files reflect the corners of the image area. 

For more information on the Hyperion product content, visit the 
Product Description Chapter of the User Guide found on the EO-1 website at: 
http://eo1.usgs.gov/documents


DATA FILE NAMES

The file naming convention is as follows:

EO1SPPPRRRYYYYDDDXXXML_GGG_VV  where:
  EO1 = Satellite
  S = Sensor (H=Hyperion, A=ALI)
  PPP = Target WRS Path
  RRR = Target WRS Row
  YYYY = Year of acquisition
  DDD = Julian day of acquisition
  X = (0=off; 1=on) Hyperion
  X = (0=off; 1=on) ALI
  X = (0=off; 1=on) AC
  M = Pointing Mode (N=Nadir; P=Pointed within path/row, 
      K=Pointed outside path/row
  L = Scene Length (F=Full scene, P=Partial scene, Q=Second partial scene, 
        S=Swath, *Other letters may be used to create distinct entity IDs) 
  GGG = Ground/Receiving Station 
  VV = Version Number


README

The README.txt is this text file.


READING DATA

Delivered via electronic file transfer protocol, data files may be zipped 
only or tarred and gzip-compressed.  UNIX systems should have the "unzip" 
or "gunzip" and "tar" commands available for uncompressing and accessing 
the data. For PC users, free software can be downloaded from on online 
source. Otherwise, check your PC, as you may already have appropriate 
software available.


GENERAL INFORMATION AND DOCUMENTATION

For further information about EO-1, see:
http://eo1.usgs.gov/

No software is included on this product for viewing EO-1 data.

For FGDC metadata, see:
http://www.fgdc.gov


CUSTOMER SUPPORT

Direct questions regarding EO-1 to the USGS Earth Resources
Observation and Science (EROS) Customer Services at 1-800-252-4547 or email:
http://earthexplorer.usgs.gov/feedback

USGS EROS:
http://eros.usgs.gov

For information about other USGS products, see:
http://ask.usgs.gov or call 1-888-ASK-USGS (275-8747)

For information about the USGS National Map, see: 
http://nationalmap.usgs.gov


DISCLAIMER

Any use of trade, product, or firm names is for descriptive purposes
only and does not imply endorsement by the U.S. Government.


Publication Date: January 2013
