"""
  读取文件
"""
import os


class Load:

    @staticmethod
    def load(file_name):
        dir = os.getcwd()
        file_path = dir + "\\" + file_name
        print("读取文件信息: " + file_path)
        link_items = []
        with open(file_path, 'r', encoding="utf-8") as file:
            for line in file:
                link_items.append(line.strip())
        return link_items

    @staticmethod
    def load_map(file_name):
        dir = os.getcwd()
        file_path = dir + "\\" + file_name
        print("读取文件信息: " + file_path)
        link_item_map = {}
        with open(file_path, 'r', encoding="utf-8") as file:
            for line in file:
                line_items = line.strip().split(">")
                link_item_map[line_items[0]] = line_items[1]
        return link_item_map
