import os
from zipfile import ZipFile
import tifffile as tiff
import matplotlib.pyplot as plt
import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from tqdm import tqdm

from hsiutils import angle_to90, imgshowN, rotate_image, plot_elbow, dict_io
from hsiutils import SpectralAnalysis, HSClusterAnalysis


# Path and Variable Initialialisation
# Variables
tilename = 'EO1H1480472016328110PZ'
tileset = 'tile1'
# Paths
RAWDATA_PATH = 'raw_data/' # Raw Data Root PathR
RAWTILE_PATH = RAWDATA_PATH+f'{tilename}.zip'
PREPDATA_PATH = 'prep_data/' # Prepared Data Root Path
PREPTILE_PATH = PREPDATA_PATH+f'{tileset}/'
for epath in [RAWDATA_PATH, PREPDATA_PATH, PREPTILE_PATH]:
    os.makedirs(epath, exist_ok=True)

spcmat_orig_path = PREPTILE_PATH+'specmat_orig.pkl'
spcmat_rotated_path = PREPTILE_PATH+'specmat_rotated.pkl'
spcmat_rotatedslice_path = PREPTILE_PATH+'specmat_rotatedsliced.pkl'
matrixX_path = PREPTILE_PATH+'matrixX.pkl'
classMasks_path = PREPTILE_PATH+'classMasks.pkl'

########################### DATA HANDLING ###########################
# Unzip all files and get all the tile paths and then read all the tiles in the dataset
print('\n########################### DATA HANDLING ###########################')
if os.listdir(PREPTILE_PATH) == []:
    with ZipFile(RAWTILE_PATH, 'r') as zip_ref:
        zip_ref.extractall(PREPTILE_PATH)
tile_imgpaths = [PREPTILE_PATH+f'{tilename}/'+k for k in os.listdir(PREPTILE_PATH+f'{tilename}/') if '.TIF' in k]
tile_imgs = []
for epath in tile_imgpaths:
    tile_imgs.append(tiff.imread(epath))
print(f'1.) [READ] Total of {len(tile_imgpaths)} tiles in the Pool')


# Calulation of the mean of the roation angle to each tile
indangles = []
for etile in tile_imgs:
    indangles.append(angle_to90(etile))
mean_angleto90 = np.mean(indangles)
print('2.) [PROCESS] Average angle to 90 : ', mean_angleto90)
origimg = tile_imgs[37]
rotatedimg = rotate_image(origimg, mean_angleto90)
imgshowN([origimg, rotatedimg], [f'Original @ {origimg.shape}', f'Rotated @ {rotatedimg.shape}'])


# Prepare Spectral Data
specmat_orig = []
specmat_rotated = []
for etile in tile_imgs:
    rotimg = rotate_image(etile, mean_angleto90)
    specmat_rotated.append(rotimg)
    specmat_orig.append(etile)
    
specmat_orig = np.dstack(tuple(specmat_orig))
specmat_rotated = np.dstack(tuple(specmat_rotated))
np.save(spcmat_orig_path, specmat_orig)
np.save(spcmat_rotated_path, specmat_rotated)
specmat_orig = np.load(spcmat_orig_path+'.npy')
specmat_rotated = np.load(spcmat_rotated_path+'.npy')
print('3.) [PROCESS] Preparation of the Spectral Matrix')
print('\t3.1) Orignal Spectral matrix shape : ', specmat_orig.shape)
print('\t3.2) Rotated Spectral matrix shape : ', specmat_rotated.shape)


# Deal with NaN data
volume_sum   = specmat_rotated.sum(axis=2)
volume_mean  = specmat_rotated.mean(axis=2)
volume_meanmask2d = volume_mean>0

xmin, xmax = np.where(volume_meanmask2d)[0].min(), np.where(volume_meanmask2d)[0].max()
ymin, ymax = np.where(volume_meanmask2d)[1].min(), np.where(volume_meanmask2d)[1].max()

ptA = (xmin,ymin)
ptB = (xmax,ymin)
ptC = (xmax,ymax)
ptD = (xmin,ymax)

specmat_rotated_sliced = specmat_rotated[ptA[0]:ptB[0]+1, ptB[1]:ptC[1]+1,:].copy()
print('\t3.3) Rotated-Sliced Spectral matrix shape : ', specmat_rotated_sliced.shape)
imgshowN([specmat_orig.mean(axis=2), specmat_rotated.mean(axis=2), specmat_rotated_sliced.mean(axis=2)],
         ['Orignal', 'Rotated', 'Rotated-Sliced'])
np.save(spcmat_rotatedslice_path, specmat_rotated_sliced)
specmat_rotated_sliced = np.load(spcmat_rotatedslice_path+'.npy')
print('#####################################################################\n')




print('############################# ANALYSIS ##############################')
specAnalysisTab = SpectralAnalysis(spectral_data = specmat_rotated_sliced)
print('#####################################################################\n')


print('#################### DIMENSIONALITY REDUCTION #######################')
specmat_rotated_sliced_2d = specmat_rotated_sliced.reshape(specmat_rotated_sliced.shape[0]*specmat_rotated_sliced.shape[1],
                                                            specmat_rotated_sliced.shape[2]).copy()
scaler = StandardScaler()
specmat_rotated_sliced_2d_scaled = scaler.fit_transform(specmat_rotated_sliced_2d)
pca = PCA(n_components=5, svd_solver='full')
specmat_rotated_sliced_DR_pca = pca.fit_transform(specmat_rotated_sliced_2d_scaled)

b1 = specmat_rotated_sliced.mean(axis=2)
b2 = specmat_rotated_sliced.std(axis=2)
b3 = specmat_rotated_sliced_DR_pca[:,0].reshape(specmat_rotated_sliced.shape[0],specmat_rotated_sliced.shape[1])
b4 = specmat_rotated_sliced_DR_pca[:,1].reshape(specmat_rotated_sliced.shape[0],specmat_rotated_sliced.shape[1])

comb =  np.dstack((b1,b2,b3,b4))
DR_COMB = comb.reshape(b1.shape[0]*b1.shape[1],4)
np.save(matrixX_path, DR_COMB)
DR_COMB = np.load(matrixX_path+'.npy')
print('4) Dimensions After Dimensionality Reduction : ', DR_COMB.shape)
print('#####################################################################\n')


print('#################### UNSUPERVISED CLUSTERING #######################')
all_classification_masks = {} # Dictionary to hold all the Classification Masks so Produced
clst_mode = 'kmeans' # Upsupervised Clustering Mode
dr_mode = 'Mn_Std_PCA01' # Data Reduction Mode
kmeans_intertia_dict = {}
matrix_X = DR_COMB.copy()
print(f'5) Unsupervised Clustering in {clst_mode} after {dr_mode} mode of Data Reduction:')

# Kmeans
clusters = [k for k in range(1,10)]
for i in tqdm(clusters):
    km = KMeans(n_clusters=i)
    km.fit(matrix_X)
    kmeans_intertia_dict[i] = km.inertia_
    _labels = km.predict(matrix_X)
    all_classification_masks[dr_mode+'_'+clst_mode+f'_c{i}'] = _labels.reshape(specmat_rotated_sliced.shape[0], 
                                                                               specmat_rotated_sliced.shape[1])

plot_elbow(measures = list(kmeans_intertia_dict.values()),
           clust = clusters)
dict_io(classMasks_path, obj=all_classification_masks)
all_classification_masks = dict_io(classMasks_path, mode='load')
print('#####################################################################\n')





print('########################## RESULT ANALYSIS ##########################\n')
# #TILESET 3
smasks = ['Mn_Std_PCA01_kmeans_c2', 'Mn_Std_PCA01_kmeans_c3',
          'Mn_Std_PCA01_kmeans_c4', 'Mn_Std_PCA01_kmeans_c5',
          'Mn_Std_PCA01_kmeans_c6', 'Mn_Std_PCA01_kmeans_c7',
          'Mn_Std_PCA01_kmeans_c8', 'Mn_Std_PCA01_kmeans_c9']
selected_masks = {k:all_classification_masks[k] for k in smasks}
clusteringAnalysis = HSClusterAnalysis(spectral_data = specmat_rotated_sliced,
                                       class_masks = selected_masks)
print('#####################################################################\n')

