import cv2
import os
import shutil
import re


class File(object):
    def __init__(self, file_path, file_name):
        self.file_path = file_path
        self.file_name = file_name

class PathSet(object):
    def __init__(self, src_path, dst_path, is_dir):
        self.src_path = src_path
        self.dst_path = dst_path
        self.is_dir = is_dir

    def get_src_file_path(self):
        if self.is_dir is False:
            return None
        else:
            for file_name in os.listdir(self.src_path):
                src_file_path = os.path.join(self.src_path, file_name)
                dst_file_path = os.path.join(self.dst_path, file_name)
                file_path_set = PathSet(src_file_path, dst_file_path, False)
                yield file_path_set
        return None

class CarCorrection(object):

    def __init__(self):

        name = input('Enter the directory name to be solved\n输入需要处理的文件夹名：\n')
        this_path = os.path.abspath('.')
        source_path = os.path.join(this_path, name)
        while not os.path.exists(source_path):
            print('Directory: ', name, ' do not exist.')
            name = input('输入正确的文件夹名：\n')
            this_path = os.path.abspath('.')
            source_path = os.path.join(this_path, name)
        dst_path = os.path.join(this_path, name + '_Solved')

        self._path_set = PathSet(source_path, dst_path, True)
        self._reserve_count = 0
        self._corrected_count = 0
        self._all_solved_count = 0

    def start_working(self):
        self.reserve_process()
        self.correct_process()
        self.print_count()

    def reserve_process(self):

        print(" 进入选择保留过程，图片将依次展示，若保留则按1，删除则按0，中断按2（中断后重启将重新处理），处理过的图片会出现在.\<name>_solved")

        if os.path.exists(self._path_set.dst_path):
            shutil.rmtree(self._path_set.dst_path)
        os.mkdir(self._path_set.dst_path)

        for file_path_set in self._path_set.get_src_file_path():
            image = cv2.imread(file_path_set.src_path, cv2.IMREAD_REDUCED_COLOR_4)
            window = cv2.namedWindow("Reserve: Push 1 | Delete: Push 0", cv2.WINDOW_AUTOSIZE)
            try:
                cv2.imshow("Reserve: Push 1 | Delete: Push 0", image)
            except:
                continue
            result = cv2.waitKey(0)

            while result != 48 and result != 49 and result != 50:
                result = cv2.waitKey(0)
            if result == 49:
                shutil.copy(file_path_set.src_path, file_path_set.dst_path)
                self._reserve_count = self._reserve_count + 1
            elif result == 50:
                break
            else:
                pass

            self._all_solved_count = self._all_solved_count + 1
            cv2.destroyAllWindows()

        cv2.destroyAllWindows()

    def correct_process(self):

        print(" 进入标签修改过程，图片将依次展示，若有问题请按1后：颜色：w：白色 b：黑色 d: 灰色 g：绿 y: 黄 r：红色 l:蓝色"
              " 0：轿车 1：小型普通客车 2：中型普通客车 3：大型普通客车 4: 轻型普通货车"
              " 没问题请按0"
              )

        for file_path_and_name in self.get_file_from_path(self._path_set.dst_path):
            #Show a picture.
            image = cv2.imread(file_path_and_name.file_path, cv2.IMREAD_REDUCED_COLOR_4)
            window = cv2.namedWindow(file_path_and_name.file_name, cv2.WINDOW_AUTOSIZE)
            try:
                cv2.imshow(file_path_and_name.file_name, image)
            except:
                continue

            print(file_path_and_name.file_name)

            #Judge the tag
            result = cv2.waitKey(0)
            while result != 48 and result != 49 and result != 50:
                result = cv2.waitKey(0)

            if result == 49:
                print("进入修改")
                self._corrected_count = self._corrected_count + 1
                color_key = cv2.waitKey(0)
                # print(color_key)

                # car color
                # w:119 b:98 d:100 g:103 y:121 r:114 l:98
                # Input for color and car types.
                while color_key != 119 and \
                    color_key != 98 and \
                    color_key != 100 and \
                    color_key != 103 and \
                    color_key != 121 and \
                    color_key != 114 and \
                        color_key != 108:
                    color_key = cv2.waitKey(0)

                # car type
                car_type_key = cv2.waitKey(0)
                # print(car_type_key)
                while car_type_key < 48 or car_type_key > 52:
                    car_type_key = cv2.waitKey(0)

                #Get new tag
                new_file_name = self._get_name_string(file_path_and_name.file_name, color_key, car_type_key)
                print("更改为：", new_file_name)
                #Correct the wrong tag
                old_file_path = file_path_and_name.file_path
                new_file_path = os.path.join(self._path_set.dst_path, new_file_name)
                os.rename(old_file_path, new_file_path)
            else:
                pass
            cv2.destroyAllWindows()

    def _get_name_string(self, old_file_name, color_key, car_type_key):
        # w:119 b:98 d:100 g:103 y:121 r:114
        # Input for color and car types.
        color_str = "错误"
        car_type_str = "错误"
        if color_key == 119:
            color_str = "白"
        elif color_key == 98:
            color_str = "黑"
        elif color_key == 100:
            color_str = "灰"
        elif color_key == 103:
            color_str = "绿"
        elif color_key == 121:
            color_str = "黄"
        elif color_key == 114:
            color_str = "红"
        elif color_key == 108:
            color_str = "蓝"
        else:
            pass

        if car_type_key == 48:
            car_type_str = "轿车"
        elif car_type_key == 49:
            car_type_str = "小型普通客车"
        elif car_type_key == 50:
            car_type_str = "中型普通客车"
        elif car_type_key == 51:
            car_type_str = "大型普通客车"
        elif car_type_key == 52:
            car_type_str == "轻型普通货车"
        else:
            pass

        id = re.search("[0-9]+",old_file_name)
        some_other_message = re.search("_[^_]{2,}_[^_]+_",old_file_name)

        return id[0] + "_" + color_str + some_other_message[0] + car_type_str + ".jpg"

    #TODO: This method should be moved to somewhere.
    def get_file_from_path(self, path):
        for filename in os.listdir(path):
            new_file = File(os.path.join(path, filename), filename)
            yield new_file
        return None

    def print_working_path(self):
        print("Dstpath is ", self._path_set.dst_path)
        print("Srcpath is", self._path_set.src_path)

    def print_count(self):
        print(self._all_solved_count, " pictures have been solved!")
        print(self._reserve_count, " pictures reserved!")
        print(self._corrected_count, " pictures have been corrected!")





if __name__ == '__main__':
    new_car_Correction = CarCorrection()
    new_car_Correction.print_working_path()
    new_car_Correction.start_working()
