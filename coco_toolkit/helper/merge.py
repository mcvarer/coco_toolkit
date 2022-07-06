import datetime
import os
import shutil

from tqdm import tqdm

from coco_toolkit.helper.preprocess import PreProcess
from coco_toolkit.helper.report import AnalyzeCategories


def merge_multiple_cocos(*args: list, merge_path: str, first_id: int, visualizer: bool):
    """
    :param merge_path: Path of output folder directory
    :param first_id: Value of first id
    :param visualizer: if it's True visualize categories with pie chart
    :param args: It contains lists in index 0 json path and index 1 images path. For example
    [json_path_1, image path_1], [json_path_2, image path_2] .....
    :return: return merge data and save to given directory
    """
    merged = {
        "licenses": [],
        "info": {},
        "categories": [],
        "images": [],
        "annotations": [],
    }
    categories: list = []
    class_names: list = []
    list_dir: list = []

    time = str(datetime.datetime.now()).split(".")[0].split()
    time = "-".join(time).replace(":", "-")

    merged_path_ann = merge_path + f"/merge_folder_{time}/annotations"
    merged_path_img = merge_path + f"/merge_folder_{time}/images"
    os.makedirs(merged_path_ann), os.makedirs(merged_path_img)

    for index, path in enumerate(tqdm(args)):
        json_path = path[0]
        image_path = path[1]
        p = PreProcess(json_path)
        coco = p.reader()
        PreProcess.check_id_unique(coco)
        coco = p.set_unique_image_id(coco, first_id * (index + 1), False)
        coco = p.set_unique_annotation_id(coco, first_id * (index + 1), False)

        list_dir.append(os.listdir(image_path))

        merged["images"] += coco["images"]
        merged["annotations"] += coco["annotations"]

        if index == 0:
            merged["categories"] += coco["categories"]
            merged["licenses"] = coco["licenses"]
            merged["info"] = coco["info"]

            class_names = [cat["name"] for cat in coco["categories"]]

        else:
            for cat in coco["categories"]:
                if cat["name"] not in class_names:
                    class_names.append(cat["name"])
                    categories.append(cat)

        if categories:
            merged["categories"] += categories
            categories = []

        for image in list_dir[0]:
            shutil.copy(image_path + f"/{image}", merged_path_img + f"/{image}")
        list_dir = []

    merged = PreProcess(merge_path).set_unique_class_id(merged, 0, False, False)

    PreProcess.save_coco_file(merged, merged_path_ann + f"/merge")
    AnalyzeCategories(merged).total_class_count()
    AnalyzeCategories(merged).plot_class_pie_chart(visualizer)
    return merged
