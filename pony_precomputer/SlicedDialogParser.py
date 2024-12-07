from typing import TypeVar, Type, List, Dict
from pony_precomputer.SlicedDialogEnums import Character, Emotion, Noise, BaseEnum

BE = TypeVar('BE', bound=BaseEnum)  # for function annotations


def parse_enumeration(member: str, enum: Type[BE]) -> Type[BE]:
    """Remove characters that are not allowed in Enums and then call enum.create()"""
    modified_member = member.lower()  # 'Mrs. Cake' -> 'mrs. cake'
    modified_member = modified_member.replace(' ', '')  # 'mrs. cake' -> 'mrs.cake'
    modified_member = modified_member.replace('.', '')  # 'mrs.cake' -> mrscake
    modified_member = modified_member.replace('-', '')  # 'mane-iac' -> maniac
    return enum.create(modified_member)


def parse_character(character: str) -> Type[Character]:
    return parse_enumeration(character, Character)


def parse_emotions(emotions_group: str) -> List[Type[Emotion]]:
    emotions_group = emotions_group.replace('Canterlot Voice', 'CanterlotVoice')  # "Canterlot Voice" is 1 emotion
    emotions = emotions_group.split(' ')
    return [parse_enumeration(emotion, Emotion) for emotion in emotions]


def parse_noise(noise: str) -> Type[Noise]:
    if not noise:
        noise = 'nothing'
    return parse_enumeration(noise, Noise)


def parse_transcript(transcript: str) -> str:
    # question marks are not allowed in filenames, so they were apparently replaced with underscores. Change them back.
    return transcript.replace('_', '?')


def parse_filename(filename: str) -> Dict:
    filename, _, extension = filename.rpartition('.')
    hour, minute, second, character, emotions_group, noise, transcript = filename.split('_', maxsplit=6)
    return {'hour': int(hour),
            'minute': int(minute),
            'second': int(second),
            'character': parse_character(character),
            'emotions': parse_emotions(emotions_group),
            'noise': parse_noise(noise),
            'transcript': parse_transcript(transcript),
            'extension': extension
            }


# This method is not needed. You can parse the audio file name to get an identical transcript, and it's way faster.
# I compared the output of this method against the output of parse_transcript for all Noise.nothing s1-s9 and Rainbow
# Roadtrip files on 11/29/2024 and the results were identical in 100% of cases. I'm keeping this method around to
# remind myself that I
# already checked this.
# import os.path
# def get_transcript(dir_path: str, filename: str) -> str:
#     filename_sans_extension = os.path.splitext(os.path.splitext(filename)[0])[0]  # eliminate .flac and ..flac
#     candidates = [item for item in os.listdir(dir_path) if filename_sans_extension in item and os.path.splitext(item)[1] == '.txt']
#     if not candidates:
#         raise Exception(f"ERROR! Unable to find transcript for {os.path.join(dir_path, filename)}")
#     if len(candidates) > 1:
#         raise Exception(f"ERROR! There is more than one transcript file for {os.path.join(dir_path, filename)}")
#     transcript_file_path = os.path.join(dir_path, candidates[0])
#     with open(transcript_file_path, 'r') as file:
#         contents = file.read()
#     if '\n' in contents:
#         print(f"WARNING! file {transcript_file_path} contains newlines.")
#     if not contents.strip():
#         print(f"WARNING! file {transcript_file_path} is empty.")
#     return contents
