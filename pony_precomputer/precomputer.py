import os
from typing import List

import soundfile
from safetensors import safe_open
from safetensors.torch import save_file

from GPT_SoVITS.inference_webui import change_gpt_weights, change_sovits_weights, preprocess_reference_text, \
    preprocess_reference_audios, get_tts_wav, device, LANGUAGES_REQUIRING_BERT
from .SlicedDialogEnums import Character
from .SlicedDialogEnums import Emotion
from .SlicedDialogEnums import Noise
from .SlicedDialogParser import parse_filename

# 1. Edit the variable ref_audio_folder to point at a local folder containing Clipper's master files.
# 2. Edit the variable model_folder if you saved the models somewhere other than the pretrained_models directory
# 3. Execute this script from the project root (GPT-SoVITS) as follows:
#    python -m pony_precomputer.precomputer
# 4. That will create a new folder named like "<ref_audio_folder> Precomp" with precomputed values organized by character and emotion.
# 5. A sample script at the bottom of this page shows how you can use the safetensors file to generate audio.

# directory containing all the reference audio files
ref_audio_folder = os.path.join(os.path.expanduser('~'), 'Desktop', 'Sliced Dialog')

# directory containing all character model files (.ckpt and .pth).
# The files may be arranged in subfolders in any way, just as long as they're all somewhere within this folder.
model_folder = os.path.join(os.getcwd(), 'GPT_SoVITS', 'pretrained_models')

# All pony references are in English
ref_language = 'English'

def find_all_files_with_name(file_name: str, directory: str) -> List[str]:
    return [os.path.join(dir_path, name)
            for dir_path, dir_names, file_names in os.walk(directory)
            for name in file_names
            if name == file_name]


def find_exactly_one_file_with_name(file_name: str, directory: str) -> str:
    matches = find_all_files_with_name(file_name, directory)
    if not matches:
        raise Exception(f'No file named {file_name} exists in {directory}')
    if len(matches) > 1:
        raise Exception(f'Found more than one file named {file_name} in {directory}: ' + '; '.join(matches))
    return matches[0]


def get_character_model_files(character: Character, directory: str) -> tuple[str, str]:
    gpt_model_file = find_exactly_one_file_with_name(available_characters[character]["GPT Model"], directory)
    sovits_model_file = find_exactly_one_file_with_name(available_characters[character]["SoVITS Model"], directory)
    return gpt_model_file, sovits_model_file


def save_to_safetensors(phones1, prompt, ge, bert1, ref_language, precomp_out_path):
    precomputed_data = {
        "phones1": phones1,
        "prompt": prompt,
        "ge": ge,
    }
    # bert1 is by far the largest piece of data, so leave it out unless the language requires it.
    if ref_language in LANGUAGES_REQUIRING_BERT:
        precomputed_data["bert1"] = bert1
    save_file(precomputed_data, precomp_out_path)


available_characters = {
    Character.twilight: {"GPT Model": "Twilight-e24.ckpt", "SoVITS Model": "Twilight_e96_s46464.pth"},
    Character.trixie: {"GPT Model": "Trixie-e8.ckpt", "SoVITS Model": "Trixie_e24_s1368.pth"},
    Character.tirek: {"GPT Model": "Tirek-e32.ckpt", "SoVITS Model": "Tirek_e32_s608.pth"},
    Character.sweetiebelle: {"GPT Model": "Sweetie Belle-e24.ckpt", "SoVITS Model": "Sweetie Belle_e96_s7296.pth"},
    Character.starlight: {"GPT Model": "Starlight-e24.ckpt", "SoVITS Model": "Starlight_e96_s11712.pth"},
    Character.spike: {"GPT Model": "Spike-e8.ckpt", "SoVITS Model": "Spike_e24_s4848.pth"},
    Character.scootaloo: {"GPT Model": "Scootaloo-e24.ckpt", "SoVITS Model": "Scootaloo_e96_s7872.pth"},
    Character.rarity: {"GPT Model": "Rarity-e24.ckpt", "SoVITS Model": "Rarity_e96_s25824.pth"},
    Character.rainbow: {"GPT Model": "Rainbow-e24.ckpt", "SoVITS Model": "Rainbow_e96_s26592.pth"},
    Character.princeblueblood: {"GPT Model": "Blueblood1-e40.ckpt", "SoVITS Model": "Blueblood1_e32_s224.pth"},
    Character.pinkie: {"GPT Model": "Pinkie-e24.ckpt", "SoVITS Model": "Pinkie_e96_s24480.pth"},
    Character.octavia: {"GPT Model": "Octavia-e48.ckpt", "SoVITS Model": "Octavia_e84_s588.pth"},
    Character.nightmaremoon: {"GPT Model": "NightmareMoon-e32.ckpt", "SoVITS Model": "NightmareMoon_e96_s576.pth"},
    Character.meadowbrook: {"GPT Model": "Meadowbrook-e48.ckpt", "SoVITS Model": "Meadowbrook_e24_s168.pth"},
    Character.luna: {"GPT Model": "Luna-e36.ckpt", "SoVITS Model": "Luna_e96_s2688.pth"},
    Character.fluttershy: {"GPT Model": "Fluttershy-e24.ckpt", "SoVITS Model": "Fluttershy_e96_s18912.pth"},
    Character.flim: {"GPT Model": "Flim-e36.ckpt", "SoVITS Model": "Flim_e96_s1152.pth"},
    Character.flam: {"GPT Model": "Flam-e48.ckpt", "SoVITS Model": "Flam_e96_s1248.pth"},
    Character.discord: {"GPT Model": "Discord-e48.ckpt", "SoVITS Model": "Discord_e96_s6432.pth"},
    Character.derpy: {"GPT Model": "Derpy-e48.ckpt", "SoVITS Model": "Derpy_e36_s288.pth"},
    Character.cozyglow: {"GPT Model": "Cozy Glow-e48.ckpt", "SoVITS Model": "Cozy Glow_e48_s1104.pth"},
    Character.chrysalis: {"GPT Model": "Chrysalis-e8.ckpt", "SoVITS Model": "Chrysalis_e32_s608.pth"},
    Character.celestia: {"GPT Model": "Celestia-e24.ckpt", "SoVITS Model": "Celestia_e96_s5376.pth"},
    Character.cadance: {"GPT Model": "Cadance-e24.ckpt", "SoVITS Model": "Cadance_e96_s1824.pth"},
    Character.applejack: {"GPT Model": "Applejack-e24.ckpt", "SoVITS Model": "Applejack_e96_s28224.pth"},
    Character.applebloom: {"GPT Model": "Apple Bloom-e24.ckpt", "SoVITS Model": "Apple Bloom_e96_s12000.pth"}
}

# walk the directory and parse all audio files:
all_files = [item for sublist in [[{'fullPath': os.path.join(dir_path, name),
                                    'fileName': name,
                                    'metadata': parse_filename(name)}
                                   for name in file_names if (name[-4::] != '.txt') and (name[-4::] != '.zip')]
                                  for dir_path, dir_names, file_names in os.walk(ref_audio_folder)]
             for item in sublist]


# precompute phones1, bert1, prompt, and ge by character and emotion
output_folder = os.path.join(os.path.dirname(ref_audio_folder), os.path.basename(ref_audio_folder) + ' Precomp')
for character in available_characters.keys():
    gpt_model_file, sovits_model_file = get_character_model_files(character, model_folder)
    change_gpt_weights(gpt_model_file)
    change_sovits_weights(sovits_model_file)
    files_for_this_character = [item for item in all_files if
                                item['metadata']['noise'] == Noise.nothing and
                                item['metadata']['character'] == character]
    for emotion in Emotion:
        files_for_this_emotion = [item for item in files_for_this_character if emotion in item['metadata']['emotions']]
        if len(files_for_this_emotion) != 0:
            directory = os.path.join(output_folder, character.name, emotion.name)
            os.makedirs(directory, exist_ok=True)
            for file in files_for_this_emotion:
                phones1, bert1, ref_free = preprocess_reference_text(file['metadata']['transcript'], ref_language, False, None, None)
                prompt, ge = preprocess_reference_audios(file['fullPath'], ref_free, None, None, None)
                precomp_out_path = os.path.join(directory, os.path.splitext(file['fileName'])[0] + '.safetensors')
                save_to_safetensors(phones1, prompt, ge, bert1, ref_language, precomp_out_path)






# Here's an example of how to use the safetensors file. It will save a file named output.wav on your Desktop.
# For this example, let's just grab the first safetensor of Rainbow Dash with a Neutral emotion
run_example = False  # Set this to true if you want to run the example.
if run_example:
    neutral_rainbow_dir = os.path.join(output_folder, Character.rainbow.name, Emotion.neutral.name)
    safetensors_file_path = os.path.join(neutral_rainbow_dir, os.listdir(neutral_rainbow_dir)[0])
    print(safetensors_file_path)
    with safe_open(safetensors_file_path, framework="pt") as f:
        phones1 = f.get_tensor("phones1")
        prompt = f.get_tensor("prompt").to(device)
        ge = f.get_tensor("ge").to(device)
        bert1 = f.get_tensor("bert1").to(device) if "bert1" in f.keys() else None
    # Instead of passing a ref_wav_path and ref_text, we can pass the precomputed values instead:
    synthesis_result = get_tts_wav(ref_wav_path=None,
                                   ref_text=None,
                                   ref_language='English',
                                   prompt_text="There's no way they'd shut it down. The weather factory has to keep running.",
                                   prompt_language='English',
                                   how_to_cut='凑四句一切',
                                   top_k=15,
                                   top_p=1.0,
                                   temperature=1.0,
                                   speed=1.0,
                                   precomputed_prompt=prompt,
                                   precomputed_phones1=phones1,
                                   precomputed_bert1=bert1,
                                   precomputed_ge=ge
                                   )

    result_list = list(synthesis_result)

    if result_list:
        last_sampling_rate, last_audio_data = result_list[-1]
        output_wav_path = os.path.join(os.path.expanduser('~'), 'Desktop', "output.wav")
        soundfile.write(output_wav_path, last_audio_data, last_sampling_rate)
        print(f"Audio saved to {output_wav_path}")

