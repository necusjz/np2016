# -*- coding: UTF-8 -*-

import struct
import numpy as np

class ImageReader:
    def decode_idx3_ubyte(self, idx3_ubyte_file):
    # 读取二进制数据
        f = open(idx3_ubyte_file, 'rb')
        bin_data = f.read();
        f.close();
    # 解析文件头信息，依次为魔数、图片数量、每张图片高、每张图片宽
        offset = 0
        fmt_header = '>IIII'
        magic_number, num_images, num_rows, num_cols = struct.unpack_from(fmt_header, bin_data, offset)
     #   print '魔数:%d, 图片数量: %d张, 图片大小: %d*%d' % (magic_number, num_images, num_rows, num_cols)

    # 解析数据集
        image_size = num_rows * num_cols
        offset += struct.calcsize(fmt_header)
        fmt_image = '>' + str(image_size) + 'B'
        images = np.empty((num_images, num_rows * num_cols))
        for i in range(num_images):
            images[i] = np.array(struct.unpack_from(fmt_image, bin_data, offset)).reshape((image_size))
            offset += struct.calcsize(fmt_image)
        return images
  
    def decode_idx1_ubyte(self, idx1_ubyte_file):
        bin_data = open(idx1_ubyte_file, 'rb').read()

    # 解析文件头信息，依次为魔数和标签数
        offset = 0
        fmt_header = '>ii'
        magic_number, num_images = struct.unpack_from(fmt_header, bin_data, offset)
      # print '魔数:%d, 图片数量: %d张' % (magic_number, num_images)

     # 解析数据集
        offset += struct.calcsize(fmt_header)
        fmt_image = '>B'
        labels = np.empty(num_images)
        for i in range(num_images):
            labels[i] = struct.unpack_from(fmt_image, bin_data, offset)[0]
            offset += struct.calcsize(fmt_image)
        return labels
    
    def load_images(self, imageSource):
        return self.decode_idx3_ubyte(imageSource);
        
    def load_labels(self, imageSource):
        return self.decode_idx1_ubyte(imageSource);
        
