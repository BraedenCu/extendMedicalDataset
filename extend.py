import numpy as np
import os
import sys
import nibabel as nib
import numpy as np
import pdb
import SimpleITK as sitk
from PIL import Image
import nrrd

def read_nii_bysitk(input_fid, peel_info = False):
    """ read nii to numpy through simpleitk

        peelinfo: taking direction, origin, spacing and metadata out
    """
    img_obj = sitk.ReadImage(input_fid)
    img_np = sitk.GetArrayFromImage(img_obj)
    if peel_info:
        info_obj = {
                "spacing": img_obj.GetSpacing(),
                "origin": img_obj.GetOrigin(),
                "direction": img_obj.GetDirection(),
                "array_size": img_np.shape
                }
        return img_np, info_obj
    else:
        return img_np
    
def printDim(npArr): 
    print("{}   {}  {} {}".format(npArr.ndim, npArr.shape, npArr.size, len(npArr)))
 

def mirror():
    input = "/home/dev/dev/IMSA/SIR/IIT/extendingDataset/output.nrrd"
    annotations = "/home/dev/dev/IMSA/SIR/IIT/extendingDataset/annotation.nrrd"
    readdata, header = nrrd.read(input);
    readannot, headerannot = nrrd.read(annotations);

    #gives the first (index 0) intended front view of image
    firstSegment = readdata[:, :, 0]
    firstAnnot = readannot[:, :, 0]
    
    #dimensions of data
    dim1, dim2, dim3 = readdata.shape
    
    #mirrors first ten images, mirrors left side
    #mirror left = mirror of left side 
    mirrorLeftSegments = np.zeros((456, 456, 503))
    mirrorLeftAnnotation = np.zeros((456, 456, 503))
    mirrorRightSegments = np.zeros((456, 456, 503))
    mirrorRightAnnotation = np.zeros((456, 456, 503))

    
    for i in range(0, dim3):
        segment = readdata[:, :, i] #get shape of one slice
        x, y = segment.shape #get x and y values
        for i1 in range(0, int(x/2)):
            for i2 in range(0, y):
                #creating left side mirror
                #newX, newY = mirrorX, mirror Y, set mirrored side
                mirrorLeftSegments[455-i1][i2][i] = readdata[i1][i2][i]
                #set regular side (just a copy)
                mirrorLeftSegments[i1][i2][i] = readdata[i1][i2][i]
                #mirror annotations
                mirrorLeftAnnotation[455-i1][i2][i] = readannot[i1][i2][i]
                mirrorLeftAnnotation[i1][i2][i] = readannot[i1][i2][i] 
                #creating right side mirror
                mirrorRightSegments[i1][i2][i] = readdata[455-i1][i2][i]
                mirrorRightSegments[i1][i2][i] = readdata[i1][i2][i]
                mirrorRightAnnotation[i1][i2][i] = readannot[455-i1][i2][i]
                mirrorRightAnnotation[i1][i2][i] = readannot[i1][i2][i]  
                
    nrrd.write("mirrorLeftSegments.nrrd", mirrorLeftSegments)
    nrrd.write("mirrorLeftAnnotation.nrrd", mirrorLeftAnnotation)
    nrrd.write("mirrorRightSegments.nrrd", mirrorRightSegments)
    nrrd.write("mirrorRightAnnotation.nrrd", mirrorRightAnnotation)

if __name__ == "__main__":
    mirror()