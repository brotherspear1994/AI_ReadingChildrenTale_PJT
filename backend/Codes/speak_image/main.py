import os
from Speak_Image import speak_image


S = speak_image()
#path for saving wav files
output_path = "/home/multicam/multicam_project/multicam/web/static/"

# load and caption a image 
S.load_image() 
S.caption_image() 
print(S.captions_list)

S.select_caption() # select a single caption
print(S.caption)
print("caption done\n\n")

# caption text -> tacotron voice
S.text_to_speech(output_path+'/src_voice.wav')
print("tts done\n\n")


# tacotron voice -> converted voice
S.load_voice()
S.convert_voice(output_path+'/tar_voice.wav')
print("conversion done\n\n")

