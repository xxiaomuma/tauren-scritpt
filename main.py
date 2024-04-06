from douyin.douyin import Douyin

dou_yin = Douyin("douyin.text", "match.text")


def select_platform():
    while True:
        print("平台:")
        print("1.抖音")
        print("2.快手")
        print("3.知乎")
        platform_num = input("请选择平台:")
        if platform_num == "1":
            dou_yin.login()
            select_douyin_function()
        elif platform_num == "2":
            print("建设中...")
        elif platform_num == "3":
            print("建设中...")
        else:
            print("输入有误")


def select_douyin_function():
    while True:
        print("抖音功能:")
        print("1.账户链接")
        print("2.视频链接")
        function_num = input("请选择抖音功能:")
        if function_num:
            select_douyin_operation(function_num)
        else:
            print("输入有误")


def select_douyin_operation(function_num):
    while True:
        print("抖音操作:")
        print("1.简单模式")
        print("2.评论模式")
        operation_num = input("请选择抖音操作:")
        if operation_num:
            if function_num == "1":
                dou_yin.search_account(operation_num)
            elif function_num == "2":
                while True:
                    if dou_yin.is_login:
                        dou_yin.search_video(operation_num)
                        break
        else:
            print("输入有误")


select_platform()
