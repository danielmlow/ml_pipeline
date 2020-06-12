# Detecting suicidality from voice and text

Clone this directory:
'git clone ' 

download opensmile, unzip, and place in parallel dir to this one or change opensmile path in `preprocessing.py`.

path/to/suicidality_millner/
path/to/opensmile-2.3.0/

Recommended (optional): create a conda virtual environment for python3.7
```
conda create -n pydra python=3.7
conda activate pydra
 ```

`pip install pydra-ml`


## Preprocessing

add labels in `.data/input/labels.csv`. You'll see each name has a format (id-000_timestep-000_task_000) add audio files with the same format in the other directories (e.g., ./data/input/raw/audio/)

### Audio features

convert all files to .wav with 16k sampling rate. 
`python3 convert_to_wav`

Make sure all the wavs are finished. Then run: 

`python3 preprocessing.py`

This extract features to `./data/input/features/audio/`, which will then be merged with the labels.csv to `./data/input/egemaps_vector_labels.csv`

in `./data_example/` you'll how the files should be outputted. 


## Running models 
Run machine learning models (hyperparameter tuning)
 
To make sure pydraml is working well run:

`pydraml -s short-spec.json.sample` which will take as input the breast_cancer.csv dataset. See `https://github.com/nipype/pydra-ml` for more details. 

This will output a json file called `results` and feature importance in `shap/`.

Then create similar one for your data like in `machine_learning_config.json.sample`

---
### TODO: text features
```
pip install blabla

pip install stanford-corenlp
```
add to `document_processor.py` but change PATH
```
import os
os.environ["CORENLP_HOME"] = "/PATH/miniconda3/envs/pydra/lib/python3.7/site-packages/corenlp/"
```
