#!/usr/bin/env python3

'''
# Extract acoustic LLDs (MFCC and eGeMAPS sets from openSMILE)
# Output: csv files
# Authors: AVEC 2019 competition and Daniel M. Low (MIT)
License: Apache 2.0
'''


import os
import time
import pandas as pd


pd.options.display.width = 0


def extract_features(feature_type = 'compare16'  , funtionals = True, opensmile_dir = './../opensmile-2.3.0/',input_dir = './', output_dir='./'):
	# feature_type = 'mfcc' or 'egemaps'
	# functional = if False, will output sequences (withouth stats), if True then outputs vector (with stats/functionals)



	# Run
	if funtionals:
		outputoption = '-csvoutput'  # lldcsvoutput is with funcs OR csvoutput without funcs|| MFCC only outputs windowed version || options from standard_data_output_lldonly.conf.inc
		# output_dir = output_dir + feature_type + '_vector/'
	else:
		outputoption = '-lldcsvoutput'  # lldcsvoutput is with funcs OR csvoutput without funcs|| MFCC only outputs windowed version || options from standard_data_output_lldonly.conf.inc
		# output_dir = output_dir + feature_type + '_sequence/'

	'''
	mfcc:                   39  (vector)
	gemaps:                 18  (sequence)
	gemaps + functionals:   62  (vector)
	egemaps:                23  (sequence)*
	egemaps + functionals:  88  (vector)*
	compare13:              130 (sequence)*
	compare13 + functionals: 6375 (vector)*
	compare16 == compare13
	'''

	'''
	n=1000
	p = 0.2
	x = np.random.binomial(1,p, size=n)
	x = [3 if n==0 else 5 for n in x]
	y = np.random.normal(np.mean(x), 0.5, size=n)
	g = sns.jointplot(x=x, y=y, kind='kde')


	'''

	# exe_opensmile = '/tools/opensmile-2.3.0/bin/linux_x64_standalone_static/SMILExtract'  # MODIFY this path to the folder of the SMILExtract (version 2.3) executable
	exe_opensmile = 'SMILExtract'  # MODIFY this path to the folder of the SMILExtract (version 2.3) executable
	path_config = opensmile_dir+'config/'  # MODIFY this path to the config folder of opensmile 2.3 - no POSIX here on cygwin (windows)

	if 'mfcc' == feature_type:
		conf_smileconf = path_config + 'MFCC12_0_D_A.conf'  # MFCCs 0-12 with delta and acceleration coefficients
	elif 'gemaps' == feature_type:
		conf_smileconf = path_config + 'gemaps/GeMAPSv01a.conf'  # eGeMAPS feature set
	elif 'egemaps' == feature_type:
		conf_smileconf = path_config + 'gemaps/eGeMAPSv01a.conf'  # eGeMAPS feature set
	# elif 'compare13' == feature_type: #This had some numerical errors according to Compare 2016
	# 	conf_smileconf = path_config + 'IS13_ComParE.conf'  # eGeMAPS feature set
	elif 'compare16' == feature_type:
		conf_smileconf = path_config + 'ComParE_2016.conf'  # eGeMAPS feature set
	else:
		print('Error: Feature type ' + feature_type + ' unknown!')

	# if not os.path.exists(output_dir):
	# 	os.mkdir(output_dir)

	for i, fn in enumerate(os.listdir(input_dir)):
		if fn == '.DS_Store' or not fn.endswith('.wav'):
			continue

		print('{} out of {}==========================='.format(i, len(os.listdir(input_dir))))
		infilename = input_dir + fn
		instname = os.path.splitext(fn)[0]
		outfilename = output_dir + instname + '.csv'
		opensmile_options = '-configfile ' + conf_smileconf + ' -appendcsvlld 0 -timestampcsvlld 1 -headercsvlld 1'  # options from standard_data_output.conf.inc
		opensmile_call = exe_opensmile + ' ' + opensmile_options + ' -inputfile ' + infilename + ' ' + outputoption + ' ' + outfilename + ' -instname ' + instname + ' -output ?'  # (disabling htk output)
		print(opensmile_call)
		os.system(opensmile_call)
		time.sleep(0.001)

	try:
		os.remove('smile.log')
	except:
		pass



def opensmile_dir_to_csv(input_dir = './', output_dir='./', output_filename='egemaps_vector'):
	files = os.listdir(input_dir)
	files = [n for n in files if '.csv' in n]

	all = []

	for file in files:
		df_1csv = pd.read_csv(input_dir+file, sep=';')
		try:
			del df_1csv['frameTime']
			all.append(df_1csv)
		except:
			pass



	df = pd.concat(all)
	df = df.reset_index(drop=True)
	df.to_csv(output_dir+output_filename+'.csv')
	return df



if __name__ == "__main__":

	# These filenames should have been corrected to 'freeres' in the wavs folder, but I didnt and extracted features, so I just search for them and manually changed names in all feature folders.
	# find . -type f -name "25702_p2_freeresponse.csv" -execdir mv {} '25702_p2_freeresp.csv' \;
	#
	# change_by_hand = ['09502_p4_freerespo', '10502_p3_freeresp_1', '19702_p1_freeresponse', '19702_p2_freeresponse',
	#                   '25301_p4_freeresponse', '25702_p1_freeresponse', '25702_p2_freeresponse']

	# MODIFY HERE
	input_dir = './../../libs/ml_pipeline/data/input/raw/audio_converted_wavs/'
	extract_features(feature_type='egemaps',opensmile_dir = './../opensmile-2.3.0/', funtionals=True, input_dir=input_dir,
	                 output_dir=input_dir)

	# 	Concat all csv to single csv.
	#1. loop through all dirs, for each dir, concat. l
	# Remove background , and sentences csv
	# For vectors create csv files with text, and have a column with the npy file for sequences.

	#
	feature_types = ['egemaps']
	trimmed = False
	# missing_sentences = ['05601_p3_freeresp.csv', '06501_p2_freeresp.csv', '06501_p3_freeresp.csv', '06501_p4_freeresp_1.csv', '06502_p2_freeresp.csv', '09002_p4_freeresp.csv', '09502_p1_freeresp.csv', '09502_p4_freeresp.csv', '10002_p1_freeresp_2.csv', '10502_p3_freeresp_1.csv', '10502_p3_freeresp_2.csv', '10701_p1_freeresp.csv', '10701_p2_freeresp.csv', '10701_p3_freeresp.csv', '12202_p1_freeresp.csv', '12202_p2_freeresp.csv', '12202_p3_freeresp.csv', '12202_p4_freeresp.csv', '13401_p4_freeresp.csv', '13701_p3_freeresp.csv', '13702_p3_freeresp.csv', '13702_p4_freeresp.csv', '16502_p1_freeresp.csv', '19702_p1_freeresp.csv', '19702_p2_freeresp.csv', '20201_p4_freeresp.csv', '21902_p2_freeresp.csv', '24401_p1_freeresp.csv', '24501_p3_freeresp.csv', '25301_p4_freeresp.csv', '25402_p3_freeresp.csv', '25601_p1_freeresp.csv', '25601_p2_freeresp.csv', '25702_p1_freeresp.csv', '25702_p2_freeresp.csv', '25702_p3_freeresp.csv', '25702_p4_freeresp.csv', '27001_p3_freeresp.csv'] #too noisy
	for feature_type in feature_types:
		df_audio = opensmile_dir_to_csv(input_dir = input_dir,
		                          output_dir = input_dir, output_filename=f'{feature_type}_vector')

