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
