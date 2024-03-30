import time

from helium import *

from load.load import Load as file_load
from operation.operation_douyin import Operation

"""
 1. 用户作品针对性点赞收藏评论
 2. 视频点赞收藏评论
"""


class Douyin:

    def __init__(self, target_file_name, match_comment_file_name):
        self.is_login = False
        self.operate = Operation()
        self.link_items = file_load.load(target_file_name)
        self.match_comment_item_map = file_load.load_map(match_comment_file_name)

    def login(self):
        start_chrome('www.douyin.com')
        wait_until(Text('登录后免费畅享高清视频').exists)
        while True:
            exist = Text("登录后免费畅享高清视频").exists()
            if not exist:
                self.is_login = True
                print("登录成功")
                break
            else:
                time.sleep(3)
        time.sleep(6)
        press(DOWN)

    def search_video(self, operation_num):
        for link in self.link_items:
            print("正在处理: %s" % link)
            go_to(link)
            time.sleep(1)
            if operation_num == "1":
                # 点赞
                self.operate.video_click_like()
                # 评论
                self.operate.video_comment(self.match_comment_item_map)
            elif operation_num == "2":
                # 评论区评论+点赞
                self.operate.video_discuss_comment(self.match_comment_item_map)
        print("已完成")
