'''
Authors: Daniel M. Low (Harvard-MIT)
license: Apache 2.0 license

'''

import os
import subprocess


# ln -s "/Users/danielmlow/miniconda3/envs/pydra/lib/python3.7/site-packages/corenlp/" "CORENLP_HOME"

def to_wav(input_dir=None, filename=None, output_dir=None, output_filename=None, sampling_rate='16000',
           bit_rate='128k'):
	subprocess.Popen(['ffmpeg', '-y','-i', input_dir + filename, '-ar', sampling_rate, '-ac', '1',
	                  '-ab', bit_rate, output_dir + output_filename])

	return


if __name__ == "__main__":

	# Change as appropriate
	input_dir = './data/input/'
	input_raw_audio_dir = './data/input/raw/audio/'  # within input_dir
	convert_to_wav_dir = input_raw_audio_dir + '../audio_converted_wavs/' #output dir
	sampling_rate = 16  # thousand

	# Convert to wav
	files_audio = os.listdir(input_raw_audio_dir)

	try:
		os.mkdir(convert_to_wav_dir)
	except:
		pass
	for filename in files_audio:
		if filename.endswith('.wav'):
			print(filename)
			to_wav(input_dir=input_raw_audio_dir, filename=filename, output_dir=convert_to_wav_dir,
			       output_filename=filename[:-4] + '.wav',
			       sampling_rate=f'{sampling_rate}000', bit_rate='128k')

