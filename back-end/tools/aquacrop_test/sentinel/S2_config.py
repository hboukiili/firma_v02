
write_dir='/home/zoubairrafi/Postdoc_Satirr_Wago/media/S2/'

"""
Configuration des images Sentinel-2 provenant de l'ESA
S2_authorized est la liste des tuiles à télécharger depuis l'ESA
"""
S2_authorized=["31TCJ","31TDJ","31TCH","31TDH","31TCG","30TYM","31TBG","29SPR","29SNR","29RNQ","29RPQ","32SNE","32SPE","30TYP","30TXP","36SYC","37SBT","37SBU","32SPF"]
S2_authorized=["29SPR","29SNR"]
downloader="aria2"
url_search="https://scihub.copernicus.eu/apihub/search?rows=100&q="
account="michel"
passwd="michel123"
sentinel="S2"
no_download=False

path_to_sen2cor='/home/michel/sen2cor'
path_to_anaconda2 = '/home/michel/anaconda2'
sen2cor_init="export SEN2COR_HOME=%s;export SEN2COR_BIN=%s/lib/python2.7/site-packages/sen2cor-2.3.0-py2.7.egg/sen2cor;export GDAL_DATA=%s/lib/python2.7/site-packages/sen2cor-2.3.0-py2.7.egg/sen2cor/cfg/gdal_data" % (path_to_sen2cor,path_to_anaconda2,path_to_anaconda2)

Cloud_mask_L1C = False
Cloud_mask_sen2cor = True

#ValuesListDict_medium_probability = {'bords':[0],'nuages' : [8,9,10], 'ombres' : [3], 'neige' : [11], 'eau' : [6]}
#ValuesListDict_high_probability = {'bords':[0],'nuages' : [9,10], 'ombres' : [3], 'neige' : [11], 'eau' : [6]}
#ValuesListDict_high_probability = {'bords':[0],'nuages' : [9,10], 'ombres' : [3]}
ValuesListDict_high_probability = {'bords':[0],'nuages' : [8,9,10], 'ombres' : [3], 'neige' : [11], 'eau' : [6]}

"""
Configuration des images Sentinel-2 provenant de THEIA
"""
Theia_S2_authorized=["31TCK"]
Theia_S2_authorized=[]

config_theia = {
	'serveur' : 'https://theia.cnes.fr/atdistrib',
	'resto' : 'resto2',
	'token_type' : 'text',
	'login_theia' : 'michel.lepage@cesbio.cnes.fr',
	'password_theia' : 'Michel123!',
	#'proxy' = 'http://proxy.truc.fr:8050',
	#'login_proxy' = 'login_proxy',
	#'password_proxy' = 'passwd_proxy',
	'platform' : 'SENTINEL2A',
	'collection' : 'SENTINEL2',	
	'downloader' : "aria2",
	'maxcloud' : 75
	}
