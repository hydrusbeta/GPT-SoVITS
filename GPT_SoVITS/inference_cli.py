import argparse
import os
from tempfile import NamedTemporaryFile

import soundfile as sf
from safetensors import safe_open

from .inference_webui import change_gpt_weights, change_sovits_weights, get_tts_wav, device, get_prefix
from .tools.i18n.i18n import I18nAuto

# Invoke this script from the project root (GPT-SoVITS) using a terminal/command prompt as follows:
# python -m GPT_SoVITS.inference_cli [options]

i18n = I18nAuto()


def synthesize(GPT_model_path, SoVITS_model_path, precomputed_traits_file, ref_audio_path, ref_text_path, ref_language,
               target_text_path, target_language, output_path, how_to_cut, top_k, top_p, temperature, ref_free, speed,
               additional_inp_refs, precomputed_trait):

    if precomputed_traits_file:
        ref_audio_path, ref_text = None, None
        with safe_open(precomputed_traits_file, framework="pt") as f:
            count = len([item for item in f.keys() if item.startswith(precomputed_trait) and item.endswith('phones1')])
            print(f"number of datapoints available for {precomputed_trait}: {count}", flush=True)
            phones1 = f.get_tensor(get_prefix(precomputed_trait, 0) + "phones1")
            prompt = f.get_tensor(get_prefix(precomputed_trait, 0) + "prompt").to(device)
            ge = f.get_tensor(get_prefix(precomputed_trait, 0) + "ge").to(device)
            bert1 = f.get_tensor(get_prefix(precomputed_trait, 0) + "bert1").to(device) if "bert1" in f.keys() else None
    else:
        print(f"No precomputed trait was supplied. Using reference audio.", flush=True)
        phones1, prompt, ge, bert1 = None, None, None, None
        # Read reference text
        with open(ref_text_path, 'r', encoding='utf-8') as file:
            ref_text = file.read()

    # Gradio prepares a list of NamedTemporaryFile objects for the additional reference audio files uploaded to the UI.
    # get_tts_wav expects the additional reference audio files to be supplied in this way, so, for compatibility, the
    # CLI must also wrap the specified file paths in NamedTemporaryFile objects.
    def make_tempfile(file_path):
        temp_file = NamedTemporaryFile(delete=False)
        temp_file.name = file_path
        return temp_file
    additional_inputs = [make_tempfile(file_path) for file_path in additional_inp_refs] if additional_inp_refs else None

    # Read target text
    with open(target_text_path, 'r', encoding='utf-8') as file:
        target_text = file.read()

    # Change model weights
    change_gpt_weights(gpt_path=GPT_model_path)
    change_sovits_weights(sovits_path=SoVITS_model_path)

    # Synthesize audio
    synthesis_result = get_tts_wav(ref_wav_path=ref_audio_path,
                                   ref_text=ref_text,
                                   ref_language=i18n(ref_language),
                                   prompt_text=target_text,
                                   prompt_language=i18n(target_language),
                                   how_to_cut=how_to_cut,
                                   top_k=top_k,
                                   top_p=top_p,
                                   temperature=temperature,
                                   ref_free=ref_free,
                                   speed=speed,
                                   inp_refs=additional_inputs,
                                   precomputed_prompt=prompt,
                                   precomputed_phones1=phones1,
                                   precomputed_bert1=bert1,
                                   precomputed_ge=ge)

    result_list = list(synthesis_result)

    if result_list:
        last_sampling_rate, last_audio_data = result_list[-1]
        output_wav_path = os.path.join(output_path, "output.wav")
        sf.write(output_wav_path, last_audio_data, last_sampling_rate)
        print(f"Audio saved to {output_wav_path}")


def main():
    parser = argparse.ArgumentParser(description="GPT-SoVITS Command Line Tool")
    parser.add_argument('--gpt_model', required=True, help="Path to the GPT model file")
    parser.add_argument('--sovits_model', required=True, help="Path to the SoVITS model file")
    parser.add_argument('--precomputed_traits_file', required=True, help="Path to the SoVITS model file")
    parser.add_argument('--ref_audio', help="Path to the reference audio file")
    parser.add_argument('--ref_text', help="Path to the reference text file")
    parser.add_argument('--ref_language', required=True, choices=["中文", "英文", "日文", "粤语", "韩文", "中英混合", "日英混合", "粤英混合", "韩英混合", "多语种混合", "多语种混合(粤语)"], help="Language of the reference audio")
    parser.add_argument('--target_text', required=True, help="Path to the target text file")
    parser.add_argument('--target_language', required=True, choices=["中文", "英文", "日文", "粤语", "韩文", "中英混合", "日英混合", "粤英混合", "韩英混合", "多语种混合", "多语种混合(粤语)"], help="Language of the target text")
    parser.add_argument('--output_path', required=True, help="Path to the output directory, where generated audio files will be saved.")
    parser.add_argument('--speed', type=float, default=1.0, help="Adjusts the speed of the generated audio without changing its pitch. Higher numbers = faster.")
    parser.add_argument('--how_to_cut', default="凑四句一切", choices=["不切", "凑四句一切", "凑50字一切", "按中文句号。切", "按英文句号.切", "按标点符号切"], help="The desired strategy for slicing up the prompt text. Audio will be generated for each slice and then concatenated together.")
    parser.add_argument('--top_k', type=int, default=15, help="Parameter for top-K filtering")
    parser.add_argument('--top_p', type=float, default=1.0, help="Parameter for nucleus filtering")
    parser.add_argument('--temperature', type=float, default=1.0, help="Inverse scale factor for the logits. Temperatures between 0 and 1.0 produce audio that sounds more like the speaker in the reference audio but may introduce pronunciation errors. Temperature > 1.0 tends to fix pronunciation but sounds less like the speaker.")
    parser.add_argument('--ref_free', action='store_true', default=False, help="Instructs the application to ignore the reference audio transcript.")
    parser.add_argument('--precomputed_trait', help='Use precomputed values associated with this trait instead of using a reference audio.')
    parser.add_argument('--additional_inp_refs', nargs='*', help='Paths to additional reference audio files. The average "Tone" of these files will guide the tone of the generated audio. If none are provided, then ref_audio will be used instead.')

    args = parser.parse_args()

    if args.precomputed_trait and (args.ref_audio or args.ref_text):
        parser.error('You must specify either just --precomputed_trait or both --ref_audio and --ref_text')
    if (args.ref_audio or args.ref_text) and not (args.ref_audio and args.ref_text):
        parser.error('If you specify either of --ref_audio or --ref_text, then you must specify both of them')
    if args.precomputed_trait and not args.precomputed_traits_file:
        parser.error('If you specify --precomputed_trait, then you must also specify --precomputed_traits_file')

    synthesize(args.gpt_model, args.sovits_model, args.precomputed_traits_file, args.ref_audio, args.ref_text, args.ref_language,
               args.target_text, args.target_language, args.output_path, args.how_to_cut, args.top_k, args.top_p,
               args.temperature, args.ref_free, args.speed, args.additional_inp_refs, args.precomputed_trait)


if __name__ == '__main__':
    main()

