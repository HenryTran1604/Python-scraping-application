import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from eventHandler import *
import threading
import webbrowser
class Window(tk.Tk):
    def __init__(self, productList):
        self.productList = productList
        tk.Tk.__init__(self)
        self.title('TEAM 16 - Python scraping')
        self.geometry(self.get_position(800, 500))
        self.resizable(False, False)
        #Create personal style
        self.style = ttk.Style()
        self.style.theme_create("Tab", parent="alt", settings={
            "TNotebook": {"configure": {"tabmargins": [2, 5, 2, 0]}},
            "TNotebook.Tab": {
                "configure": {"padding": [5, 4], "background": '#d2ffd2'},
                "map": {"background": [("selected", '#FF8C00')],
                        "expand": [("selected", [1, 1, 1, 0])]}}})
        self.style.theme_use("Tab")
        self.myfont = ('Inter', '11', 'bold')
        self.initPage()

    def get_position(self, window_width, window_height):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        position_top = int(screen_height / 2 - window_height / 2)
        position_right = int(screen_width / 2 - window_width / 2)
        return f'{window_width}x{window_height}+{position_right}+{position_top}'
    
    def accessToGithub(self):
        webbrowser.open("https://github.com/Team-16-Python-Scraping/final-python-scraping.git")

    def showProgressBar(self):
        self.win = tk.Toplevel()
        self.win.title('Đang xử lý...')
        self.win.attributes("-topmost", True)
        self.win.geometry(self.get_position(300, 120))
        self.win.resizable(False, False)
        self.pb = ttk.Progressbar(
            self.win,
            orient='horizontal',
            mode='indeterminate',
            length=280
        )
        self.pb.grid(row=0, column=0, columnspan=2, padx=10, pady=20)
        cancel_button = ttk.Button(
            self.win,
            text='Cancel',
            command=self.win.destroy
        )
        cancel_button.grid(column=0, row=1, padx=10, pady=10, sticky=tk.E)
        self.pb.start()

    def endProgressBar(self):
        self.pb.destroy()
        self.win.destroy()

    def create_tab1(self):
        self.tab1 = ttk.Frame(self.tabControl)
        ttk.Label(self.tab1)  # root for shopee
        self.lbSearch = tk.Label(self.tab1, text='Nhập tên sản phẩm: ', font=self.myfont)
        self.eSearch = tk.Entry(self.tab1, width=70, font=self.myfont)
        self.frame = tk.LabelFrame(self.tab1, text='Danh sách thuộc tính cần lấy về', width=500, height=200)

        self.lbSearch.place(x=10, y=10)
        self.eSearch.focus()
        self.eSearch.place(x=180, y=10)
        self.frame.place(x=10, y=50)

        checkVar = tk.IntVar(value=1)
        self.ckbName = ttk.Checkbutton(self.frame, text='Tên sản phẩm', state=tk.DISABLED, variable=checkVar)
        self.ckbMinPrice = ttk.Checkbutton(self.frame, text='Giá nhỏ nhất', state=tk.DISABLED, variable=checkVar)
        self.ckbMaxPrice = ttk.Checkbutton(self.frame, text='Giá lớn nhất', state=tk.DISABLED, variable=checkVar)
        self.ckbRating = ttk.Checkbutton(self.frame, text='Đánh giá (sao)', state=tk.DISABLED, variable=checkVar)
        self.ckbLink = ttk.Checkbutton(self.frame, text='Link sản phẩm', state=tk.DISABLED, variable=checkVar)

        self.ckbName.place(x=15, y=10)
        self.ckbMinPrice.place(x=15, y=45)
        self.ckbMaxPrice.place(x=15, y=80)
        self.ckbRating.place(x=15, y=115)
        self.ckbLink.place(x=15, y=150)

        self.lbNumberOfPage = tk.Label(self.tab1, text='Số trang muốn lấy dữ liệu: ')
        self.eNumberOfPage = tk.Entry(self.tab1, width=20, textvariable=tk.IntVar(value=1))
        self.lbNumberOfPage.place(x=10, y=265)
        self.eNumberOfPage.place(x=170, y=265)

        self.imgLogo = ImageTk.PhotoImage(Image.open('data/Img/logoshopee.png').resize((205, 205)))
        self.lbLogo = tk.Label(self.tab1, image=self.imgLogo)

        self.lbLogo.place(x=550, y=45)

        self.btnSearch = tk.Button(self.tab1, text='TRA CỨU!', font=self.myfont, command= lambda: threading.Thread(target=accessToShopee, args=(self, self.eNumberOfPage.get(), self.eSearch.get())).start())
        self.lbCopyRight = tk.Label(self.tab1, text='@2022 - team 16 PTIT',
                               height=2, bg='black', fg='white',
                               font=self.myfont, relief=tk.SUNKEN, width=self.winfo_screenwidth(), anchor=tk.W)
        self.btnSearch.place(x=550, y=270)
        self.lbCopyRight.pack(side='bottom', fill='y')
        return self.tab1

    def create_tab2(self):
        self.tab2 = ttk.Frame(self.tabControl)
        ttk.Label(self.tab2)

        self.lbUrl = tk.Label(self.tab2, text='Nhập url bạn muốn lấy ảnh: ', font=self.myfont)
        self.lbLimit = tk.Label(self.tab2, text='Nhập số lượng tối đa ảnh: \n(Bỏ trống nếu muốn lấy tất cả)')
        self.eLimit = tk.Entry(self.tab2, width=20, font=self.myfont)
        self.eUrl = tk.Entry(self.tab2, width=65, font=self.myfont)
        self.btnSearch2 = tk.Button(self.tab2, text='Lấy ảnh!', font=self.myfont, command=lambda :threading.Thread(target=downloadImages, args=(self, self.eUrl.get(), './data/downloadedImages', self.eLimit.get())).start())

        self.lbUrl.place(x=10, y=10)
        self.lbLimit.place(x=10, y=50)
        self.eUrl.focus_set()
        self.eUrl.place(x=220, y = 10)
        self.eLimit.place(x=220, y=50)
        self.btnSearch2.place(x=650, y = 80)

        self.lbCopyRight = tk.Label(self.tab2, text='@2022 - team 16 PTIT',
                               height=2, bg='black', fg='white',
                               font=self.myfont, relief=tk.SUNKEN, width=self.winfo_screenwidth(), anchor=tk.W)

        self.lbCopyRight.pack(side='bottom', fill='y')
        return self.tab2

    def initPage(self):
        # Insert picture as background
        maxsize = (800, 500)
        self.img = Image.open('data/Img/background.jpg')
        self.img = self.img.resize(maxsize)
        self.bg = ImageTk.PhotoImage(self.img)
        self.rootImg = tk.Label(self, image=self.bg)
        self.rootImg.place(in_=self, x=0, y=0)
        # Button about us for more infor
        self.btn_about_us = tk.Button(self, text='ABOUT US', bg='black',
                               fg='white', width=9, height=2,
                               font=('Inter', 10, 'bold'),command=self.accessToGithub)
        self.btn_about_us.pack(pady=2, anchor='e')

        self.tabControl = ttk.Notebook(self)
        self.tab1 = self.create_tab1()
        self.tab2 = self.create_tab2()
        self.s = ttk.Style()
        self.s.configure('TNotebook.Tab', font=self.myfont)

        self.tabControl.add(self.tab1, text='Get product from shopee')
        self.tabControl.add(self.tab2, text='Get image from URL', )
        self.tabControl.pack(expand=1, fill="both")
        # self.mainloop()


    def clearTreeView(self):
        for i in self.productTree.get_children():
            self.productTree.delete(i)


    def fillTreeView(self):
        contacts = []
        for i in range(0, len(self.productList)):
            contacts.append((i+1, self.productList[i].name, self.productList[i].minPrice, self.productList[i].maxPrice,
                            self.productList[i].sales, '%.1f' % self.productList[i].rating, self.productList[i].link))
        self.productTree.tag_configure('oddrow', background="#7DE5ED")
        self.productTree.tag_configure('evenrow', background="white")
        count = 0
        for contact in contacts:
            if (count % 2 == 0):
                self.productTree.insert('', tk.END, values=contact, tags="oddrow")
            else:
                self.productTree.insert('', tk.END, values=contact, tags="evenrow")
            count += 1


    def showProducts(self):  # ProductTable
        self.table = tk.Toplevel()
        # self.table.attributes('-topmost', True)
        self.table.title('Danh sách sản phẩm')
        self.table.geometry("1280x424")
        self.table.resizable(False, False)
        # Construct Treeview
        columns = ['S_T_T', 'Tên_sản_phẩm', 'Giá_nhỏ_nhất',
                'Giá_lớn_nhất', 'Đã_bán', 'Sao_đánh_giá', 'Giảm_giá_(%)', 'Link_sản_phẩm']
        self.productTree = ttk.Treeview(
            self.table, columns=columns, show='headings', cursor="hand2 orange")

        def columnConstructor(cl, text, w):
            self.productTree.heading(cl, text=text)
            self.productTree.column(cl, width=w, anchor=tk.CENTER)
        columnConstructor('S_T_T', 'STT', 50)
        columnConstructor('Tên_sản_phẩm', 'Tên sản phẩm', 210)
        columnConstructor('Giá_nhỏ_nhất', 'Giá nhỏ nhất', 100)
        columnConstructor('Giá_lớn_nhất', 'Giá lớn nhất', 100)
        columnConstructor('Đã_bán', 'Đã bán', 80)
        columnConstructor('Sao_đánh_giá', 'Sao đánh giá', 100)
        columnConstructor('Giảm_giá_(%)', 'Giảm giá (%)', 80)
        columnConstructor('Link_sản_phẩm', 'Link sản phẩm', 200)
        contacts = []
        for i in range(0, len(self.productList)):
            contacts.append((i+1, self.productList[i].name, self.productList[i].minPrice, self.productList[i].maxPrice,
                            self.productList[i].sales, '%.1f' % self.productList[i].rating if self.productList[i].rating is not None else None, self.productList[i].discount, self.productList[i].link))
        self.productTree.tag_configure('oddrow', background="#7DE5ED")
        self.productTree.tag_configure('evenrow', background="white")
        count = 0
        for contact in contacts:
            if (count % 2 == 0):
                self.productTree.insert('', tk.END, values=contact, tags="oddrow")
            else:
                self.productTree.insert('', tk.END, values=contact, tags="evenrow")
            count += 1
        s2 = ttk.Style()
        s2.theme_use("default")
        s2.configure('Treeview.Heading', background="orange", bd=1)
        s2.configure('Treeview', rowheight=40, border=1)
        s2.map('Treeview', background=[('selected', 'orange')],)
        # Access to link of selected product

        def goLink(event):
            input_id = self.productTree.selection()
            input_item = self.productTree.set(input_id, column="Link_sản_phẩm")
            webbrowser.open('{}'.format(input_item))
        self.productTree.bind("<Double-1>", goLink)
        self.productTree.grid(row=0, column=0, sticky='nsew')
        # Scrollbar
        self.scrollbar = ttk.Scrollbar(
            self.table, orient=tk.VERTICAL, command=self.productTree.yview)
        self.productTree.configure(yscroll=self.scrollbar.set)
        self.scrollbar.grid(row=0, column=1, sticky='ns')

        def sortByPrice():
            self.clearTreeView()
            self.productList.sort(key=lambda x: (x.minPrice, x.maxPrice, -x.rating, -int(x.sales)))
            self.fillTreeView()

        def sortByRating():
            self.clearTreeView()
            self.productList.sort(key=lambda x: (-x.rating, -int(x.sales), x.minPrice ,x.maxPrice))
            self.fillTreeView()

        def sortBySales():
            self.clearTreeView()
            self.productList.sort(key=lambda x: (-int(x.sales), -x.rating, x.minPrice, x.maxPrice))
            self.fillTreeView()


        # Set Selections
        self.selections = tk.Frame(self.table, relief="solid")
        self.selections.place(x=980, y=60, height=350, width=200)
        self.btn_sortPrice = tk.Button(self.selections, text="Sắp xếp theo giá tăng dần",
                                pady=10, fg="white", bg="black", cursor="hand2", command=sortByPrice)
        self.btn_sortSales = tk.Button(self.selections, text="Sắp xếp theo doanh số giảm dần",
                                        pady=10, fg="white", bg="black", cursor="hand2", command=sortBySales)
        self.btn_sortRate = tk.Button(self.selections, text="Sắp xếp theo đánh giá giảm dần",
                                pady=10, fg="white", bg="black", cursor="hand2", command=sortByRating)
        self.lb_exportToFile = tk.Label(self.selections, text='Nhập tên file: ')
        self.e_exportToFile = tk.Entry(self.selections, width=40)
        self.btn_exportToFile = tk.Button(self.selections, text='Lưu vào file csv!', pady=10,
                                    fg='white', bg='green', command=lambda: writeToFile(self.e_exportToFile.get(),self))
        self.btn_sortPrice.pack(pady=10)
        self.btn_sortSales.pack(pady=10)
        self.btn_sortRate.pack(pady=10)
        self.lb_exportToFile.pack(pady=10)
        self.e_exportToFile.pack(pady=5)
        self.btn_exportToFile.pack(pady=10)

    def run(self):
        self.mainloop()