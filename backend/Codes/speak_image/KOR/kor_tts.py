import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)) + '/KOR/')

import torch
import torch.nn as nn
import numpy as np
import hparams as hp
import os

os.environ["CUDA_DEVICE_ORDER"]="PCI_BUS_ID"
os.environ["CUDA_VISIBLE_DEVICES"]=hp.train_visible_devices

import argparse
import re
from string import punctuation

from fastspeech2 import FastSpeech2
from vocoder import vocgan_generator

from text2 import text_to_sequence, sequence_to_text
import utils3
import audio as Audio

import codecs
from g2pk import G2p
from jamo import h2j

from synthesize import kor_preprocess, get_FastSpeech2, synthesize

device = torch.device('cpu')

class KOR_Model:
    def __init__(self):
        self.model = get_FastSpeech2(200000).to(device)
        self.vocoder = utils3.get_vocgan(ckpt_path=hp.vocoder_pretrained_model_path)


    def inference(self, sentence, output_path):
        text = kor_preprocess(sentence)
        #synthesize(self.model, self.vocoder, text, sentence, prefix='step_{}'.format(200000))
        sentence = sentence[:10]
        mean_mel, std_mel = torch.tensor(np.load(os.path.join(hp.preprocessed_path, "mel_stat.npy")), dtype=torch.float).to(device)
        mean_f0, std_f0 = torch.tensor(np.load(os.path.join(hp.preprocessed_path, "f0_stat.npy")), dtype=torch.float).to(device)
        mean_energy, std_energy = torch.tensor(np.load(os.path.join(hp.preprocessed_path, "energy_stat.npy")), dtype=torch.float).to(device)

        mean_mel, std_mel = mean_mel.reshape(1, -1), std_mel.reshape(1, -1)
        mean_f0, std_f0 = mean_f0.reshape(1, -1), std_f0.reshape(1, -1)
        mean_energy, std_energy = mean_energy.reshape(1, -1), std_energy.reshape(1, -1)

        src_len = torch.from_numpy(np.array([text.shape[1]])).to(device)
        
        mel, mel_postnet, log_duration_output, f0_output, energy_output, _, _, mel_len = self.model(text, src_len)
    
        mel_torch = mel.transpose(1, 2).detach() 
        mel_postnet_torch = mel_postnet.transpose(1, 2).detach()
        f0_output = f0_output[0]
        energy_output = energy_output[0]

        mel_torch = utils3.de_norm(mel_torch.transpose(1, 2), mean_mel, std_mel)
        mel_postnet_torch = utils3.de_norm(mel_postnet_torch.transpose(1, 2), mean_mel, std_mel).transpose(1, 2)
        f0_output = utils3.de_norm(f0_output, mean_f0, std_f0).squeeze().detach().cpu().numpy()
        energy_output = utils3.de_norm(energy_output, mean_energy, std_energy).squeeze().detach().cpu().numpy()

        if not os.path.exists(hp.test_path):
            os.makedirs(hp.test_path)

        #Audio.tools.inv_mel_spec(mel_postnet_torch[0], os.path.join(output_path, '{}_griffin_lim_{}.wav'.format('step_{}'.format(200000), sentence)))

        if self.vocoder is not None:
            if hp.vocoder.lower() == "vocgan":
                utils3.vocgan_infer(mel_postnet_torch, self.vocoder, path=os.path.join(output_path, '{}_{}_{}.wav'.format('step_{}'.format(200000), hp.vocoder, sentence)))   
    
        #utils3.plot_data([(mel_postnet_torch[0].detach().cpu().numpy(), f0_output, energy_output)], ['Synthesized Spectrogram'], filename=os.path.join(output_path, '{}_{}.png'.format('step_{}'.format(200000), sentence)))
        return os.path.join(output_path, '{}_{}_{}.wav'.format('step_{}'.format(200000), hp.vocoder, sentence))


if __name__ == '__main__':
    kor_model = KOR_Model()

    sentence ="오늘도 모두가 행복합니다아아아 집이 그립읍니다"
    kor_model.inference(sentence, "temp")


