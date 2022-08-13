import os
from tkinter import *
import tkinter.messagebox
import requests
from bs4 import BeautifulSoup
import pyperclip

# 目录获取
def lists(url):
    names2 = []
    urls2 = []
    header = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Mobile Safari/537.36'}
    a = requests.get(url, headers=header).text
    b = BeautifulSoup(a, 'html.parser').find('div', id='list')
    c = b.find('dl')
    d = c.find_all('dd')
    n = 0
    for e in d:
        if n < 12:
            n += 1
            continue
        name = e.find('a').text  # 获取书名
        u = e.find('a')['href']  # 获取书链接
        names2.append(name)  # 存入书名
        urls2.append('https://www.biqudu.net' + u)  # 存入书链接
    return names2, urls2  # 返回书名及链接


# 保存收藏的书名及链接
def join(n, u):
    a = open('book', 'r')  # 以只读打开存储文件
    c = a.read()  # 读取
    a.close()  # 关闭
    # 尝试转化为json
    try:
        b = eval(c)
    except:
        b = {}  # 如果文件为空
    b[n] = u  # 加入书名及链接
    a = open('book', 'w')  # 以写入打开存储文件
    a.write(str(b))  # 将json格式转化为str并写入
    a.close()  # 关闭


# 读取收藏文件
def r():
    r = open('book', 'r')  # 以只读打开存储文件
    rr = eval(r.read())  # 转化为json
    r.close()  # 关闭
    return rr  # 返回收藏json


# 搜索
def sc(ss):
    url = "https://www.biqudu.net/searchbook.php?keyword=" + str(ss)  # 搜索链接
    header = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Mobile Safari/537.36'}
    web = requests.get(url, headers=header)  # get请求
    a = BeautifulSoup(web.text, 'html.parser')
    d = a.find('div', class_="novelslist2")
    b = d.find_all("li")
    urls = []
    names = []
    for c in b:
        try:
            e = c.find('span', class_="s2").find('a')
            urls.append('https://www.biqudu.net' + e['href'])
            names.append(e.text)
        except:
            pass
    return urls, names


# 收藏gui
def bookw():
    bk = r()
    root3 = Tk()
    width = 390
    hight = 600
    sreen_width = root3.winfo_screenwidth()
    sreen_hight = root3.winfo_screenheight()
    x = int((sreen_width - width) / 2)
    y = int((sreen_hight - hight) / 2)
    root3.title('书架')
    root3.geometry('%sx%s+%s+%s' % (width, hight, x-390, y))
    root3.resizable(0, 0)
    var = StringVar()
    scrollbar = Scrollbar(root3)
    list = Listbox(root3, listvariable=var)
    scrollbar.pack(side=RIGHT, fill=Y)
    list.pack(fill=BOTH, expand=YES)
    scrollbar.config(command=list.yview)
    list.config(yscrollcommand=scrollbar.set)
    urls = []
    names = []
    # 读取收藏
    for k, v in bk.items():
        names.append(k)
        urls.append(v)
    # 写入收藏的书名
    for i in names:
        list.insert(END, i)

    def myPrint(self):
        number = list.curselection()[0]
        name = list.get(list.curselection())
        root1(urls[int(number)], name, names)  # 打开目录界面

    list.bind("<Double-Button-1>", myPrint)  # 绑定双击


# 主界面gui
def root():
    # 判断有无目录没有则创建
    try:
        os.listdir('./记录')
    except:
        os.mkdir('记录')
    # 判断有无book文件， 没有则创建
    try:
        a = open('book', 'r')
        a.close()
    except:
        a = open('book', 'w')
        a.write('{}')
        a.close()
    root = Tk()
    width = 390
    hight = 600
    sreen_width = root.winfo_screenwidth()
    sreen_hight = root.winfo_screenheight()
    x = int((sreen_width - width) / 2)
    y = int((sreen_hight - hight) / 2)
    root.title('笔趣阁')  # 标题
    root.geometry('%sx%s+%s+%s' % (width, hight, x, y))
    root.resizable(0, 0)

    # 打开收藏界面
    def bks():
        bookw()

    frame = Frame(root)
    search_entry = Entry(frame, width=30)
    search_entry.grid(row=0, column=0)
    buttom = Button(frame, text="搜索", relief=FLAT)
    buttom.grid(row=0, column=1)
    Button(frame, text='书架', command=bks, relief=FLAT).grid(row=0, column=3)
    frame.pack()
    listframe = Frame()
    var = StringVar()
    scrollbar = Scrollbar(listframe)
    scrollbar.pack(side=RIGHT, fill=Y)
    list = Listbox(listframe, listvariable=var, yscrollcommand=scrollbar.set)
    list.pack(fill=BOTH, expand=YES)

    def s():
        global urls
        try:
            list.delete(0, END)
        except:
            pass
        if search_entry.get() == '':
            tkinter.messagebox.askquestion(title='错误', message='搜索框不能为空')
        urls, names = sc(search_entry.get())
        if urls == [] and names == []:
            tkinter.messagebox.askquestion(title='错误', message='没有搜索到与之相关的书籍')
        for a in names:
            list.insert(END, a)

    buttom['command'] = s

    def myPrint(self):
        number = list.curselection()[0]
        name = list.get(list.curselection())
        names1 = []
        try:
            bk = r()
            for k, v in bk.items():
                names1.append(k)
        except:
            pass
        root1(urls[int(number)], name, names1)

    list.bind("<Double-Button-1>", myPrint)

    def k(self):
        s()

    search_entry.bind("<Return>", k)
    listframe.pack(fill=BOTH, expand=YES)
    mainloop()


def root1(url, name1, names1):
    n = os.listdir('./记录/')
    root1 = Tk()
    width = 390
    hight = 600
    sreen_width = root1.winfo_screenwidth()
    sreen_hight = root1.winfo_screenheight()
    x = int((sreen_width - width) / 2)
    y = int((sreen_hight - hight) / 2)
    root1.geometry('%sx%s+%s+%s' % (width, hight, x+390, y))
    root1.resizable(0, 0)
    root1.title('目录')
    listsframe = Frame(root1)
    var = StringVar()
    scrollbar = Scrollbar(listsframe)
    list1 = Listbox(listsframe, listvariable=var)
    scrollbar.config(command=list1.yview)
    list1.config(yscrollcommand=scrollbar.set)
    scrollbar.pack(side=RIGHT, fill=Y)
    list1.pack(fill=BOTH, expand=YES)
    scrollbar.config(command=list1.yview)
    list1.config(yscrollcommand=scrollbar.set)
    names, urls = lists(url)
    frame2 = Frame(root1)
    for a in names:
        list1.insert(END, a)

    def cc():
        f = open('./记录/' + name1, 'r').read()
        readw(urls, int(f), name1, names)

    def jj():
        join(name1, url)
        tkinter.messagebox.showinfo(message='加入成功')
        bbb.destroy()

    bb = 0
    c = 0
    for kk in names1:
        if name1 == kk:
            c = 1
    for i in n:
        if name1 == i:
            Button(frame2, text='继续上一次阅读', command=cc, relief=FLAT).grid(row=0, column=0)
            if c == 0:
                bbb = Button(frame2, text='加入书架', command=jj, relief=FLAT)
                bbb.grid(row=0, column=2)
            bb = 1
        elif bb == 0 and c == 0:
            bb = 2
    if bb == 2:
        bbb = Button(frame2, text='加入书架', command=jj, relief=FLAT)
        bbb.grid(row=0, column=1)

    def myPrint(self):
        number = list1.curselection()[0]  # 提取点中选项的下标
        readw(urls, number, name1, names)

    list1.bind("<Double-Button-1>", myPrint)
    listsframe.pack(fill=BOTH, expand=YES)
    frame2.pack()


def readt(url, rule):
    header = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Mobile Safari/537.36'}
    a = requests.get(url)
    b = BeautifulSoup(a.text, 'html.parser')
    c = str(b.find('div', class_="box_con").find('div', id="content"))
    s = eval(rule)
    for k, v in s.items():
        c = c.replace(k, s[k])
    return c


def readw(urls, number, name, names):
    try:
        rules = open('rule.josn', 'r')
        rule = rules.read()
        rules.close()
        if rule == '':
            rule = '''{
                '<br/>': '\\n',
                '<div id="content">': "",
                '<script>chaptererror();</script>': '',
                '</div>': '',
                '　　手机用户请浏览m.1biquge.com　阅读，更优质的阅读体验。': '',
                '\\n				　　一秒记住【笔趣阁　】\\n':'',
                '手机用户请浏览m.1biquge.com　阅读，更优质的阅读体验。': '',
                '\\n				　　一秒记住【笔趣阁　】为您提供最快更新！\\n': '',
                '水印广告测试': '',
                '\\n				　　readx();': ''
            }'''
            rules.write(rule)
            rules.close()
    except:
        rules = open('rule.json', 'w')
        rule = '''{
        '<br/>': '\\n',
        '<div id="content">': "",
        '<script>chaptererror();</script>': '',
        '</div>': '',
        '　　手机用户请浏览m.1biquge.com　阅读，更优质的阅读体验。': '',
        '\\n				　　一秒记住【笔趣阁　】\\n':'',
        '手机用户请浏览m.1biquge.com　阅读，更优质的阅读体验。': '',
        '\\n				　　一秒记住【笔趣阁　】为您提供最快更新！\\n': '',
        '水印广告测试': '',
        '\\n				　　readx();': ''
    }'''
        rules.write(rule)
        rules.close()
    url = urls[int(number)]
    try:
        f = open('./记录/' + name, 'r+')
        e = f.read()
        w = open('./记录/' + name, 'w')
        w.write(str(number))
        w.close()
    except:
        w = open('./记录/' + name, 'w')
        w.write(str(number))
        w.close()
    root2 = Tk()
    root2.title('阅读')
    width = 844
    hight = 944
    sreen_width = root2.winfo_screenwidth()
    sreen_hight = root2.winfo_screenheight()
    x = int((sreen_width - width) / 2)
    y = int((sreen_hight - hight) / 2)
    root2.geometry('%sx%s+%s+%s' % (width, hight, x, y-40))
    frame = Frame(root2)
    a = readt(url, rule)
    scrollbar = Scrollbar(frame)
    text = Text(frame, font=("Purisa", 20))
    scrollbar.pack(side=RIGHT, fill=Y)
    text.tag_config('center', justify='center', font=("Purisa", 30))
    text.insert('insert', names[number] + '\n\n', 'center')
    scrollbar.config(command=text.yview)
    text.config(yscrollcommand=scrollbar.set)
    text.insert('insert', a)
    text.config(state='disabled')
    text.pack(fill=BOTH, expand=YES)
    frame.pack(fill=BOTH, expand=YES)
    frame2 = Frame(root2)
    def ret():
        n = int(open('./记录/' + name, 'r').read()) - 1
        try:
            if n<0:
                tkinter.messagebox.showinfo(title='提示', message='没有了')
            else:
                b = urls[n]
                open('./记录/' + name, 'w').write(str(n))
                a = readt(b, rule)
                text.config(state='normal')
                text.delete('1.0', 'end')
                text.insert('insert', names[n]+'\n\n', 'center')
                text.insert('insert', a)
                text.config(state='disabled')
        except:
            tkinter.messagebox.showinfo(title='提示', message='没有了')
    def next():
        n = int(open('./记录/' + name, 'r').read()) + 1
        try:
            b = urls[n]
            open('./记录/' + name, 'w').write(str(n))
            a = readt(b, rule)
            text.config(state='normal')
            text.delete("1.0", 'end')
            text.insert('insert', names[n] + '\n\n', 'center')
            text.insert('insert', a)
            text.config(state='disabled')
        except:
            tkinter.messagebox.showinfo(title='提示', message='没有了')
            pass
    # def pb():
    #     text.event_generate('<<Copy>>')
    #     p = pyperclip.paste().encode('gbk').decode('utf-8')
    #     print(p)
    # menu =Menu(frame, tearoff=0)
    # menu.add_command(label='屏蔽', command=pb)
    # def mm(event):
    #     menu.post(event.x_root, event.y_root)
    # text.bind('<Button-3>', mm)
    Button(frame2, text='上一章', command=ret, font=("Purisa", 20), relief=FLAT).grid(row=0, column=0)
    Button(frame2, text='下一章', command=next, font=("Purisa", 20), relief=FLAT).grid(row=0, column=1)
    frame2.pack()
    root2.mainloop()


if __name__ == '__main__':
    header = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Mobile Safari/537.36'}
    try:
        a = requests.get('https://www.biqudu.net/', headers=header)
        root()
    except:
        tkinter.messagebox.showerror(title='错误', message='连接失败\n请检查网络连接')
