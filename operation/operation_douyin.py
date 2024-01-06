import time

from helium import *


class Operation:

    @staticmethod
    def _match_comment(video_desc, match_comment_item_map):
        for key, value in match_comment_item_map.items():
            if key in video_desc:
                return value
        return ""

    @staticmethod
    def _get_comment_total_count(video_comment_count_text):
        return video_comment_count_text[video_comment_count_text.find("(") + 1:video_comment_count_text.find(")")]

    @staticmethod
    def video_click_like():
        time.sleep(3)
        like_label_items = find_all(S("//div[@data-e2e-state='video-player-no-digged']"))
        if len(like_label_items) > 0:
            press("z")
            print("点赞成功")
        else:
            print("该视频已经点赞啦")

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
        handle_video_discuss_comment_count = 20
        while True:
            video_comment_label_items = find_all(S("//div[@data-e2e='comment-item']"))
            video_comment_label_item_count = len(video_comment_label_items)
            if total_video_comment_count == 0 or video_comment_label_item_count <= 0:
                break
            handle_start_index = video_comment_label_item_count - handle_video_discuss_comment_count
            self._handle_video_discuss_comment(handle_start_index, video_comment_label_items, match_comment_item_map)
            # 悬浮
            hover(video_comment_label_items[video_comment_label_item_count - 1].web_element)
        self.video_comment(match_comment_item_map)

    def _handle_video_discuss_comment(self, handle_start_index, video_comment_label_items, match_comment_item_map):
        for index in range(len(video_comment_label_items) - handle_start_index):
            video_comment_item = video_comment_label_items[handle_start_index + index]
            comment_class = video_comment_item.web_element.get_attribute("class")
            try:
                comment_text = find_all(S("." + comment_class + " div div div span span span span span span span"))[
                    handle_start_index + index].web_element.text
                if len(comment_text) > 0:
                    match_comment_text = self._match_comment(comment_text, match_comment_item_map)
                    if len(match_comment_text) > 0:
                        click(find_all(S("." + comment_class + " .dy-tip-container"))[handle_start_index + index].web_element)
                        write(comment_text)
            except IndexError as e:
                continue

    @staticmethod
    def _video_discuss_comment_click_like():
        print("简单的操作")
