import time
from helium import *


class Operation:

    #
    # 用户作品评论
    #
    def user_video_comment(self, operation_num, match_video_items, match_comment_item_map):
        total_user_video_count = int(find_all(S("//span[@data-e2e='user-tab-count']"))[0].web_element.text)
        if total_user_video_count > 0:
            while True:
                user_video_label_items = find_all(S("//div[@data-e2e='user-post-list']/ul[@data-e2e='scroll-list']/li"))
                user_video_label_item_count = len(user_video_label_items)
                if total_user_video_count == 0 or user_video_label_item_count <= 0:
                    break
                self._handle_user_video_comment(operation_num, user_video_label_items, match_video_items, match_comment_item_map)
                hover(user_video_label_items[user_video_label_item_count].web_element)
        print("评论成功")

    #
    # 视频评论
    #
    def video_comment(self, match_comment_item_map):
        time.sleep(3)
        video_desc_label_items = find_all(S("//div[@data-e2e='video-desc']"))
        if len(video_desc_label_items) > 0 and len(match_comment_item_map.keys()) > 0:
            video_desc = video_desc_label_items[0].web_element.text
            match_comment_text = self._match_comment(video_desc, match_comment_item_map)
            if len(match_comment_text) > 0:
                press("x")
                time.sleep(1)
                write(match_comment_text)
                press(ENTER)
        print("评论成功")

    #
    # 视频评论区评论
    #
    def video_discuss_comment(self, match_comment_item_map):
        time.sleep(3)
        press("x")
        total_video_comment_count = 0
        video_comment_count_label_items = find_all(S('.comment-header-inner-container'))
        if len(video_comment_count_label_items) > 0:
            # '大家都在搜：泰山爬到山顶需要几小时全部评论(28710)'
            video_comment_count_text = video_comment_count_label_items[0].web_element.text
            total_video_comment_count = self._get_comment_total_count(video_comment_count_text)
        # 20初始化
        comment_class = ""
        comment_context_class = ""
        while True:
            time.sleep(3)
            video_comment_label_items = find_all(S("//div[@data-e2e='comment-item']"))
            video_comment_label_item_count = len(video_comment_label_items)
            if total_video_comment_count == 0 or video_comment_label_item_count <= 0:
                break
            if len(comment_class) <= 0 or len(comment_context_class) <= 0:
                elect_video_comment_label_item = video_comment_label_items[0]
                # 获取内容class
                comment_class = elect_video_comment_label_item.web_element.get_attribute("class")
                print("获取内容class:", comment_class)
                # 获取评论class
                elect_video_comment_context_label_items = find_all(S("." + comment_class + " > div > div > div"))
                comment_context_class = elect_video_comment_context_label_items[1].web_element.get_attribute("class")
                print("获取评论class:", comment_context_class)
            self._handle_video_discuss_comment(video_comment_label_item_count,
                                               comment_class, comment_context_class,
                                               match_comment_item_map)
            # 悬浮
            hover(video_comment_label_items[video_comment_label_item_count].web_element)
        self.video_comment(match_comment_item_map)

    #
    # 处理用户作品评论
    #
    def _handle_user_video_comment(self, operation_num, user_video_label_items, match_video_items, match_comment_item_map):
        handle_count = len(user_video_label_items)
        for index in range(handle_count):
            try:
                time.sleep(3)
                user_video_label_item = user_video_label_items[index].web_element
                user_video_text = user_video_label_item.text
                is_match_video = self._match_video(user_video_text, match_video_items)
                if is_match_video:
                    print("正在处理作品:", user_video_text)
                    user_video_label_item.click()
                    time.sleep(3)
                    if operation_num == "1":
                        self.video_comment(match_comment_item_map)
                    else:
                        self.video_discuss_comment(match_comment_item_map)
                    find_all(S(".isDark"))[0].web_element.click()
            except IndexError as e:
                print("err: {e}")
                continue

    #
    # 处理视频评论区评论
    #
    def _handle_video_discuss_comment(self, handle_count, comment_class, comment_context_class, match_comment_item_map):
        for index in range(handle_count):
            try:
                video_comment_context_label_item = find_all(S("." + comment_class + " ." + comment_context_class))[
                    index]
                comment_text = video_comment_context_label_item.web_element.text
                match_comment_text = self._match_comment(comment_text, match_comment_item_map)
                print("正在处理:", comment_text)
                if len(match_comment_text) > 0:
                    response_label_items = find_all(S("." + comment_class + " .dy-tip-container"))
                    click(response_label_items[index].web_element)
                    click("留下你的精彩评论吧")
                    write(match_comment_text)
                    press(ENTER)
            except IndexError as e:
                print("err: {e}")
                continue

    #
    # 视频点赞
    #
    @staticmethod
    def video_click_like():
        time.sleep(3)
        like_label_items = find_all(S("//div[@data-e2e-state='video-player-no-digged']"))
        if len(like_label_items) > 0:
            press("z")
            print("点赞成功")
        else:
            print("该视频已经点赞啦")

    #
    # 用户关注
    #
    @staticmethod
    def user_click_follow():
        time.sleep(3)
        follow_exist = Text("关注").exists()
        if not follow_exist:
            follow_exist = Text("回关").exists()
            if not follow_exist:
                print("该用户已关注啦")
            else:
                click("回关")
                print("回关成功")
        else:
            click("关注")
            print("关注成功")

    #
    # 匹配消息
    #
    @staticmethod
    def _match_comment(video_desc, match_comment_item_map):
        for key, value in match_comment_item_map.items():
            if key in video_desc:
                return value
        return ""

    #
    # 匹配视频
    #
    @staticmethod
    def _match_video(video_desc, match_video_items):
        for match_video_item in match_video_items:
            if match_video_item in video_desc:
                return True
        return False

    #
    # 获取内容评论总条数
    #
    @staticmethod
    def _get_comment_total_count(video_comment_count_text):
        return video_comment_count_text[video_comment_count_text.find("(") + 1:video_comment_count_text.find(")")]


