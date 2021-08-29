
import os
import json as jsonmod
import hashlib

import torch
import torch.utils.data as data
from jina import Document


cur_dir = os.path.dirname(os.path.abspath(__file__))



class MyDataSet(data.Dataset):
    """
    Loading Data present in the dir
    """

    def __init__(self, images_root, captions_file_path):
        self.images_root = images_root
        self.captions_file_path = captions_file_path
        with open(self.captions_file_path, 'r') as cf:
            self.lines = cf.readlines()[1:]

    def __getitem__(self, index):
        """This function returns a tuple that is further passed to collate_fn
        """
        image_file_name, caption = self.lines[index*5].split(',', 1)
        with open(os.path.join(self.images_root, image_file_name), 'rb') as fp:
            image_buffer = fp.read()
        return image_buffer, str(caption).lower().rstrip()

    def __len__(self):
        return int(len(self.lines)/5)


def collate_fn(data):
    # Not sure this is actually needed
    images, captions = zip(*data)
    return images, captions



def input_index_data(num_docs=None, batch_size=8):
    captions = 'captions.txt'
    base_folder = '.'
    root=os.path.join(cur_dir, f'{base_folder}/data/images')
    captions=os.path.join(cur_dir, './data/captions.txt')
    dataset = MyDataSet(images_root=root, captions_file_path=captions)
    data_loader = torch.utils.data.DataLoader(dataset=dataset,
                                              batch_size=batch_size,
                                              shuffle=False,
                                              pin_memory=True,
                                              num_workers=1,
                                              collate_fn=collate_fn)


    for i, (images, captions) in enumerate(data_loader):
        for image, caption in zip(images, captions):
            hashed = hashlib.sha1(image).hexdigest()
            document_img = Document()
            
            document_img.buffer = image
            document_img.modality = 'image'
            document_img.mime_type = 'image/jpeg'
            
            document_caption = Document(id=hashed)
            
            document_caption.text = caption
            document_caption.modality = 'text'
            document_caption.mime_type = 'text/plain'
            document_caption.tags['id'] = caption

            yield document_img
            yield document_caption

        if num_docs and (i + 1) * batch_size >= num_docs:
            break
