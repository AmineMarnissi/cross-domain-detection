import sys
import time
import chainer
from chainercv.links import FasterRCNNVGG16
from chainercv.links import SSD300
from chainercv.links import SSD512

from dataset import BAMDataset
from dataset import ClipArtDataset
from dataset import VOCDataset
from opt import bam_media_classes


def get_detector(det_type, model_args):
    if det_type == 'ssd300':
        model = SSD300(**model_args)
    elif det_type == 'ssd512':
        model = SSD512(**model_args)
    elif det_type == 'faster':
        model = FasterRCNNVGG16(**model_args)
    else:
        raise NotImplementedError
    return model


def get_detection_dataset(data_type, subset, root):
    if data_type in bam_media_classes:
        dataset = BAMDataset(root, subset)
    elif data_type == 'clipart':
        dataset = ClipArtDataset(root, subset)
    elif data_type == 'voc':
        dataset = VOCDataset(root, subset)
    else:
        raise NotImplementedError
    assert (issubclass(type(dataset), chainer.dataset.DatasetMixin))
    return dataset


class ProgressHook(object):
    def __init__(self, n_total):
        self.n_total = n_total
        self.start = time.time()
        self.n_processed = 0

    def __call__(self, imgs, pred_values, gt_values):
        self.n_processed += len(imgs)
        fps = self.n_processed / (time.time() - self.start)
        sys.stdout.write(
            '\r{:d} of {:d} images, {:.2f} FPS'.format(
                self.n_processed, self.n_total, fps))
        sys.stdout.flush()
