import os
import unittest

from coco_toolkit.helper.merge import merge_multiple_cocos
from coco_toolkit.helper.preprocess import PreProcess
from coco_toolkit.helper.report import AnalyzeCategories


class TestCocoMergeTool(unittest.TestCase):
    def test_set_unique_image_id(self):
        path = "tests/coco_dataset/annotations/coco.json"
        parent_path_json = os.path.abspath(os.path.join(path, os.pardir))
        coco = PreProcess(path).reader()
        start_id = 10
        coco = PreProcess(parent_path_json).set_unique_image_id(coco=coco, first_id=start_id, inplace=True)
        result = coco["images"][0]["id"]
        result_1 = coco["images"][2]["id"]
        result_2 = coco["images"][4]["id"]
        self.assertEqual(result, start_id)
        self.assertEqual(result_1, start_id + 2)
        self.assertEqual(result_2, start_id + 4)

    def test_set_unique_class_id(self):
        path = "tests/coco_dataset/annotations/coco.json"
        parent_path_json = os.path.abspath(os.path.join(path, os.pardir))
        coco = PreProcess(path).reader()
        start_id = 1
        coco = PreProcess(parent_path_json).set_unique_class_id(
            coco=coco, first_id=start_id, b_grounds=True, inplace=True
        )
        result = coco["categories"][1]["id"]
        result_1 = coco["categories"][2]["id"]
        self.assertEqual(result, start_id)
        self.assertEqual(result_1, start_id + 1)

    def test_set_unique_annotation_id(self):
        path = "tests/coco_dataset/annotations/coco.json"
        parent_path_json = os.path.abspath(os.path.join(path, os.pardir))
        coco = PreProcess(path).reader()
        start_id = 6
        coco = PreProcess(parent_path_json).set_unique_annotation_id(coco=coco, first_id=start_id, inplace=True)
        result = coco["annotations"][0]["id"]
        result_1 = coco["annotations"][2]["id"]
        result_2 = coco["annotations"][4]["id"]
        self.assertEqual(result, start_id)
        self.assertEqual(result_1, start_id + 2)
        self.assertEqual(result_2, start_id + 4)

    def test_check_id_unique(self):
        path = "tests/coco_dataset/annotations/coco.json"
        coco = PreProcess(path).reader()
        result = PreProcess.check_id_unique(coco=coco)
        self.assertTrue(result)

    def test_extrack_data_by_class_name(self):
        path = "tests/coco_dataset/annotations/coco.json"
        parent_path_json = os.path.abspath(os.path.join(path, os.pardir))
        img_path = "tests/coco_dataset/images"
        coco = PreProcess(path).reader()
        export_list = ["crosswalk"]
        coco = PreProcess(parent_path_json).extrack_data_by_class_name(
            coco=coco, categories=export_list, image_path=img_path
        )
        result = AnalyzeCategories(coco).class_have_ann_list()
        self.assertEqual(result, export_list)

    def test_filter_data_by_class_name(self):
        path = "tests/coco_dataset/annotations/coco.json"
        parent_path_json = os.path.abspath(os.path.join(path, os.pardir))
        img_path = "tests/coco_dataset/images"
        coco = PreProcess(path).reader()
        filter_list = ["crosswalk"]
        coco = PreProcess(parent_path_json).filter_data_by_class_name(
            coco=coco, categories=filter_list, image_path=img_path
        )
        result = AnalyzeCategories(coco).class_have_ann_list()
        self.assertEqual(result, ["stop", "trafficlight"])

    def test_remove_segmentation(self):
        path = "tests/coco_dataset/annotations/coco.json"
        parent_path_json = os.path.abspath(os.path.join(path, os.pardir))
        coco = PreProcess(path).reader()
        coco = PreProcess(parent_path_json).remove_segmentation(coco=coco, inplace=True)
        result = coco["annotations"][0]["segmentation"]
        result_1 = coco["annotations"][7]["segmentation"]
        self.assertEqual(result, {})
        self.assertEqual(result_1, {})

    def test_box2segmentation(self):
        path = "tests/coco_dataset/annotations/coco.json"
        parent_path_json = os.path.abspath(os.path.join(path, os.pardir))
        coco = PreProcess(path).reader()
        coco = PreProcess(parent_path_json).remove_segmentation(coco=coco, inplace=True)
        coco = PreProcess(parent_path_json).box2segmentation(coco=coco, inplace=True)
        result = coco["annotations"][0]["segmentation"]
        self.assertEqual(result, [[147, 70, 147, 173, 288, 173, 288, 70]])

    def test_change_image_file_names(self):
        path = "tests/coco_dataset/annotations/coco.json"
        parent_path_json = os.path.abspath(os.path.join(path, os.pardir))
        img_path = "tests/coco_dataset/images"
        image_list = os.listdir(img_path)
        coco = PreProcess(path).reader()
        name = coco["images"][0]["file_name"]
        coco = PreProcess(parent_path_json).change_image_file_names(coco=coco, path=img_path, inplace=True)
        if name in image_list:
            result = True
        else:
            result = False
        self.assertTrue(result)

    def test_remove_duplicate_image_names(self):
        path = "tests/coco_dataset/annotations/coco.json"
        parent_path_json = os.path.abspath(os.path.join(path, os.pardir))
        coco = PreProcess(path).reader()
        coco = PreProcess(parent_path_json).remove_duplicate_image_name(coco=coco, inplace=True)
        len_image = 10
        result = len(coco["images"])
        self.assertEqual(result, len_image)

    def test_given_category_count(self):
        path = "tests/coco_dataset/annotations/coco.json"
        coco = PreProcess(path).reader()
        result = AnalyzeCategories(coco).given_category_count("crosswalk")
        self.assertEqual(result, 4)

    def test_class_names(self):
        path = "tests/coco_dataset/annotations/coco.json"
        class_names = ["Background", "stop", "trafficlight", "crosswalk"]
        coco = PreProcess(path).reader()
        result = AnalyzeCategories(coco).class_names()
        self.assertEqual(result, class_names)

    def test_total_class(self):
        path = "tests/coco_dataset/annotations/coco.json"
        coco = PreProcess(path).reader()
        result = AnalyzeCategories(coco).total_class_count()
        total_class = 4
        self.assertEqual(result, total_class)

    def test_classes_have_annotations_tuple(self):
        path = "tests/coco_dataset/annotations/coco.json"
        coco = PreProcess(path).reader()
        have_anno_class = ("stop", "trafficlight", "crosswalk")
        result = AnalyzeCategories(coco).classes_have_annotations_tuple()
        self.assertEqual(result, have_anno_class)

    def test_aspect_ratio(self):
        path = "tests/coco_dataset/annotations/coco.json"
        coco = PreProcess(path).reader()
        aspect_ratio_dict = {
            "100:67": 1,
            "16:9": 1,
            "200:133": 1,
            "3:4": 2,
            "400:267": 1,
            "400:301": 2,
            "40:27": 1,
            "4:3": 1,
        }
        result = AnalyzeCategories(coco).images_aspect_ratio()
        self.assertEqual(result, aspect_ratio_dict)

    def test_merge_multiple_cocos(self):
        path_1 = "tests/coco_dataset_1/annotations/coco.json"
        img_1 = "tests/coco_dataset_1/images"
        path_2 = "tests/coco_dataset/annotations/coco.json"
        img_2 = "tests/coco_dataset/images"
        merge_path = "test_merge"
        len_annotations = 51
        len_images = 20
        len_categories = 7
        args = [path_1, img_1], [path_2, img_2]
        merge = merge_multiple_cocos(*args, merge_path=merge_path, first_id=100000, visualizer=False)
        result = len(merge["annotations"])
        result_1 = len(merge["images"])
        result_2 = len(merge["categories"])

        self.assertEqual(result, len_annotations)
        self.assertEqual(result_1, len_images)
        self.assertEqual(result_2, len_categories)

    def test_remove_distorted_bbox(self):
        path = "tests/coco_dataset/annotations/coco.json"
        parent_path_json = os.path.abspath(os.path.join(path, os.pardir))
        coco = PreProcess(path).reader()
        coco = PreProcess(parent_path_json).remove_distorted_bbox(coco, True)
        count = []
        for ann in coco["annotations"]:
            if ann["bbox"] != {}:
                count.append(0)
        result = len(count)
        len_anno = 13
        self.assertEqual(result, len_anno)


if __name__ == "__main__":
    unittest.main()
