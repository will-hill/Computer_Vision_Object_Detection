import json
import sys
from os import path
import numpy as np
from pathlib import Path
import ruamel_yaml as yaml
from ruamel_yaml import CLoader


def main():
    if len(sys.argv) < 3:
        print((len(sys.argv) - 1), " arguments passed")
        for arg in sys.argv:
            print(arg)
        print("you need to pass a yaml file and a model name as an argument.")
        exit(-1)

    if ~path.exists(sys.argv[1]):
        print(sys.argv[1], " does not exist.")

    model_name = sys.argv[2]
    yaml_file = open(sys.argv[1], 'r')
    yaml_file_to_json_file(yaml_file, model_name)


def yaml_file_to_json_file(yaml_file_path, model_name):
    yaml_obj = yaml_file_to_obj(yaml_file_path)
    json_obj = convert_yaml_to_json(yaml_obj, model_name)
    json_obj_to_file(json_obj, model_name)


def yaml_file_to_obj(yaml_file_path):
    yaml_file_handle = open(yaml_file_path, 'r')
    yaml_text = yaml_file_handle.read().replace('%YAML:1.0\n', '').replace('!!opencv-matrix', '')
    yaml_file_handle.close()
    yaml_obj = yaml.load(yaml_text, Loader=CLoader)
    return yaml_obj


def json_obj_to_file(json_object, model_name):
    potential_json_file_name = model_name + '.yaml.2.json'
    count = 0
    while Path(potential_json_file_name).is_file():
        potential_json_file_name = str(count) + "_" + potential_json_file_name
        count = int(count) + 1

    json_file = open(potential_json_file_name, 'w+')
    json.dump(json_object, json_file, indent=4)
    json_file.close()


def test_fieldname(yaml_obj, yaml_fieldname, default_val):
    if yaml_fieldname in yaml_obj:
        return yaml_obj[yaml_fieldname]
    else:
        print('Warning: No ', yaml_fieldname, ' is set in yaml, defaulting to: ', default_val, '\n')
        return default_val


def convert_yaml_to_json(yaml_obj, model_name):
    # order of JSON matters to toolbox octave/matlab code
    json_ojb = {model_name: {}}
    json_ojb[model_name]['opts'] = {}
    json_ojb[model_name]['opts']['pPyramid'] = {}
    json_ojb[model_name]['opts']['pPyramid']['pChns'] = {}

    # ##########################################################
    # ############### Pyramid Channels SETTINGS ################
    #  pChns       - parameters (struct or name/value pairs) (see chnsCompute.m)

    #   .shrink       - [4] integer downsampling amount for channels
    json_ojb[model_name]['opts']['pPyramid']['pChns']['shrink'] = test_fieldname(yaml_obj['hdc_acfdetector']['pyramid']['channel_features'], 'shrink', 4)

    #   .pColor       - parameters for color space:
    json_ojb[model_name]['opts']['pPyramid']['pChns']['pColor'] = {}
    #   .pColor.enabled      - [1] if true enable color channels
    json_ojb[model_name]['opts']['pPyramid']['pChns']['pColor']['enabled'] = test_fieldname(yaml_obj['hdc_acfdetector']['pyramid']['channel_features']['color'], 'enabled', 1)
    #    .pColor.smooth       - [1] radius for image smoothing (using convTri)
    json_ojb[model_name]['opts']['pPyramid']['pChns']['pColor']['smooth'] = test_fieldname(yaml_obj['hdc_acfdetector']['pyramid']['channel_features']['color'], 'smooth', 1)
    #    .pColor.colorSpace   - ['luv'] choices are: 'gray', 'rgb', 'hsv', 'orig'
    json_ojb[model_name]['opts']['pPyramid']['pChns']['pColor']['colorSpace'] = test_fieldname(yaml_obj['hdc_acfdetector']['pyramid']['channel_features']['color'], 'colorSpace', 'luv')

    #   .pGradMag     - parameters for gradient magnitude:
    json_ojb[model_name]['opts']['pPyramid']['pChns']['pGradMag'] = {}
    #   .pGradMag.enabled      - [1] if true enable gradient magnitude channel
    json_ojb[model_name]['opts']['pPyramid']['pChns']['pGradMag']['enabled'] = yaml_obj['hdc_acfdetector']['pyramid']['channel_features']['gradient_magnitude']['enabled']
    #   .pGradMag.colorChn     - [0] if>0 color channel to use for grad computation
    json_ojb[model_name]['opts']['pPyramid']['pChns']['pGradMag']['colorChn'] = yaml_obj['hdc_acfdetector']['pyramid']['channel_features']['gradient_magnitude']['color_chn']
    #    .pGradMag.normRad      - [5] normalization radius for gradient
    json_ojb[model_name]['opts']['pPyramid']['pChns']['pGradMag']['normRad'] = yaml_obj['hdc_acfdetector']['pyramid']['channel_features']['gradient_magnitude']['norm_rad']
    #    .pGradMag.normConst    - [.005] normalization constant for gradient
    json_ojb[model_name]['opts']['pPyramid']['pChns']['pGradMag']['normConst'] = yaml_obj['hdc_acfdetector']['pyramid']['channel_features']['gradient_magnitude']['norm_const']
    #    .pGradMag.full         - [0] if true compute angles in [0,2*pi) else in [0,pi)
    json_ojb[model_name]['opts']['pPyramid']['pChns']['pGradMag']['full'] = yaml_obj['hdc_acfdetector']['pyramid']['channel_features']['gradient_magnitude']['full']

    #   .pGradHist    - parameters for gradient histograms:
    json_ojb[model_name]['opts']['pPyramid']['pChns']['pGradHist'] = {}
    #   .pGradHist.enabled      - [1] if true enable gradient histogram channels
    json_ojb[model_name]['opts']['pPyramid']['pChns']['pGradHist']['enabled'] = yaml_obj['hdc_acfdetector']['pyramid']['channel_features']['gradient_histogram']['enabled']
    #    .pGradHist.binSize      - [shrink] spatial bin size (defaults to shrink)
    json_ojb[model_name]['opts']['pPyramid']['pChns']['pGradHist']['binSize'] = yaml_obj['hdc_acfdetector']['pyramid']['channel_features']['gradient_histogram']['bin_size']
    #    .pGradHist.nOrients     - [6] number of orientation channels
    json_ojb[model_name]['opts']['pPyramid']['pChns']['pGradHist']['nOrients'] = yaml_obj['hdc_acfdetector']['pyramid']['channel_features']['gradient_histogram']['n_orients']
    #    .pGradHist.softBin      - [0] if true use "soft" bilinear spatial binning
    json_ojb[model_name]['opts']['pPyramid']['pChns']['pGradHist']['softBin'] = yaml_obj['hdc_acfdetector']['pyramid']['channel_features']['gradient_histogram']['soft_bin']
    #    .pGradHist.useHog       - [0] if true perform 4-way hog normalization/clipping
    json_ojb[model_name]['opts']['pPyramid']['pChns']['pGradHist']['useHog'] = yaml_obj['hdc_acfdetector']['pyramid']['channel_features']['gradient_histogram']['use_hog']
    #    .pGradHist.clipHog      - [.2] value at which to clip hog histogram bins
    json_ojb[model_name]['opts']['pPyramid']['pChns']['pGradHist']['clipHog'] = yaml_obj['hdc_acfdetector']['pyramid']['channel_features']['gradient_histogram']['clip_hog']

    #   .complete     - [] if true does not check/set default vals in pChns
    json_ojb[model_name]['opts']['pPyramid']['pChns']['complete'] = 1

    #   .pCustom      - parameters for custom channels (optional struct array):
    #     .enabled      - [1] if true enable custom channel type
    #     .name         - ['REQ'] custom channel type name
    #     .hFunc        - ['REQ'] function handle for computing custom channels
    #     .pFunc        - [{}] additional params for chns=hFunc(I,pFunc{:})
    #     .padWith      - [0] how channel should be padded (e.g. 0,'replicate')

    # #################################################
    # ############### PYRAMID SETTINGS ################
    #   .pPyramid   - [{}] params for creating pyramid (see chnsPyramid)

    #   .nPerOct      - [8] number of scales per octave
    json_ojb[model_name]['opts']['pPyramid']['nPerOct'] = test_fieldname(yaml_obj['hdc_acfdetector']['pyramid'], 'n_per_oct', 8)

    #   .nOctUp       - [0] number of upsampled octaves to compute
    json_ojb[model_name]['opts']['pPyramid']['nOctUp'] = test_fieldname(yaml_obj['hdc_acfdetector']['pyramid'],
                                                                        'n_oct_up', 0)

    #   .nApprox      - [-1] number of approx. scales (if -1 nApprox=nPerOct-1)
    json_ojb[model_name]['opts']['pPyramid']['nApprox'] = test_fieldname(yaml_obj['hdc_acfdetector']['pyramid'], 'n_approx', -1)

    #   .lambdas      - [] coefficients for power law scaling (see BMVC10)
    json_ojb[model_name]['opts']['pPyramid']['lambdas'] = test_fieldname(yaml_obj['hdc_acfdetector']['pyramid'], 'lambdas', {})

    #   .pad          - [0 0] amount to pad channels (along T/B and L/R)
    json_ojb[model_name]['opts']['pPyramid']['pad'] = test_fieldname(yaml_obj['hdc_acfdetector']['pyramid'], 'pad',
                                                                     [0, 0])

    #   .minDs        - [16 16] minimum image size for channel computation
    json_ojb[model_name]['opts']['pPyramid']['minDs'] = [yaml_obj['hdc_acfdetector']['pyramid']['min_rows'],
                                                         yaml_obj['hdc_acfdetector']['pyramid']['min_cols']]

    #   .smooth       - [1] radius for channel smoothing (using convTri)
    json_ojb[model_name]['opts']['pPyramid']['smooth'] = test_fieldname(yaml_obj['hdc_acfdetector']['pyramid'], 'smooth', 1)

    #   .concat       - [1] if true concatenate channels
    json_ojb[model_name]['opts']['pPyramid']['concat'] = test_fieldname(yaml_obj['hdc_acfdetector']['pyramid'], 'concat', 1)

    #   .complete     - [] if true does not check/set default vals in pPyramid
    json_ojb[model_name]['opts']['pPyramid']['complete'] = test_fieldname(yaml_obj['hdc_acfdetector']['pyramid'], 'complete', {})

    # #########################################
    # ############### ACF OPTS ################
    # ##### (1) features and model ############

    #   .filters    - [] [wxwxnChnsxnFilter] filters or [wFilter,nFilter]
    json_ojb[model_name]['opts']['filters'] = test_fieldname(yaml_obj['hdc_acfdetector'], 'filters', {})

    #   .modelDs    - [] model height+width without padding (eg [100 41])
    json_ojb[model_name]['opts']['modelDs'] = [yaml_obj['hdc_acfdetector']['model_n_rows'], yaml_obj['hdc_acfdetector']['model_n_cols']]

    #   .modelDsPad - [] model height+width with padding (eg [128 64])
    json_ojb[model_name]['opts']['modelDsPad'] = [yaml_obj['hdc_acfdetector']['model_n_rows_pad'], yaml_obj['hdc_acfdetector']['model_n_cols_pad']]

    #   .stride     - [4] spatial stride between detection windows
    json_ojb[model_name]['opts']['stride'] = test_fieldname(yaml_obj['hdc_acfdetector'], 'stride', 4)

    #   .cascThr    - [-1] constant cascade threshold (affects speed/accuracy)
    json_ojb[model_name]['opts']['cascThr'] = test_fieldname(yaml_obj['hdc_acfdetector'], 'casc_thr', -1)

    #   .cascCal    - [.005] cascade calibration (affects speed/accuracy)
    json_ojb[model_name]['opts']['cascCal'] = test_fieldname(yaml_obj['hdc_acfdetector'], 'casc_cal', 0.005)

    #   .nWeak      - [128] vector defining number weak clfs per stage
    json_ojb[model_name]['opts']['nWeak'] = test_fieldname(yaml_obj['hdc_acfdetector'], 'nWeak', 128)

    #   .seed       - [0] seed for random stream (for reproducibility)
    json_ojb[model_name]['opts']['seed'] = test_fieldname(yaml_obj['hdc_acfdetector'], 'seed', 0)

    #   .name       - [''] name to prepend to clf and log filenames
    json_ojb[model_name]['opts']['name'] = test_fieldname(yaml_obj['hdc_acfdetector'], 'name', '')

    # ##########################################
    # ########### AdaBoost Settings ############
    #   .pBoost     - [..] parameters for boosting (see adaBoostTrain.m)
    json_ojb[model_name]['opts']['pBoost'] = test_fieldname(yaml_obj['hdc_acfdetector'], 'pBoost', {})

    # ##########################################
    # ########### pNms #########################
    #   .pNms       - [..] params for non-maximal suppression (see bbNms.m)
    #   from bbNms.m
    json_ojb[model_name]['opts']['pNms'] = {}
    #   .radii      - [.15 .15 1 1] supression radii ('ms' only, see above)
    # json_model[model_name]['opts']['pNms']['radii'] = test_fieldname(yaml['hdc_acfdetector']['pNms'],'radii', {})

    #   .resize     - {} parameters for bbApply('resize')
    json_ojb[model_name]['opts']['pNms']['resize'] = test_fieldname(yaml_obj['hdc_acfdetector']['pNms'], 'resize', {})

    #   .thr        - [-inf] threshold below which to discard (0 for 'ms')
    json_ojb[model_name]['opts']['pNms']['thr'] = test_fieldname(yaml_obj['hdc_acfdetector']['pNms'], 'thr', '-inf')

    #   .maxn       - [inf] if n>maxn split and run recursively (see above)
    json_ojb[model_name]['opts']['pNms']['maxn'] = test_fieldname(yaml_obj['hdc_acfdetector']['pNms'], 'maxn', 'inf')

    #   .separate   - [0] run nms separately on each bb type (bbType)
    json_ojb[model_name]['opts']['pNms']['separate'] = test_fieldname(yaml_obj['hdc_acfdetector']['pNms'], 'separate',
                                                                      0)

    #   .overlap    - [.5] area of overlap for bbs
    json_ojb[model_name]['opts']['pNms']['overlap'] = test_fieldname(yaml_obj['hdc_acfdetector']['pNms'], 'overlap',
                                                                     0.5)

    #   .ovrDnm     - ['union'] area of overlap denominator ('union' or 'min')
    json_ojb[model_name]['opts']['pNms']['ovrDnm'] = test_fieldname(yaml_obj['hdc_acfdetector']['pNms'], 'ovrDnm',
                                                                    'union')

    #   .type       - ['max'] 'max', 'maxg', 'ms', 'cover', or 'none'
    json_ojb[model_name]['opts']['pNms']['type'] = test_fieldname(yaml_obj['hdc_acfdetector']['pNms'], 'type', 'max')

    # ########################################################
    # ############### ACF OPTS ###############################
    # ##### (2) training data location and amount ############

    #   .posGtDir   - [''] dir containing ground truth
    json_ojb[model_name]['opts']['posGtDir'] = ''

    #   .posImgDir  - [''] dir containing full positive images
    json_ojb[model_name]['opts']['posImgDir'] = ''

    #   .negImgDir  - [''] dir containing full negative images
    json_ojb[model_name]['opts']['negImgDir'] = ''

    #   .posWinDir  - [''] dir containing cropped positive windows
    json_ojb[model_name]['opts']['posWinDir'] = ''

    #   .negWinDir  - [''] dir containing cropped negative windows
    json_ojb[model_name]['opts']['negWinDir'] = ''

    #   .imreadf    - [@imread] optional custom function for reading images
    json_ojb[model_name]['opts']['imreadf'] = {}

    #   .imreadp    - [{}] optional custom parameters for imreadf
    json_ojb[model_name]['opts']['imreadp'] = {}

    #   .nPos       - [inf] max number of pos windows to sample
    json_ojb[model_name]['opts']['nPos'] = test_fieldname(yaml_obj['hdc_acfdetector'], 'nPos', 'inf')

    #   .nNeg       - [5000] max number of neg windows to sample
    json_ojb[model_name]['opts']['nNeg'] = test_fieldname(yaml_obj['hdc_acfdetector'], 'nNeg', 5000)

    #   .nPerNeg    - [25]  max number of neg windows to sample per image
    json_ojb[model_name]['opts']['nPerNeg'] = test_fieldname(yaml_obj['hdc_acfdetector'], 'nPerNeg', 25)

    #   .nAccNeg    - [10000] max number of neg windows to accumulate
    json_ojb[model_name]['opts']['nAccNeg'] = test_fieldname(yaml_obj['hdc_acfdetector'], 'nAccNeg', 10000)

    #   .winsSave   - [0] if true save cropped windows at each stage to disk
    json_ojb[model_name]['opts']['winsSave'] = test_fieldname(yaml_obj['hdc_acfdetector'], 'winsSave', 0)

    #   .pLoad      - [..] params for bbGt>bbLoad (see bbGt)
    json_ojb[model_name]['opts']['pLoad'] = test_fieldname(yaml_obj['hdc_acfdetector'], 'pLoad', {})

    #   .pJitter    - [{}] params for jittering pos windows (see jitterImage)
    json_ojb[model_name]['opts']['pJitter'] = test_fieldname(yaml_obj['hdc_acfdetector'], 'pJitter', {})

    # ########################################################
    # ############ Actual Model  aka Classifier ##############
    json_ojb[model_name]['clf'] = {}

    json_ojb[model_name]['clf']['treeDepth'] = yaml_obj['hdc_acfdetector']['classifier']['tree_depth']

    child_rows = yaml_obj['hdc_acfdetector']['classifier']['child']['rows']
    child_cols = yaml_obj['hdc_acfdetector']['classifier']['child']['cols']
    child_data = yaml_obj['hdc_acfdetector']['classifier']['child']['data']
    json_ojb[model_name]['clf']['child'] = np.array(child_data).reshape(child_rows, child_cols).tolist()

    depth_rows = yaml_obj['hdc_acfdetector']['classifier']['depth']['rows']
    depth_cols = yaml_obj['hdc_acfdetector']['classifier']['depth']['cols']
    depth_data = yaml_obj['hdc_acfdetector']['classifier']['depth']['data']
    json_ojb[model_name]['clf']['depth'] = np.array(depth_data).reshape(depth_rows, depth_cols).tolist()

    fids_rows = yaml_obj['hdc_acfdetector']['classifier']['fids']['rows']
    fids_cols = yaml_obj['hdc_acfdetector']['classifier']['fids']['cols']
    fids_data = yaml_obj['hdc_acfdetector']['classifier']['fids']['data']
    json_ojb[model_name]['clf']['fids'] = np.array(fids_data).reshape(fids_rows, fids_cols).tolist()

    hs_rows = yaml_obj['hdc_acfdetector']['classifier']['hs']['rows']
    hs_cols = yaml_obj['hdc_acfdetector']['classifier']['hs']['cols']
    hs_data = yaml_obj['hdc_acfdetector']['classifier']['hs']['data']
    json_ojb[model_name]['clf']['hs'] = np.array(hs_data).reshape((hs_rows, hs_cols)).tolist()

    thrs_rows = yaml_obj['hdc_acfdetector']['classifier']['thrs']['rows']
    thrs_cols = yaml_obj['hdc_acfdetector']['classifier']['thrs']['cols']
    thrs_data = yaml_obj['hdc_acfdetector']['classifier']['thrs']['data']
    json_ojb[model_name]['clf']['thrs'] = np.array(thrs_data).reshape(thrs_rows, thrs_cols).tolist()

    weights_rows = yaml_obj['hdc_acfdetector']['classifier']['weights']['rows']
    weights_cols = yaml_obj['hdc_acfdetector']['classifier']['weights']['cols']
    weights_data = yaml_obj['hdc_acfdetector']['classifier']['weights']['data']
    json_ojb[model_name]['clf']['weights'] = np.array(weights_data).reshape(weights_rows, weights_cols).tolist()

    json_ojb[model_name]['info'] = {}

    return json_ojb
