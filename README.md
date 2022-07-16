## Introduction
Coco-toolkit is a tool for preparing and analyzing object detection data which is coco json format in Python. Tool countains merge, preprocessing, report and converter modules.

1 - Preprocessing
This class obtain preprocess functions for preparing coco json dataset.

2 - Converter
This module has converters functions which are Pascal voc to coco json and coco json to tfrecords.

3 - Merge
Merge module has multiple coco merge function.
It merges all given coco json file and return all in one output folder.

4- Report
Report module has analyze dataset functions. These functions are; return information of data set, plots data set information as pie chart, and integrates data set with coco viewer.

### System requirements
### Installation
## Basic usage

###  1 - Import
##### 1.1 -Import preprocess
from coco_toolkit.helper.preprocess import PreProcess
##### 1.2 -Import merge
from coco_toolkit.helper.merge import merge_multiple_cocos
##### 1.2 -Import report
from coco_toolkit.helper.report import AnalyzeCategories
###  2 - Sample usage
##### 2.1 - Usage filter class
This function filter given class names. It returns filtered coco json as dictionary and saves filtered coco json file and filtered images in new folder.
`
PreProcess(path).export_according2_class(coco, categories, image_path)`


parameter path : This parameter is directory of output.Function saves
filtered dataset in this path.

parameter coco : Coco json file as read dictionary

parameter categories : List of to be filtered class names

parameter image_path: Dataset images folder path

`
coco = PreProcess(path to coco json file).reader()
`
`
PreProcess(path).export_according2_class(coco, ["human", "car"], "/home/user/data/images")
`

## Check before PR 

```bash
black . --config pyproject.toml
isort .
pre-commit run --all-files


```