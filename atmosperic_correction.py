import numpy as np 
import math
from global_land_mask import globe 
import funcions_autonom as f ##hvis ting blir kaos kan det vøre denne

def rss_atm_corrected(who_var_wavelwngths, cla_atm_data):
    rss_atmc = []
    for var in who_var_wavelwngths : 
        rss_atmc.append(cla_atm_data[var]/math.pi)
    
    return np.array(rss_atmc)

def piksles_in_slected_area(start_end_piksel_row, start_end_piksle_col, latitudes, longitudes):
    sorted_row = sorted(start_end_piksel_row)
    sorted_col = sorted(start_end_piksle_col)

    rows_water = []
    cols_water = []

    for i in range(sorted_row[1], sorted_row[-2]+1): #iterating from second smallest to secound biggest and the secound biigest value
        for j in range(sorted_col[1], sorted_col[-2]+1):
            if globe.is_ocean(latitudes[i][j], longitudes[i][j]): ## sjekke rekkefølgen på disse 
                rows_water.append(i)
                cols_water.append(j)

    return rows_water, cols_water 

def rss_given_pixels(rows, columns, rss_data):
    rss_given = []
    for i in range(len(rows)):
        piksel_values = rss_data[:, rows[i], columns[i]]
        has_nan = np.isnan(piksel_values)
        if has_nan.any() == False:
            rss_given.append(rss_data[:, rows[i], columns[i]])
        
    return np.array(rss_given)

def rss_matrix_for_several_Areas_same_picture(target_lat_matrix, target_lon_matrix, latitudes, longitudes, rss_all):
    rss_area_matrix = []
    for i in range(len(target_lat_matrix)):
        #matrise[i] -> en hel rad 
        start_end_row, start_end_col = f.latLong_to_piksel(target_lat_matrix[i], target_lon_matrix[i], latitudes, longitudes)
        area_in_piksels_row, area_in_piksels_col = piksles_in_slected_area(start_end_row, start_end_col, latitudes, longitudes)
        rss_area = rss_given_pixels(area_in_piksels_row, area_in_piksels_col, rss_all)
        rss_area_matrix.append(rss_area)
    
    return rss_area_matrix #kan ikke gjøre til np.array her fordi listene har ulik størrelse 




     