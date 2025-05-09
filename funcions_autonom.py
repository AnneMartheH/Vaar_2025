import numpy as np 
from global_land_mask import globe 

def min_max_nomralization(data):
    return (data - data.min()) / (data.max() - data.min())

def latLong_to_piksel(target_lat, target_lon, latitudes, longitudes):  
    rowForPos = []
    colForPos = []

    for i in range(4):
        # Calculate the absolute difference between the target and all lat/lon values
        lat_diff = np.abs(latitudes - target_lat[i])
        lon_diff = np.abs(longitudes - target_lon[i])

        # Find the indices of the minimum difference
        row, col = np.unravel_index(np.argmin(lat_diff + lon_diff), latitudes.shape)
        #row = np.argmin(np.abs(latitudes - target_lat[i]))
        #col = np.argmin(np.abs(longitudes - target_lon[i]))

        rowForPos.append(row)
        colForPos.append(col)

    return rowForPos, colForPos

def rss_matrix(band, row, column, l1d_cube):
    sorted_row = sorted(row)
    sorted_col = sorted(column)

    pixelNr=0
    for i in range(sorted_row[1], sorted_row[-2]+1): #iterating from second smallest to secound biggest and the secound biigest value
        for j in range(sorted_col[1], sorted_col[-2]+1):
            pixelNr=pixelNr+1

    rss_matrix = np.zeros((110, pixelNr)) #floats
    #print(pixelNr)
    pixelNr = 0

    for i in range(sorted_row[1], sorted_row[-2]+1): #iterating from second smallest to secound biggest and the secound biigest value
        for j in range(sorted_col[1], sorted_col[-2]+1):
            for k in range(5,115):
                rss_matrix[k-5][pixelNr] = l1d_cube[i,j,k]
            pixelNr=pixelNr+1
    print("Pixel number: ", pixelNr)
    return rss_matrix

def water_masked_rss_matrix(row, column, l1d_cube, satobj_h1 ):
    sorted_row = sorted(row)
    sorted_col = sorted(column)
    
    rows_water = []
    cols_water = []
    pixelNr=0

    for i in range(sorted_row[1], sorted_row[-2]+1): #iterating from second smallest to secound biggest and the secound biigest value
        for j in range(sorted_col[1], sorted_col[-2]+1):
            if globe.is_ocean(satobj_h1.latitudes[i][j], satobj_h1.longitudes[i][j]): ## sjekke rekkefølgen på disse 
                rows_water.append(i)
                cols_water.append(j)
    
                pixelNr=pixelNr+1

    rss_matrix = np.zeros((110, pixelNr)) #floats
    #print(pixelNr)
    pixelNr = 0

    for i in range(len(rows_water)):
        for k in range(5,115):
            rss_matrix[k-5][pixelNr] = l1d_cube[rows_water[i],cols_water[i],k]
        pixelNr=pixelNr+1
    print("Pixel number: ", pixelNr)
    return rss_matrix


##sende denne fila per mail og sjekke om den funker :))))
## legge in en liten sjekk om hvor nørme en piskel er land..... 

##men først sjekke om denne funker 


