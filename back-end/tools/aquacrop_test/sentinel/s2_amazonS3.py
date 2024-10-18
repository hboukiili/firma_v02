# -*- coding: utf-8 -*-
"""
Created on Wed Feb 24 21:22:00 2016

Ca marche avec Kit SDK AWS pour Python (Boto3) 
https://aws.amazon.com/fr/sdk-for-python/

"""

import boto3
from botocore.handlers import disable_signing
import os

#S2bucket='sentinel-s2-l1c.s3-website.eu-central-1.amazonaws.com'
S2bucket2='sentinel-s2-l1c'

dst_dir='C:\\Users\\michel\\Documents'

s3 = boto3.resource('s3')
s3.meta.client.meta.events.register('choose-signer.s3.*', disable_signing)

bucket = s3.Bucket(S2bucket2)
kk=bucket.objects.filter(Prefix='tiles/30/S/TB/2016',MaxKeys=20)

for key in kk.all():
    print(key.key,' ', key.size,' bytes')
    aaa=key.key.split('/')
    name=aaa[len(aaa)-1]
    path = os.path.join(dst_dir, name)
    bucket.download_file(key.key, path)
