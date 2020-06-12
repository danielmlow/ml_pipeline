'''
Authors: Daniel M. Low (Harvard-MIT), Jim Schwoebel
license: Apache 2.0 license

'''



import os
import subprocess
import pandas as pd
import extract_opensmile

# ln -s "/Users/danielmlow/miniconda3/envs/pydra/lib/python3.7/site-packages/corenlp/" "CORENLP_HOME"

def to_wav(input_dir=None, filename=None, output_dir=None, output_filename=None, sampling_rate='16000', bit_rate='128k'):
	subprocess.Popen(['ffmpeg','-y','-i', input_dir + filename, '-ar', sampling_rate, '-ac', '1',
					  '-ab', bit_rate, output_dir + output_filename])

	return



if __name__ == "__main__":

	# Change as appropriate
	opensmile_dir = './../opensmile-2.3.0/'
	input_dir = './data/input/'

	# Audio
	wavs_dir = input_dir + 'raw/audio_converted_wavs/'
	output_audio_features = './data/input/features/audio/'
	audio_features = 'egemaps'
	functionals = True #take statistics (functionals) of timeseries and turn into vector
	sampling_rate = 16# thousand
	extract_audio_features = True

	# Main

	if functionals:
		audio_name = audio_features + '_vector'  # this is the type of feature being extracted to name dirs and files
	else:
		audio_name = audio_features + '_sequence'  # this is the type of feature being extracted to name dirs and files

	# Extract audio features
	if extract_audio_features:
		# make feature dir
		output_audio_features = output_audio_features+audio_name+'/'
		try: os.mkdir(output_audio_features )
		except: pass

		extract_opensmile.extract_features(feature_type=audio_features, funtionals=functionals,
		                                   input_dir=wavs_dir,output_dir=output_audio_features,
		                                   opensmile_dir =opensmile_dir )

		# concat all csvs (1 for each wav) to a single csv
		df_audio = extract_opensmile.opensmile_dir_to_csv(input_dir = output_audio_features , output_dir = output_audio_features+'../', output_filename = audio_name)


		# Create a final dataset with features and labels
		df_labels = pd.read_csv(input_dir + 'labels.csv')
		df_audio_labels = df_labels.merge(df_audio)
		df_audio_labels.to_csv(input_dir+audio_name+'_labels.csv')

	#


	'''
	Todo:
	files_text = os.listdir(input_raw_text_dir)
	# Extract text features
	if extract_text_features:
		from blabla.document_processor import DocumentProcessor
		import os
		os.environ["CORENLP_HOME"] = "/path/to/miniconda3/envs/pydra/lib/python3.7/site-packages/corenlp/"

		command = "blabla compute-features -F features.yaml -S stanza_config.yaml -i ~/path/to/txt/dir. -o blabla_features.csv -format string"
		subprocess.Popen(command.split())




	
	'''