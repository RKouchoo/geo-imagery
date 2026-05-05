from satpy import Scene, find_files_and_readers
import dask

from pathlib import Path
import shutil
import warnings
from glob import glob
    
warnings.filterwarnings('ignore', 'Mean of empty slice', category=RuntimeWarning)
warnings.filterwarnings('ignore', 'invalid value encountered in divide', category=RuntimeWarning)

# https://github.com/pytroll/satpy/blob/main/satpy/etc/readers/ahi_hsd.yaml
# https://github.com/pytroll/satpy/blob/main/satpy/etc/composites/ahi.yaml

def SubDirPath (d):
    return [f for f in d.iterdir() if f.is_dir()]

dask.config.set(**{'array.slicing.split_large_chunks': False})


outputdir = "./completed2/"
existingImgs = glob(f"{outputdir}*.png")


#..\data\processed\noaa-himawari9\202602171430
datDirs = SubDirPath(Path(r'./data/processed/noaa-goes19'))
renderTemplate = "true_color_reproduction_uncorr" #colorized_ir_clouds true_color_reproduction_uncorr true_color_reproduction_corr

renderQue = []

for dataDir in datDirs:

    imageName = f"{renderTemplate}.{str(dataDir).strip("data/processed/noaa-goes19/")}.png"
    print(imageName)

    if outputdir + imageName in existingImgs:
        continue
    else:
        renderQue.append(dataDir)

if (len(renderQue) == 0):
    print("No images to render, exiting...")
    exit

print(f"{len(renderQue)} Images to render, starting...")     




for job in renderQue:
    
    with dask.config.set({"array.chunk-size" : "512MiB"}):
 
        imageName = f"{renderTemplate}.{str(job).strip("data/processed/noaa-goes19/")}.png"

        #abi_dataset_reader = find_files_and_readers(base_dir=job, reader="abi_l1b")

        files=glob(f"{job}/*.nc")
        
        dataset_scene = Scene(reader="abi_l2_nc", filenames=files, reader_kwargs={'mask_space': False})

        dataset_scene.load([renderTemplate], generate=False)
        resampled_dataset_scene = dataset_scene.resample(dataset_scene.coarsest_area(), cachedir="./rendercache", resampler="native")
       
        resampled_dataset_scene.save_datasets(dataset_id=renderTemplate, filename=imageName, compute=True)
        print("Rendered: " + imageName)

        shutil.move(imageName, outputdir)
