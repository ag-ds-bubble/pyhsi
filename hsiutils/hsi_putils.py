    
def angle_to90(img):
    imgproc = (img!=0).astype(int)
    rows,cols = imgproc.shape
    ptA, ptB = (None, None), (None, None)
    idx = 0
    while ptA == (None, None) and idx < cols:
        if sum(imgproc[:,idx])>0:
            ptA = (idx, np.argmax(imgproc[:,idx]))
            break
        idx+=1
    idx=0
    while ptB == (None, None) and idx < rows:
        if sum(imgproc[idx,:])>0:
            ptB = (np.argmax(imgproc[idx,:]),idx)
            break
        idx+=1

    angle = np.rad2deg(np.arctan((ptB[0]-ptA[0])/(ptA[1]-ptB[1])))
    return angle

def rotate_image(mat, angle):
    """
    Rotates an image (angle in degrees) and expands image to avoid cropping
    """

    height, width = mat.shape[:2] # image shape has 3 dimensions
    image_center = (width/2, height/2) 

    # getRotationMatrix2D needs coordinates in reverse order (width, height) compared to shape
    rotation_mat = cv2.getRotationMatrix2D(image_center, angle, 1.)
    
    # rotation calculates the cos and sin, taking absolutes of those.
    abs_cos = abs(rotation_mat[0,0]) 
    abs_sin = abs(rotation_mat[0,1])

    # find the new width and height bounds
    bound_w = int(height * abs_sin + width * abs_cos)
    bound_h = int(height * abs_cos + width * abs_sin)

    # subtract old image center (bringing image back to origo) and adding the new image center coordinates
    rotation_mat[0, 2] += bound_w/2 - image_center[0]
    rotation_mat[1, 2] += bound_h/2 - image_center[1]

    # rotate image with the new bounds and translated rotation matrix
    rotated_mat = cv2.warpAffine(mat, rotation_mat, (bound_w, bound_h))
    return rotated_mat

def prep_specmat(imgpaths, band_ident, save_file=''):
    
    if prepareddata_path+save_file in os.listdir(prepareddata_path):
        return np.load(PREPAREDDATA_PATH+save_file)

    def atoi(text):
        return int(text) if text.isdigit() else text
    def natural_keys(text):
        return [atoi(c) for c in re.split(band_ident, text) ]

    paths = sorted(np.copy(imgpaths), key=natural_keys)
    specmat = []
    for epath in paths:
        band_no = re.search(band_ident, epath).group(1)
        specmat.append(tiff.imread(epath))
    specmat = np.dstack(tuple(specmat))
    return specmat
        
def display_rst_prop(imgpath, dst_crs = 'EPSG:4326'):
    src = rst.open(imgpath)
    print('Data set Name : ', src.name)
    print('Data set Mode : ', src.mode)
    print('Data set Closed : ', src.closed)
    print(f'Coordinate Reference System : {src.crs}')
    print('Number of bands contained : ', src.count)
    print(f'Height x Width : {src.height} x {src.width}')
    print('Band data type : ',{i: dtype for i, dtype in zip(src.indexes, src.dtypes)})
    print('Image bounding Box : ')
    _top, _bottom, _left, _right = src.bounds[3], src.bounds[1], src.bounds[0], src.bounds[2]
    print('\t Left Most Spatial Marker', _left)
    print('\t Right Most Spatial Marker', _right)
    print('\t Bottom Most Spatial Marker', _bottom)
    print('\t Top Most Spatial Marker', _top)
    print(f'\t\t Top Left Coordinates in {src.crs} CRS: {_left, _top}')
    print(f'\t\t Top Right Coordinates in {src.crs} CRS: {_right, _top}')
    print(f'\t\t Bottom Right Coordinates in {src.crs} CRS: {_left, _bottom}')
    print(f'\t\t Bottom Left Coordinates in {src.crs} CRS: {_right, _bottom}\n')
    src_crs_cords = np.array([[_left, _top],
                                [_right, _top],
                                [_right, _bottom],
                                [_left, _bottom]])
    cord_pnames = ['Top Left', 'Top Right', 'Bottom Right', 'Bottom Left']

    for eachname, eachcoord in zip(cord_pnames, src_crs_cords):
        lat,long = rasterio.warp.transform(src_crs= src.crs.__str__(),
                                        dst_crs = dst_crs,
                                        xs=[eachcoord[0]], ys=[eachcoord[1]])
        print(f'\t\t {eachname} Corrdinates in {dst_crs} CRS : {(lat[0], long[0])}')

    print(f'\n\t Total Width  {_right-_left} mt')
    print(f'\t Total Height {_top-_bottom} mt')

def to_epsg4326(self, _long, _lat, from_crs='EPSG:32643', to_crs='EPSG:4326'):
    """
    Returns long and lat
    """
    long, lat = rst.warp.transform(src_crs= from_crs,
                                    dst_crs= to_crs,
                                    xs=[_long], ys=[_lat])
    return long[0], lat[0]        
    
