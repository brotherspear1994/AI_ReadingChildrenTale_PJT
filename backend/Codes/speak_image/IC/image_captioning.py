import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__))+'/IC/vqa_origin')
sys.path.append(os.path.dirname(os.path.dirname(__file__))+'/IC/')
sys.path.append(os.path.dirname(os.path.dirname(__file__))+'./vqa_origin')
import yaml
import cv2
import torch
import requests
import numpy as np
import gc
import torch.nn.functional as F


import torchvision.models as models
import torchvision.transforms as transforms

from PIL import Image
from io import BytesIO


from maskrcnn_benchmark.config import cfg
from maskrcnn_benchmark.layers import nms
from maskrcnn_benchmark.modeling.detector import build_detection_model
from maskrcnn_benchmark.structures.image_list import to_image_list
from maskrcnn_benchmark.utils.model_serialization import load_state_dict

#model for captioning
import captioning
import captioning.utils.misc
import captioning.models
# 경로설정을 위한 import
from os.path import dirname
from os.path import abspath

#Req. 3-2 클래스 이해
class FeatureExtractor:
  TARGET_IMAGE_SIZE = [448, 448]
  CHANNEL_MEAN = [0.485, 0.456, 0.406]
  CHANNEL_STD = [0.229, 0.224, 0.225]
  
  def __init__(self):
    # self._init_processors()
    self.base_dir = os.path.dirname(os.path.dirname(__file__))
    self.detection_model = self._build_detection_model()
  
  def __call__(self, url):
    with torch.no_grad():
      detectron_features = self.get_detectron_features(url)
    
    return detectron_features
  
  def _build_detection_model(self):

      # detectron_model.yaml의 주소
      # cfg.merge_from_file('/home/multicam/multicam_project/speak_image/IC/model_data/detectron_model.yaml')
      cfg.merge_from_file('/home/ubuntu/test/backend/Codes/speak_image/IC/model_data/detectron_model.yaml')
      cfg.freeze()

      model = build_detection_model(cfg)
      # detectron_model.pth의 주소
    #   checkpoint = torch.load('C:\\Users\\multicampus\\subproject3\\backend\\Codes\\checkpoints\\detectron_model.pth',
    #                           map_location=torch.device("cuda"))
      checkpoint = torch.load('/home/ubuntu/test/IC/detectron_model.pth',
                              map_location=torch.device("cpu"))
      load_state_dict(model, checkpoint.pop("model"))

      model.to("cpu")
      model.eval()
      return model
  
  def get_actual_image(self, image_path):
      # image path 우리 프로젝트에 맞게 조정 필요.
      if image_path.startswith('http'):
          path_sub = requests.get(image_path, stream=True).raw
      else:
          path_sub = image_path
        # 상위 폴더 상대경로 지정
      print(path_sub)
      upper = dirname(abspath(dirname(abspath(dirname(abspath(dirname(__file__)))))))
      path = upper+path_sub
    #   path = os.path.dirname(os.path.realpath(__file__)) + '\\checkpoints\\model-best.pth')  
      return path

  def _image_transform(self, image_path):
      path = self.get_actual_image(image_path)
      img = Image.open(path)
      im = np.array(img).astype(np.float32)
      im = im[:, :, ::-1]
      im -= np.array([102.9801, 115.9465, 122.7717])
      im_shape = im.shape
      im_size_min = np.min(im_shape[0:2])
      im_size_max = np.max(im_shape[0:2])
      im_scale = float(800) / float(im_size_min)
      # Prevent the biggest axis from being more than max_size
      if np.round(im_scale * im_size_max) > 1333:
           im_scale = float(1333) / float(im_size_max)
      im = cv2.resize(
           im,
           None,
           None,
           fx=im_scale,
           fy=im_scale,
           interpolation=cv2.INTER_LINEAR
       )
      img = torch.from_numpy(im).permute(2, 0, 1)
      return img, im_scale


  def _process_feature_extraction(self, output,
                                 im_scales,
                                 feat_name='fc6',
                                 conf_thresh=0.2):
      batch_size = len(output[0]["proposals"])
      n_boxes_per_image = [len(_) for _ in output[0]["proposals"]]
      score_list = output[0]["scores"].split(n_boxes_per_image)
      score_list = [torch.nn.functional.softmax(x, -1) for x in score_list]
      feats = output[0][feat_name].split(n_boxes_per_image)
      cur_device = score_list[0].device

      feat_list = []

      for i in range(batch_size):
          dets = output[0]["proposals"][i].bbox / im_scales[i]
          scores = score_list[i]

          max_conf = torch.zeros((scores.shape[0])).to(cur_device)

          for cls_ind in range(1, scores.shape[1]):
              cls_scores = scores[:, cls_ind]
              keep = nms(dets, cls_scores, 0.5)
              max_conf[keep] = torch.where(cls_scores[keep] > max_conf[keep],
                                           cls_scores[keep],
                                           max_conf[keep])

          keep_boxes = torch.argsort(max_conf, descending=True)[:100]
          feat_list.append(feats[i][keep_boxes])
      return feat_list

  def get_detectron_features(self, image_path):
      im, im_scale = self._image_transform(image_path)
      img_tensor, im_scales = [im], [im_scale]
      current_img_list = to_image_list(img_tensor, size_divisible=32)
      current_img_list = current_img_list.to('cpu')
      with torch.no_grad():
          output = self.detection_model(current_img_list)
      feat_list = self._process_feature_extraction(output, im_scales, 
                                                  'fc6', 0.2)
      return feat_list[0]

#Req. 3-2 클래스 이해 
class Caption_Model:
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.dirname(__file__))
        self.feature_extractor = FeatureExtractor()
        self.load_model()
        
    def load_model(self):
        # infos_trans12-best.pkl의 주소
        # infos = captioning.utils.misc.pickle_load(open('C:\\Users\\multicampus\\subproject3\\backend\\Codes\\checkpoints\\infos_trans12-best.pkl', 'rb'))
        infos = captioning.utils.misc.pickle_load(open('/home/ubuntu/test/IC/infos_trans12-best.pkl', 'rb'))
        infos['opt'].vocab = infos['vocab']
    
        self.model = captioning.models.setup(infos['opt'])
        self.model.cpu()
        # self.model.load_state_dict(torch.load('C:\\Users\\multicampus\\subproject3\\backend\\Codes\\checkpoints\\model-best.pth'))
        device = torch.device('cpu')
        self.model.load_state_dict(torch.load('/home/ubuntu/test/IC/model-best.pth', map_location=device))
        
    def inference(self,img_feature):
        img_feature = self.feature_extractor(img_feature)
        # Return the 5 captions from beam serach with beam size 5
        return self.model.decode_sequence(self.model(img_feature.mean(0)[None], img_feature[None], mode='sample', opt={'beam_size':5, 'sample_method':'beam_search', 'sample_n':5})[0])

#Req. 3-3 지 및 캡션 결과 출력
####TODO####
# 이미지와 이미지에 대한 설명을 출력해야한다.
# 이미지 load : cv2.imread / 이미지 출력 : cv2.imshow
# 이미지 캡션 생성 : Caption_Model.inference
if __name__ == '__main__':
    caption_model = Caption_Model()

    image_url = 'example.jpg'
    img = cv2.imread(image_url, cv2.IMREAD_COLOR)
    result = caption_model.inference(image_url)
    cv2.imshow("image", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


    # result = caption_model.inference('http://img.hani.co.kr/imgdb/resize/2018/0328/00500164_20180328.JPG')
    # print(result)
    pass

####TODO#### 
