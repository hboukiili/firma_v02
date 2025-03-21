# -*- coding: utf-8 -*-
"""
Created on Thu Apr 28 18:07:58 2016

"""
import os
import glob
import shutil

repert="/media/SATIRR/data"
img_name="S2A_OPER_PRD_MSIL1C_PDMC_20160408T232349_R008_V20160408T104845_20160408T104845.SAFE"
img_out="S2A_OPER_PRD_MSIL1C_PDMC_20160408T232349_R008_V20160408T104845_20160408T104845.SAFE_satirr"

ndvi_list=[]
pat=os.path.join(repert,img_name)

pat_satirr=os.path.join(repert,img_name+'_satirr')
os.mkdir(pat_satirr)

list_granules=glob.glob(os.path.join(pat,"GRANULE/*"))
for granule in list_granules:
    granule_name=granule.split('/')
    granule_name=granule_name[len(granule_name)-1]
    print(granule_name)
    granule_dir=os.path.join(repert,granule_name)
    # create the granule directory
    os.mkdir(granule_dir)
    # copy auxiliariy repertories
    shutil.copytree(os.path.join(pat,"AUX_DATA"),os.path.join(granule_dir,"AUX_DATA"))
    shutil.copytree(os.path.join(pat,"DATASTRIP"),os.path.join(granule_dir,"DATASTRIP"))
    shutil.copytree(os.path.join(pat,"HTML"),os.path.join(granule_dir,"HTML"))
    shutil.copytree(os.path.join(pat,"rep_info"),os.path.join(granule_dir,"rep_info"))
    # copy 4 auxiliary files
    file_list=glob.glob(os.path.join(pat,"*.*"))
    for fn in file_list:
        shutil.copyfile(fn,fn.replace(img_name,granule_name))
    # create GRANULE directory
    os.mkdir(os.path.join(granule_dir,"GRANULE"))
    # copy one granule tree
    shutil.copytree(os.path.join(pat,"GRANULE",granule_name),os.path.join(granule_dir,"GRANULE",granule_name))

    # execute sen2cor 
    os.system("L2A_Process "+os.path.join(repert,granule_name)+" --resolution 10")
    
    sen2cor_dir=granule_dir.replace("OPER","USER")
    
    # compute NDVI from sen2cor_dir
  
    # rajouter le nom du fichier NDVI à la liste
    #ndvi_list.append(ndvi_fname)
    
    # CLEAN: delete sen2cor_dir and granule_dir
    #shutil.rmtree(granule_dir)
    #shutil.rmtree(sen2cor_dir)
    
# fin de la boucle, on fait le merge des ndvis avec gdal_merge


    
    
    
    
