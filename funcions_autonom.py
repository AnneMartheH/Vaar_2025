import numpy as np 
from global_land_mask import globe 
import matplotlib.pyplot as plt


def min_max_nomralization(data):
    return (data - data.min()) / (data.max() - data.min())

def latLong_to_piksel(target_lat, target_lon, latitudes, longitudes):  
    pikselRow = []
    pikselCol = []

    for i in range(4):
        # Calculate the absolute difference between the target and all lat/lon values
        lat_diff = np.abs(latitudes - target_lat[i])
        lon_diff = np.abs(longitudes - target_lon[i])

        # Find the indices of the minimum difference
        row, col = np.unravel_index(np.argmin(lat_diff + lon_diff), latitudes.shape)
        #row = np.argmin(np.abs(latitudes - target_lat[i]))
        #col = np.argmin(np.abs(longitudes - target_lon[i]))

        pikselRow.append(row)
        pikselCol.append(col)

    return pikselRow, pikselCol

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

def water_masked_rss_and_chl(row, column, l1d_cube, satobj_h1, chl ):
    sorted_row = sorted(row)
    sorted_col = sorted(column)
    
    rows_water = []
    cols_water = []
    chl_values = []
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
        chl_values.append(chl[rows_water[i],cols_water[i]]) #sjekke rekkefølgen på disse
        for k in range(5,115):
            rss_matrix[k-5][pixelNr] = l1d_cube[rows_water[i],cols_water[i],k]
        pixelNr=pixelNr+1
    print("Pixel number: ", pixelNr)
    return rss_matrix, chl_values


##sende denne fila per mail og sjekke om den funker :))))
## legge in en liten sjekk om hvor nørme en piskel er land..... 

##men først sjekke om denne funker 

def plot_coaastal_line(satobj_h1, l1c_cube):
    fig, ax = plt.subplots()
    band = 20
    # Display the full 2D slice of the cube at the specified band
    img = ax.imshow(l1c_cube[:, :, band], cmap='viridis')  # Only call imshow once
    ax.set_title(f'costal line plotted')
    ax.set_xlabel('Pixel column')
    ax.set_ylabel('Pixel row')

    for i in range(len(satobj_h1.latitudes)):
        for j in range(len(satobj_h1.longitudes)):
            if globe.is_ocean(satobj_h1.latitudes[i][j], satobj_h1.longitudes[i][j]):
                #if(globe.is_land(satobj_h1.latitudes[i][j-1], satobj_h1.longitudes[i][j-1])):
                    #plt.plot(satobj_h1.longitudes[i][j], satobj_h1.latitudes[i][j], 'bo')
                    ax.scatter(i, j, color='red', s=1)
    
    plt.colorbar(img, ax=ax)
    return

def rss_matrix_selected_bands(row, column, l1d_cube, satobj_h1): ## fiske over denne  etter de nye enklere funkjsonene er lagd 
    selected_bands = [15, 67, 95, 102]

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

    rss_matrix = np.zeros((len(selected_bands), pixelNr)) #floats
    #print(pixelNr)

    for i in range(len(rows_water)):
        for k in range(len(selected_bands)):
            rss_matrix[k][i] = l1d_cube[rows_water[i],cols_water[i],selected_bands[k]]

    print("Pixel number: ", pixelNr)
    return rss_matrix

def water_filter(target_row, target_column, satobj_h1):
    sorted_row = sorted(target_row)
    sorted_col = sorted(target_column)
    
    rows_water = []
    cols_water = []
    pixelNr=0

    for i in range(sorted_row[1], sorted_row[-2]+1): #iterating from second smallest to secound biggest and the secound biigest value
        for j in range(sorted_col[1], sorted_col[-2]+1):
            if globe.is_ocean(satobj_h1.latitudes[i][j], satobj_h1.longitudes[i][j]): ## sjekke rekkefølgen på disse 
                rows_water.append(i)
                cols_water.append(j)
    
                pixelNr=pixelNr+1

    return rows_water, cols_water, pixelNr


def water_masked_rss_and_chl_and_angles(row, column, l1d_cube, satobj_h1, chl, angles ):
    sorted_row = sorted(row)
    sorted_col = sorted(column)
    
    rows_water = []
    cols_water = []
    chl_values = []
    solar_zenith_angles = []
    solar_azimuth_angles = []
    sensor_zenith_angles = []
    sensor_azimuth_angles = []
    relative_azimuth_angles = []
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
        chl_values.append(chl[rows_water[i],cols_water[i]]) #sjekke rekkefølgen på disse
        solar_zenith_angles.append(angles[0][rows_water[i],cols_water[i]])
        solar_azimuth_angles.append(angles[1][rows_water[i],cols_water[i]])
        sensor_zenith_angles.append(angles[2][rows_water[i],cols_water[i]])
        sensor_azimuth_angles.append(angles[3][rows_water[i],cols_water[i]])
        relative_azimuth_angles.append(angles[4][rows_water[i],cols_water[i]])
        for k in range(5,115):
            rss_matrix[k-5][pixelNr] = l1d_cube[rows_water[i],cols_water[i],k]
        pixelNr=pixelNr+1
    print("Pixel number: ", pixelNr)
    return rss_matrix, chl_values, sensor_zenith_angles, solar_azimuth_angles, sensor_zenith_angles, sensor_azimuth_angles, relative_azimuth_angles
    
def water_masked_angles(row, column, satobj_h1, angles):
    sorted_row = sorted(row)
    sorted_col = sorted(column)
    
    rows_water = []
    cols_water = []
    solar_zenith_angles = []
    solar_azimuth_angles = []
    sensor_zenith_angles = []
    sensor_azimuth_angles = []
    relative_azimuth_angles = []
    pixelNr=0

    for i in range(sorted_row[1], sorted_row[-2]+1): #iterating from second smallest to secound biggest and the secound biigest value
        for j in range(sorted_col[1], sorted_col[-2]+1):
            if globe.is_ocean(satobj_h1.latitudes[i][j], satobj_h1.longitudes[i][j]): ## sjekke rekkefølgen på disse 
                rows_water.append(i)
                cols_water.append(j)
    
                pixelNr=pixelNr+1

    for i in range(len(rows_water)):
        #chl_values.append(chl[rows_water[i],cols_water[i]]) #sjekke rekkefølgen på disse
        solar_zenith_angles.append(angles[0][rows_water[i],cols_water[i]])
        solar_azimuth_angles.append(angles[1][rows_water[i],cols_water[i]])
        sensor_zenith_angles.append(angles[2][rows_water[i],cols_water[i]])
        sensor_azimuth_angles.append(angles[3][rows_water[i],cols_water[i]])
        relative_azimuth_angles.append(angles[4][rows_water[i],cols_water[i]])
    print("Pixel number: ", pixelNr)
    return sensor_zenith_angles, solar_azimuth_angles, sensor_zenith_angles, sensor_azimuth_angles, relative_azimuth_angles

def water_masked_chl(row, column, satobj_h1, chl):
    sorted_row = sorted(row)
    sorted_col = sorted(column)
    
    rows_water = []
    cols_water = []
    chl_values = []
    pixelNr=0

    for i in range(sorted_row[1], sorted_row[-2]+1): #iterating from second smallest to secound biggest and the secound biigest value
        for j in range(sorted_col[1], sorted_col[-2]+1):
            if globe.is_ocean(satobj_h1.latitudes[i][j], satobj_h1.longitudes[i][j]): ## sjekke rekkefølgen på disse 
                rows_water.append(i)
                cols_water.append(j)
    
                pixelNr=pixelNr+1

    for i in range(len(rows_water)):
        chl_values.append(chl[rows_water[i],cols_water[i]]) #sjekke rekkefølgen på disse

    print("Pixel number: ", pixelNr)
    return chl_values

def hyps1_rss_matrix(cube_norm, end_points_row, end_points_col, satobj_h1):
   sorted_row = sorted(end_points_row)
   sorted_col = sorted(end_points_col)
   
   rows_water = []
   cols_water = []
   pixelNr=0
   rss_matrix = []
   
   for i in range(sorted_row[1], sorted_row[-2]+1): #iterating from second smallest to secound biggest and the secound biigest value
        for j in range(sorted_col[1], sorted_col[-2]+1):
            if globe.is_ocean(satobj_h1.latitudes[i][j], satobj_h1.longitudes[i][j]): ## sjekke rekkefølgen på disse 
                if (not np.isnan(cube_norm[i][j]).any()):
                    rows_water.append(i)
                    cols_water.append(j)

                    pixelNr=pixelNr+1

   for i in range(len(rows_water)):
    rss_matrix.append(cube_norm[rows_water[i]][cols_water[i]])

   print("Pixel number: ", pixelNr)
   return np.array(rss_matrix)