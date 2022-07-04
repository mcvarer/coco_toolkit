import datetime
import logging
import os
import shutil

from coco_toolkit.helper.preprocess import PreProcess
from coco_toolkit.modules.voc2coco import main


def voc2coco(data_xml_folder_path: str, output_path: str, image_path: str):
    """
    :param data_xml_folder_path: directory of folder that obtain datas in format xml
    :param output_path: directory of folder that created coco json
    :param image_path: Data set's images path
    :return: Coco json file as dictionary and saves coco data set in given output path
    """
    time = str(datetime.datetime.now()).split(".")[0].split()
    time = "-".join(time).replace(":", "-")

    main(data_xml_folder_path, output_path, time)
    json_path = output_path + f"/converted_coco_{time}/annotations/coco.json"
    coco = PreProcess(json_path).reader()
    coco = PreProcess(json_path).set_unique_image_id(coco, 1, False)
    coco = PreProcess(json_path).set_unique_annotation_id(coco, 1, False)
    coco = PreProcess(json_path).set_unique_class_id(coco, 1, False, False)
    list_dir_img = os.listdir(image_path)
    for image in list_dir_img:
        shutil.copy(
            image_path + f"/{image}", output_path + f"/converted_coco_{time}/images/{image}",
        )
    PreProcess.save_coco_file(coco, json_path.split(".")[0])
    log = logging.getLogger()
    log.info("coco dataset is ready!")
    log.info(f"It's saved to {output_path}/converted_coco_{time}")
    return coco
