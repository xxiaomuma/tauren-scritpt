import time

from helium import *


def message():
    login()
    hover('私信')
    time.sleep(3)
    while True:
        messageItems = find_all(S("//div[@data-e2e='conversation-item']"))
        hover(messageItems[len(messageItems) - 1].web_element)
        time.sleep(1)
        notNull = Text('暂时没有更多了').exists()
        if notNull:
            messageTotalItems = messageItems
            print("私聊用户数量: " + str(len(messageItems)))
            break

    if len(messageTotalItems) > 0:
        for item in messageTotalItems:
            item.web_element.click()
            time.sleep(1)
            write("已私聊")
            press(ENTER)
            time.sleep(1)
            click("退出会话")
    print("私信操作完成")


def searchMember():
    searchKey = input("请选择你需要视频评论点赞的关键词:")
    login()
    searchElement = find_all(S("//input[@data-e2e='searchbar-input']"))
    write(searchKey, searchElement[0].web_element)
    click("搜索")

    wait_until(Text('综合').exists)
    click("用户")

    while True:
        time.sleep(3)
        memberItems = find_all(S("ul li div a"))
        # find_all(Window())[0]._driver.close()  # 关闭窗口
        hover(memberItems[len(memberItems) - 1].web_element)
        time.sleep(1)
        refreshMember = Text("服务异常，重新刷新拉取数据").exists()
        if refreshMember:
            click("刷新")
        notNull = Text('暂时没有更多了').exists()
        if notNull:
            memberTotalItems = memberItems
            print("搜索出用户数量: " + str(len(memberItems)))
            break

    if len(memberTotalItems) > 0:
        print("正在处理搜索用户:")
        memberHrefItems = [item.web_element.get_attribute("href") for item in memberTotalItems]
        memberIndex(memberHrefItems)
    print("已完成搜索关键词用户关注私信")


memberLink = []


def memberIndex(memberHrefItems) -> int:
    size = len(memberHrefItems)
    for index in range(size):
        link = memberHrefItems[index]
        if link in memberLink:
            continue
        elif not link.__contains__('user'):
            continue
        memberLink.append(link)
        go_to(link)
        wait_until(Button('私信').exists)
        memberName = find_all(S("h1 span span span span span span"))[0].web_element.text
        likeButtonExists = Button("关注").exists()
        if likeButtonExists:
            click(Button("关注"))
            print("关注" + memberName + "成功")
            time.sleep(3)
            click(Button("私信"))
            time.sleep(3)
            click(Button("私信"))
            time.sleep(3)
            write("您的视频太好看了")
            time.sleep(3)
            press(ENTER)
            print("私信" + memberName + "成功")
        else:
            print("已经关注了" + memberName)
    return size


def searchVideo():
    searchKey = input("请选择你需要视频评论点赞的关键词:")
    login()
    searchElement = find_all(S("//input[@data-e2e='searchbar-input']"))
    write(searchKey, searchElement[0].web_element)
    click("搜索")

    wait_until(Text('综合').exists)
    click("视频")
    click("筛选")
    click("最新发布")
    click("一天内")
    time.sleep(3)
    videoItems = find_all(S("//div[@data-home-video-id]"))
    videoItems[0].web_element.click()

    first = True
    while True:
        time.sleep(3)
        press(DOWN)
        time.sleep(3)
        likeItems = find_all(S("//div[@data-e2e-state='video-player-no-digged']"))
        if len(likeItems) > 0:
            doubleclick(likeItems[0].web_element)
            print("点赞成功")
        if first:
            commentItems = find_all(S("//div[@data-e2e='feed-comment-icon']"))
            commentItems[0].web_element.click()
            first = False
        time.sleep(1)
        press(ENTER)
        time.sleep(1)
        write("已评论")
        print("评论成功")
        press(ENTER)


def main():
    while True:
        print("请输入你需要的功能:")
        print("1.私信")
        print("2.搜索关键词用户关注私信")
        print("3.搜索关键词视频评论及点赞")
        num = input("请选择你需要的内容:")
        if num == "1":
            message()
        elif num == "2":
            searchMember()
        elif num == "3":
            searchVideo()
        else:
            print("输入有误")


def login():
    start_chrome('www.douyin.com')
    wait_until(Text('登录后免费畅享高清视频').exists)
    while True:
        exist = Text("登录后免费畅享高清视频").exists()
        if not exist:
            break
        else:
            time.sleep(3)
    time.sleep(6)


main()
