import unittest
from pony_precomputer.SlicedDialogEnums import Character, Emotion, Noise
from pony_precomputer.SlicedDialogParser import parse_filename


class TestSlicedDialogParser(unittest.TestCase):

    def setUp(self) -> None:
        self.tests_strings_and_expected_results = [
            # a typical file name
            ('00_03_56_Rainbow_Neutral_Very Noisy_Then, I would mesmerize them With my fantastic filly flash!.flac',
             {'hour': 0,
              'minute': 3,
              'second': 56,
              'character': Character.rainbow,
              'emotions': [Emotion.neutral],
              'noise': Noise.verynoisy,
              'transcript': 'Then, I would mesmerize them With my fantastic filly flash!',
              'extension': 'flac'}
             ),
            # contains a quote character
            ('00_00_17_Twilight_Neutral_Noisy_I\'m glad the goal is lunchtime.flac',
             {'hour': 0,
              'minute': 0,
              'second': 17,
              'character': Character.twilight,
              'emotions': [Emotion.neutral],
              'noise': Noise.noisy,
              'transcript': 'I\'m glad the goal is lunchtime',
              'extension': 'flac'}
             ),
            # underscore (question mark) at the end
            ('00_05_00_Twilight_Neutral__Don\'t you think_.flac',
             {'hour': 0,
              'minute': 5,
              'second': 0,
              'character': Character.twilight,
              'emotions': [Emotion.neutral],
              'noise': Noise.nothing,
              'transcript': 'Don\'t you think?',
              'extension': 'flac'}
             ),
            # unrecognized emotion name
            ('00_05_00_Twilight_humanlike__Don\'t you think_.flac',
             {'hour': 0,
              'minute': 5,
              'second': 0,
              'character': Character.twilight,
              'emotions': [Emotion.unknown],
              'noise': Noise.nothing,
              'transcript': 'Don\'t you think?',
              'extension': 'flac'}
             ),
            # unrecognized noise name
            ('00_05_00_Twilight_Neutral_Super Noisy_Don\'t you think_.flac',
             {'hour': 0,
              'minute': 5,
              'second': 0,
              'character': Character.twilight,
              'emotions': [Emotion.neutral],
              'noise': Noise.unknown,
              'transcript': 'Don\'t you think?',
              'extension': 'flac'}
             ),
            # unrecognized character name
            ('00_05_00_Twilot_Neutral__Don\'t you think_.flac',
             {'hour': 0,
              'minute': 5,
              'second': 0,
              'character': Character.unknown,
              'emotions': [Emotion.neutral],
              'noise': Noise.nothing,
              'transcript': 'Don\'t you think?',
              'extension': 'flac'}
             ),
            # space in character name
            ('00_05_00_Photo Finish_Neutral__da magicks!.flac',
             {'hour': 0,
              'minute': 5,
              'second': 0,
              'character': Character.photofinish,
              'emotions': [Emotion.neutral],
              'noise': Noise.nothing,
              'transcript': 'da magicks!',
              'extension': 'flac'}
             ),
            # hyphen in character name
            ('10_15_10_Mane-iac_Crazy__Behold!.flac',
             {'hour': 10,
              'minute': 15,
              'second': 10,
              'character': Character.maneiac,
              'emotions': [Emotion.crazy],
              'noise': Noise.nothing,
              'transcript': 'Behold!',
              'extension': 'flac'}
             ),
            # dot in character name
            ('00_00_13_Mrs. Cake_Happy_Noisy_Oh, thank you, Pinkie!.flac',
             {'hour': 0,
              'minute': 0,
              'second': 13,
              'character': Character.mrscake,
              'emotions': [Emotion.happy],
              'noise': Noise.noisy,
              'transcript': 'Oh, thank you, Pinkie!',
              'extension': 'flac'}
             ),
            # more than one emotion
            ('00_03_56_Rainbow_Smug Shouting_Very Noisy_Then, I would mesmerize them With my fantastic filly flash!.flac',
             {'hour': 0,
              'minute': 3,
              'second': 56,
              'character': Character.rainbow,
              'emotions': [Emotion.smug, Emotion.shouting],
              'noise': Noise.verynoisy,
              'transcript': 'Then, I would mesmerize them With my fantastic filly flash!',
              'extension': 'flac'}
             ),
            # 'Canterlot Voice' is *one* emotion, not two. Requires special-case processing due to the space.
            ('00_11_38_Luna_Canterlot Voice_Noisy_Nay, children! wait!.flac',
             {'hour': 0,
              'minute': 11,
              'second': 38,
              'character': Character.luna,
              'emotions': [Emotion.canterlotvoice],
              'noise': Noise.noisy,
              'transcript': 'Nay, children! wait!',
              'extension': 'flac'}
             ),
            # 'Canterlot Voice' with another emotion
            ('00_11_38_Luna_Canterlot Voice angry_Noisy_Nay, children! wait!.flac',
             {'hour': 0,
              'minute': 11,
              'second': 38,
              'character': Character.luna,
              'emotions': [Emotion.canterlotvoice, Emotion.angry],
              'noise': Noise.noisy,
              'transcript': 'Nay, children! wait!',
              'extension': 'flac'}
             )
        ]

    def test_parse_filename(self):
        for test_string, expected_result in self.tests_strings_and_expected_results:
            with self.subTest(test_string):
                self.assertEqual(parse_filename(test_string), expected_result)


if __name__ == '__main__':
    unittest.main()
