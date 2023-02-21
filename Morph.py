class Morph:
    positive_value = '1'
    negative_value = ' '

    # structuring element
    SE = {
        'core': {'x': 0, 'y': 0, 'defined': False},
        'shape': [],
        'square': 0
    }

    # changeable image
    binary_image = []

    # make black matrix filled with negative values
    def pure_canvas(self, lines: int, columns: int):
        return [[self.negative_value] * columns for i in range(lines)]

    def set_SE(self, shape: list, core_x=None, core_y=None):
        self.SE['shape'] = shape

        # count square of SE
        for line in self.SE['shape']:
            for pixel in line:
                if pixel == self.positive_value:
                    self.SE['square'] += 1

        # set core of SE
        if core_x is not None and core_y is not None:
            self.SE['core']['defined'] = True
            self.SE['core']['x'] = core_x
            self.SE['core']['y'] = core_x
        else:
            SE_height = len(self.SE['shape'])
            SE_widht = len(self.SE['shape'][0])

            self.SE['core']['defined'] = True
            self.SE['core']['x'] = round((SE_widht - 1) / 2)
            self.SE['core']['y'] = round((SE_height - 1) / 2)

    def set_binary_image(self, image):
        self.binary_image = image

    def erosion(self, keep_sizes=False):
        # Algorithm:
        # define padding (see CSS, if dont understand or imagine it's margins), that was make with SE
        # make result image
        # iterate with SE on the binary image and fill the result image
        # overwrite the binary image by result image

        # meaning like in CSS
        # If you dont want to see, think that paddings're margins
        paddings = {
            'top': self.SE['core']['y'],
            'bottom': len(self.SE['shape']) - self.SE['core']['y'] - 1,
            'left': self.SE['core']['x'],
            'right': len(self.SE['shape'][0]) - self.SE['core']['x'] - 1,
        }

        # make pure result image
        height = len(self.binary_image) - paddings['top'] - paddings['bottom']
        width = len(self.binary_image[0]) - paddings['left'] - paddings['right']
        result_image = self.pure_canvas(height, width)

        # iterate with core of SE through each pixel fo image
        for y in range(paddings['top'], paddings['top'] + height):
            for x in range(paddings['left'], paddings['left'] + width):

                HITs_ctr = 0  # will count HITs

                # check for HITs
                for i, SE_line in enumerate(self.SE['shape']):
                    for j, SE_pixel in enumerate(SE_line):
                        offset_y = -self.SE['core']['y'] + i
                        offset_x = -self.SE['core']['x'] + j

                        if SE_pixel == self.positive_value and SE_pixel == self.binary_image[y + offset_y][
                            x + offset_x]:
                            HITs_ctr += 1

                # if FIT, fill core of SE in result image
                if HITs_ctr == self.SE['square']:
                    result_image[y - paddings['top']][x - paddings['left']] = self.positive_value

                # if only HIT, unfill core of SE in result image
                # this is unneeded operation, because result image already pure
                # I wrote it only for understanding
                elif HITs_ctr > 0:
                    result_image[y - paddings['top']][x - paddings['left']] = self.negative_value

        self.binary_image = result_image

        if keep_sizes:
            self.add_borders()

    def dilation(self, keep_sizes=False):
        # Algorithm:
        # define padding (see CSS, if dont understand or imagine it's margins), that was make with SE
        # make result image
        # iterate with SE on the binary image and fill the result image
        # overwrite the binary image by result image

        # meaning like in CSS
        # If you dont want to see, think that it's margins
        paddings = {
            'top': self.SE['core']['y'],
            'bottom': len(self.SE['shape']) - self.SE['core']['y'] - 1,
            'left': self.SE['core']['x'],
            'right': len(self.SE['shape'][0]) - self.SE['core']['x'] - 1,
        }

        # make pure result image
        height = len(self.binary_image) - paddings['top'] - paddings['bottom']
        width = len(self.binary_image[0]) - paddings['left'] - paddings['right']
        result_image = self.pure_canvas(height, width)

        # iterate with core of SE through each pixel fo image
        for y in range(paddings['top'], paddings['top'] + height):
            for x in range(paddings['left'], paddings['left'] + width):

                HIT = False

                # check for HITs
                for i, SE_line in enumerate(self.SE['shape']):
                    for j, SE_pixel in enumerate(SE_line):
                        offset_y = -self.SE['core']['y'] + i
                        offset_x = -self.SE['core']['x'] + j

                        if SE_pixel == self.positive_value and SE_pixel == self.binary_image[y + offset_y][
                            x + offset_x]:
                            HIT = True

                # if was HIT fill core of SE in result image
                # I dont need check for FIT, because all pixel will be paint each in his own time
                if HIT:
                    result_image[y - paddings['top']][x - paddings['left']] = self.positive_value

        self.binary_image = result_image

        if keep_sizes:
            self.add_borders()

    # dilation and erosion removes paddings (margins) from original image
    # this method was called to add missing borders
    def add_borders(self):
        top = self.SE['core']['y']
        bottom = len(self.SE['shape']) - self.SE['core']['y'] - 1
        left = self.SE['core']['x']
        right = len(self.SE['shape'][0]) - self.SE['core']['x'] - 1

        width = len(self.binary_image[0]) + left + right

        for i in range(len(self.binary_image)):
            self.binary_image[i] = [self.negative_value for i in range(left)] + self.binary_image[i] + [
                self.negative_value for i in range(right)]

        for i in range(top):
            self.binary_image.insert(0, [self.negative_value for i in range(width)])

        for i in range(bottom):
            self.binary_image.append([self.negative_value for i in range(width)])

    def opening(self, keep_sizes=False):
        self.erosion(keep_sizes)
        self.dilation(keep_sizes)

    def closing(self, keep_sizes=False):
        self.dilation(keep_sizes)
        self.erosion(keep_sizes)
