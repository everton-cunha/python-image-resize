import os
import threading
import json
import PIL
from PIL import Image
import urllib.request


class PhotoResize:
    def __init__(self):
        self.photo_list = []
    
    def json_load(self, json_file):
        print("Downloads ... \n")
        with open(json_file) as file:
            self.photo_list = json.load(file)
        for j in self.photo_list['photos']:
            print(j['name'], j['url'])

    def download_photo(self, file_name, url):
        if file_name and url:
            try:
                urllib.request.urlretrieve(url, file_name)
            except:
                return ValueError("error")
        else:
            return ValueError("Error: File Name and/or Url empty")
        return None

    def photo_resize(self, save_path, file_name, widths, heights):
        img = Image.open(file_name)
        size = widths, heights 
        img = img.resize(size, PIL.Image.ANTIALIAS)
        img.save(save_path + str(widths) + "_" + str(heights) + str(file_name))
        return   


    def resize_photo_list(self, file_name):
        heights_widths = [ [900, 540], [110, 65], [100, 80], [415, 311], [300, 250], [620, 372],
         [60, 45], [300, 225], [300, 250], [158, 158], [100, 80], [115, 113], [150, 113] ]

        new_photos_path = '{}/new_photos/'.format(os.path.abspath(os.path.dirname(__file__)))
        
        if file_name:
            threads = []
            print("Photo " + file_name + " resize ... \n")
            try:
                for hw in heights_widths:
                    #self.photo_resize(new_photos_path, file_name, hw[0], hw[1])
                    t = threading.Thread(target = self.photo_resize, args= (new_photos_path, file_name, hw[0], hw[1]))
                    threads.append(t)
                    t.start()
                for t in threads:
                    t.join()
            except:
                return ValueError("Error: Resize " + str(file_name))


if __name__ == "__main__":
    p = PhotoResize()
    p.json_load("photos_array.json")
    if p.photo_list:
        for j in p.photo_list['photos']:
            p.download_photo(j['name'], j['url'])
            error = p.resize_photo_list(j['name'])
            if error:
                print(error)

