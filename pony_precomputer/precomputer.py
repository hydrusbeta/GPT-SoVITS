from .SlicedDialogParser import parse_filename
from .SlicedDialogEnums import Noise
from .SlicedDialogEnums import Character
from .SlicedDialogEnums import Emotion
from GPT_SoVITS.inference_webui import preprocess_reference_text, preprocess_reference_audios
import os

# Edit the variable top_folder to point at a folder containing Clipper's master files.
# Then, execute this script from the project root (GPT-SoVITS) as follows:
# python -m pony_precomputer.precomputer
# That will create a new folder named like "<top_folder> Precomp" with precomputed values organized by character and emotion.

# location of the directory containing all the raw audio files
top_folder = os.path.join(os.path.expanduser('~'), 'Desktop', 'Sliced Dialog')

# walk the directory and parse all audio files:
all_files = [item for sublist in [[{'fullPath': os.path.join(dir_path, name),
                                    'fileName': name,
                                    'metadata': parse_filename(name)}
                                   for name in file_names if (name[-4::] != '.txt') and (name[-4::] != '.zip')]
                                  for dir_path, dir_names, file_names in os.walk(top_folder)]
             for item in sublist]

available_characters = {Character.twilight, Character.trixie, Character.tirek, Character.sweetiebelle,
                        Character.starlight, Character.spike, Character.scootaloo, Character.rarity, Character.rainbow,
                        Character.pinkie, Character.octavia, Character.nightmaremoon, Character.meadowbrook,
                        Character.luna, Character.fluttershy, Character.flim, Character.flam, Character.discord,
                        Character.derpy, Character.cozyglow, Character.chrysalis, Character.celestia, Character.cadance,
                        Character.applejack, Character.applebloom}

output_folder = os.path.join(os.path.dirname(top_folder), os.path.basename(top_folder) + ' Precomp')
for character in available_characters:
    files_for_this_character = [item for item in all_files if
                                item['metadata']['noise'] == Noise.nothing and
                                item['metadata']['character'] == character]
    for emotion in Emotion:
        files_for_this_emotion = [item for item in files_for_this_character if emotion in item['metadata']['emotions']]
        if len(files_for_this_emotion) != 0:
            os.makedirs(os.path.join(output_folder, character.name, emotion.name), exist_ok=True)
            # let's just do the first one for now, as a proof-of-concept. # todo: In the future, loop through all files.
            file = files_for_this_emotion[0]
            phones1, bert1, ref_free = preprocess_reference_text(file['metadata']['transcript'], 'English', False, None, None)
            prompt, refers = preprocess_reference_audios(file['fullPath'], ref_free, None, None, None)
            print("phones1: ", phones1)
            print("prompt: ", prompt)
            print("refers: ", refers)
            # todo: Write phones1, prompt, refers, and maybe bert1 to a file. What's the preferred way to do that? Pickled dictionary? JSON?



