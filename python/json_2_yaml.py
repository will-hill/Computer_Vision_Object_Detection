import json
import sys
from os import path
import numpy as np
from pathlib import Path
import ruamel_yaml as yaml

def main():
    if len(sys.argv) < 3:
        print((len(sys.argv) - 1), " arguments passed")
        for arg in sys.argv:
            print(arg)
        print("you need to pass a json file and a model name as an argument.")
        exit(-1)

    if not path.exists(sys.argv[1]):
        print(sys.argv[1], " does not exist.")

    model_name = sys.argv[2]
    json_file = open(sys.argv[1], 'r')
    json_file_to_yaml_file(json_file, model_name)


def json_file_to_yaml_file(json_file_path, model_name):
    json_obj = json_file_to_obj(json_file_path, model_name)
    del json_file_path
    yaml_obj = convert_json_to_yaml(json_obj, model_name)
    del json_obj
    yaml_text = opencv_ize_yaml(yaml_obj)
    del yaml_obj
    yaml_text_to_file(yaml_text, model_name)


def json_file_to_obj(json_file_path, model_name):
    json_obj = json.load(json_file_path)[model_name]
    json_file_path.close()
    return json_obj


def yaml_text_to_file(yaml_text, model_name):
    potential_yaml_file_name = model_name + '.json.2.yaml'
    count = 0
    while Path(potential_yaml_file_name).is_file():
        potential_yaml_file_name = str(count) + "_" + potential_yaml_file_name
        count = int(count) + 1

    yaml_file = open(potential_yaml_file_name, 'w+')
    yaml_file.write(yaml_text)
    yaml_file.close()


def convert_json_to_yaml(json_obj, model_name):
    yaml_obj = {model_name: {}}
    y = yaml_obj[model_name]

    y['format'] = 3

    y['pyramid'] = {}

    y['pyramid']['channel_features'] = {}

    y['pyramid']['channel_features']['shrink'] = json_obj['opts']['pPyramid']['pChns']['shrink']

    y['pyramid']['channel_features']['color'] = {}
    y['pyramid']['channel_features']['color']['enabled'] = json_obj['opts']['pPyramid']['pChns']['pColor']['enabled']
    y['pyramid']['channel_features']['color']['smooth'] = json_obj['opts']['pPyramid']['pChns']['pColor']['smooth']
    # y['pyramid']['channel_features']['color']['colorSpace'] = json_obj['opts']['pPyramid']['pChns']['pColor']['colorSpace']

    y['pyramid']['channel_features']['gradient_magnitude'] = {}

    y['pyramid']['channel_features']['gradient_magnitude']['enabled'] = json_obj['opts']['pPyramid']['pChns']['pGradMag']['enabled']
    y['pyramid']['channel_features']['gradient_magnitude']['color_chn'] = json_obj['opts']['pPyramid']['pChns']['pGradMag']['colorChn']
    y['pyramid']['channel_features']['gradient_magnitude']['norm_rad'] = json_obj['opts']['pPyramid']['pChns']['pGradMag']['normRad']
    y['pyramid']['channel_features']['gradient_magnitude']['norm_const'] = json_obj['opts']['pPyramid']['pChns']['pGradMag']['normConst']
    y['pyramid']['channel_features']['gradient_magnitude']['full'] = json_obj['opts']['pPyramid']['pChns']['pGradMag']['full']

    y['pyramid']['channel_features']['gradient_histogram'] = {}
    y['pyramid']['channel_features']['gradient_histogram']['enabled'] = json_obj['opts']['pPyramid']['pChns']['pGradHist']['enabled']
    y['pyramid']['channel_features']['gradient_histogram']['bin_size'] = json_obj['opts']['pPyramid']['pChns']['pGradHist']['binSize']
    y['pyramid']['channel_features']['gradient_histogram']['n_orients'] = json_obj['opts']['pPyramid']['pChns']['pGradHist']['nOrients']
    y['pyramid']['channel_features']['gradient_histogram']['soft_bin'] = json_obj['opts']['pPyramid']['pChns']['pGradHist']['softBin']
    y['pyramid']['channel_features']['gradient_histogram']['use_hog'] = json_obj['opts']['pPyramid']['pChns']['pGradHist']['useHog']
    y['pyramid']['channel_features']['gradient_histogram']['clip_hog'] = json_obj['opts']['pPyramid']['pChns']['pGradHist']['clipHog']

    y['pyramid']['n_per_oct'] = json_obj['opts']['pPyramid']['nPerOct']
    y['pyramid']['n_oct_up'] = json_obj['opts']['pPyramid']['nOctUp']
    y['pyramid']['n_approx'] = json_obj['opts']['pPyramid']['nApprox']
    y['pyramid']['min_rows'] = json_obj['opts']['pPyramid']['minDs'][0]
    y['pyramid']['min_cols'] = json_obj['opts']['pPyramid']['minDs'][1]

    y['pyramid']['lambdas'] = str(np.array(json_obj['opts']['pPyramid']['lambdas']).ravel().tolist())

    y['pyramid']['pad'] = str(json_obj['opts']['pPyramid']['pad'])
    y['pyramid']['smooth'] = json_obj['opts']['pPyramid']['smooth']

    y['pNms'] = {}
    y['pNms']['type'] = json_obj['opts']['pNms']['type']
    y['pNms']['overlap'] = json_obj['opts']['pNms']['overlap']
    y['pNms']['ovrDnm'] = json_obj['opts']['pNms']['ovrDnm']

    y['seed'] = json_obj['opts']['seed']

    y['model_n_rows'] = json_obj['opts']['modelDs'][0]
    y['model_n_cols'] = json_obj['opts']['modelDs'][1]
    y['model_n_rows_pad'] = json_obj['opts']['modelDsPad'][0]
    y['model_n_cols_pad'] = json_obj['opts']['modelDsPad'][1]

    y['stride'] = json_obj['opts']['stride']

    y['classifier'] = {}

    y['classifier']['fids'] = {}
    fids_list = json_obj['clf']['fids']  # list [3]
    y['classifier']['fids']['rows'] = len(fids_list)
    y['classifier']['fids']['cols'] = len(fids_list[0])
    y['classifier']['fids']['dt'] = 'i'
    y['classifier']['fids']['data'] = str(np.concatenate(fids_list).ravel().tolist())
    y['classifier']['thrs'] = {}
    thrs_list = json_obj['clf']['thrs']  # list [3]
    y['classifier']['thrs']['rows'] = len(thrs_list)
    y['classifier']['thrs']['cols'] = len(thrs_list[0])
    y['classifier']['thrs']['dt'] = 'f'
    y['classifier']['thrs']['data'] = str(np.concatenate(thrs_list).ravel().tolist())

    y['classifier']['child'] = {}
    child_list = json_obj['clf']['child']  # list [3]
    y['classifier']['child']['rows'] = len(child_list)
    y['classifier']['child']['cols'] = len(child_list[0])
    y['classifier']['child']['dt'] = 'i'
    y['classifier']['child']['data'] = str(np.concatenate(child_list).ravel().tolist())

    y['classifier']['hs'] = {}
    hs_list = json_obj['clf']['hs']  # list [3]
    y['classifier']['hs']['rows'] = len(hs_list)
    y['classifier']['hs']['cols'] = len(hs_list[0])
    y['classifier']['hs']['dt'] = 'f'
    y['classifier']['hs']['data'] = str(np.concatenate(hs_list).ravel().tolist())

    y['classifier']['weights'] = {}
    weights_list = json_obj['clf']['weights']  # list [3]
    y['classifier']['weights']['rows'] = len(weights_list)
    y['classifier']['weights']['cols'] = len(weights_list[0])
    y['classifier']['weights']['dt'] = 'f'
    y['classifier']['weights']['data'] = str(np.concatenate(weights_list).ravel().tolist())

    y['classifier']['depth'] = {}
    depth_list = json_obj['clf']['depth']  # list [3]
    y['classifier']['depth']['rows'] = len(depth_list)
    y['classifier']['depth']['cols'] = len(depth_list[0])
    y['classifier']['depth']['dt'] = 'i'
    y['classifier']['depth']['data'] = str(np.concatenate(depth_list).ravel().tolist())

    y['classifier']['tree_depth'] = json_obj['clf']['treeDepth']

    # return y
    # yaml_obj = {model_name: y}

    return yaml_obj


class CustomDumper(yaml.Dumper):
    def represent_dict_preserve_order(self, data):
        return self.represent_dict(data.items())

    def represent_list(self, data):
        self.default_flow_style = True
        return self.represent_list(self, data)


def opencv_ize_yaml(yaml_obj):
    CustomDumper.add_representer(dict, CustomDumper.represent_dict_preserve_order)

    yaml_text = yaml.dump(yaml_obj, Dumper=CustomDumper, indent=4, allow_unicode=True, default_flow_style=False, canonical=False, version=(1, 0), explicit_start=None)

    yaml_text = yaml_text.replace("'[","[ ")
    yaml_text = yaml_text.replace("]'"," ]")

    yaml_text = yaml_text.replace('child:', 'child: !!opencv-matrix')
    yaml_text = yaml_text.replace('fids:', 'fids: !!opencv-matrix')
    yaml_text = yaml_text.replace('hs:', 'hs: !!opencv-matrix')
    yaml_text = yaml_text.replace('weights:', 'weights: !!opencv-matrix')
    yaml_text = yaml_text.replace('thrs:', 'thrs: !!opencv-matrix')
    yaml_text = yaml_text.replace(' depth:', ' depth: !!opencv-matrix')
    return yaml_text


main()
