import customtkinter as ctk # لتصميم الواجهة الرئيسية
from tkinter import ttk, messagebox, filedialog # لإنشاء الواجهة وعرض الرسائل وإختيار الملفات
import datetime # لتنسيق التاريخ والوقت
from PIL import Image, ImageTk # لعرض الصور
import os # للعمل مع الملفات والمجلدات
import screeninfo # للحصول على أبعاد الشاشة
import shutil # للتعامل مع نسخ الملفات
import json # للتعامل مع ملفات JSON
import cv2 # للتعامل مع الكاميرا
import threading # لتشغيل الكاميرا في خيط منفصل
import qrcode # لإنشاء QR Code
import mediapipe as mp

class SmartAccountingApp:
    def __init__(self):
        self.root = ctk.CTk() # لإنشاء النافذة الرئيسية
        self.show_splash_screen() # لعرض الشاشة البداية
        self.root.after(2000, self.start_main_app)  # بعد 2 ثانية يتم تشغيل البرنامج الرئيسي
        self.root.mainloop() # لتشغيل البرنامج

#==================================================[شاشة التحميل يبداء من هنا]==================================================#
    def show_splash_screen(self):    # الحصول على أبعاد الشاشة

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

    # ضبط حجم نافذة الـ splash بحيث تكون في وسط الشاشة
        self.root.geometry(f"600x400+{int((screen_width - 600) / 2)}+{int((screen_height - 400) / 2)}") # لضبط حجم الشاشة
        self.root.title("مرحباً بك ✨") # لإعطاء النافذة العنوان
        self.root.iconbitmap("image/titel_name_2.ico") # لإضافة الصورة الى النافذة


        splash_frame = ctk.CTkFrame(self.root, corner_radius=20) # لإنشاء قسم للصورة والنص
        splash_frame.pack(expand=True, fill="both", padx=40, pady=40) # لتغطية الشاشة بالقسم

    # إطار فرعي لتجميع الصورة والنص
        top_frame = ctk.CTkFrame(splash_frame, corner_radius=10) # لإنشاء قسم للصورة والنص
        top_frame.pack(expand=True, fill="x", pady=20) # لتغطية الشاشة بالقسم

        try:
        # ضبط حجم الصورة بشكل مناسب للنافذة
            splash_img = ctk.CTkImage(light_image=Image.open("image/titel_name_2.png"),dark_image=Image.open("image/titel_name_2.png"),size=(100, 100))  # تحديد حجم الصورة
        # إضافة الصورة في اليسار
            ctk.CTkLabel(top_frame, image=splash_img, text="").pack(side="left", padx=20)
        except Exception as e:
            print("فشل تحميل الصورة:", e)

    # إضافة النص بجانب الصورة
        ctk.CTkLabel(top_frame, text="💼 برنامج المحاسبة الذكية", font=("Tajawal", 30, "bold")).pack(side="left", padx=10)

        # إضافة النص السفلي
        ctk.CTkLabel(splash_frame, text="جارٍ التحميل...", font=("Tajawal", 18)).pack(pady=10)

#==================================================[شاشة التحميل ينتهي هنا]==================================================#

#==================================================[البرنامج الرئيسي يبداء من هنا]==================================================#

    def start_main_app(self):
        for widget in self.root.winfo_children():# لإزالة الواجهات القديمة
            widget.destroy()
        self.setup_ui() # لإعداد الواجهة الرئيسية

    def setup_ui(self):
        ctk.set_appearance_mode("system")    
        ctk.set_default_color_theme("blue")

        # الحصول على أبعاد الشاشة
        screen = screeninfo.get_monitors()[0]
        window_width = int(screen.width * 0.9)  # 90% من عرض الشاشة
        window_height = int(screen.height * 0.9)  # 90% من ارتفاع الشاشة
        
        # حساب موقع النافذة ليكون في المنتصف
        x = int((screen.width - window_width) / 2)
        y = int((screen.height - window_height) / 2)
        
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.root.minsize(1024, 768)  # الحد الأدنى لحجم النافذة
        self.root.title('💼 برنامج المحاسبة الذكية')
        self.root.state('zoomed')

        # تكوين الشبكة الرئيسية
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)  # للسجلات
        self.root.grid_columnconfigure(1, weight=2)  # للمنتجات

        # إنشاء الإطار الرئيسي
        self.main_frame = ctk.CTkFrame(self.root, corner_radius=15)
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

        # إنشاء إطار السجلات في اليسار
        self.records_frame = ctk.CTkFrame(self.root, corner_radius=15)
        self.records_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.setup_records_section()

        # إنشاء إطار التبويبات في الإطار الرئيسي
        self.tabview = ctk.CTkTabview(self.main_frame)
        self.tabview.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        # إضافة التبويبات
        self.products_tab = self.tabview.add("المنتجات")
        self.qr_tab = self.tabview.add("QR Code")

        # تكوين الشبكة في كل تبويب
        self.products_tab.grid_rowconfigure(0, weight=1)
        self.products_tab.grid_columnconfigure(0, weight=1)

        self.qr_tab.grid_rowconfigure(0, weight=1)
        self.qr_tab.grid_columnconfigure(0, weight=1)

        # إعداد محتوى التبويبات
        self.setup_products_content()
        self.setup_qr_content()

    def setup_products_content(self):
        # إطار المنتجات
        self.menu_frame = ctk.CTkFrame(self.products_tab, corner_radius=10)
        self.menu_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.setup_menu()
        self.setup_bill_section()

    def setup_qr_content(self):
        # إطار QR Code
        qr_frame = ctk.CTkFrame(self.qr_tab)
        qr_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        # عنوان الصفحة
        title_label = ctk.CTkLabel(qr_frame, text="QR Code صفحة", font=("Tajawal", 24, "bold"))
        title_label.pack(pady=20)

        # إطار لعرض الكاميرا
        self.camera_frame = ctk.CTkFrame(qr_frame)
        self.camera_frame.pack(pady=10)
        
        # تسمية لعرض الكاميرا
        self.camera_label = ctk.CTkLabel(self.camera_frame, text="")
        self.camera_label.pack(padx=10, pady=10)

        # إطار للأزرار
        buttons_frame = ctk.CTkFrame(qr_frame)
        buttons_frame.pack(pady=10)

        # زر تشغيل الكاميرا
        self.start_camera_btn = ctk.CTkButton(buttons_frame, text="تشغيل الكاميرا", 
                                            command=self.start_camera,
                                            font=("Tajawal", 14))
        self.start_camera_btn.pack(side="left", padx=10)

        # زر إيقاف الكاميرا
        self.stop_camera_btn = ctk.CTkButton(buttons_frame, text="إيقاف الكاميرا", 
                                           command=self.stop_camera,
                                           font=("Tajawal", 14))
        self.stop_camera_btn.pack(side="left", padx=10)

        # إطار لعرض المنتج الممسوح
        self.scanned_product_frame = ctk.CTkFrame(qr_frame)
        self.scanned_product_frame.pack(pady=10, fill="x", padx=10)

        # متغيرات للكاميرا
        self.camera = None
        self.is_camera_running = False
        self.scanned_products = []

    def start_camera(self):
        if not self.is_camera_running:
            self.camera = cv2.VideoCapture(0)
            self.is_camera_running = True
            self.start_camera_btn.configure(state="disabled")
            self.stop_camera_btn.configure(state="normal")
            threading.Thread(target=self.update_camera, daemon=True).start()

    def stop_camera(self):
        if self.is_camera_running:
            self.is_camera_running = False
            if self.camera is not None:
                self.camera.release()
            self.camera_label.configure(text="")
            self.start_camera_btn.configure(state="normal")
            self.stop_camera_btn.configure(state="disabled")

    def update_camera(self):
        qr_detector = cv2.QRCodeDetector()
        while self.is_camera_running:
            ret, frame = self.camera.read()
            if ret:
                # تحويل الإطار إلى RGB
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                
                # قراءة QR Code
                data, bbox, _ = qr_detector.detectAndDecode(frame)
                if data and data.isdigit() and int(data) in self.products:
                    product_info = self.products[int(data)]
                    self.add_scanned_product(product_info)
                
                # تحويل الإطار إلى صورة يمكن عرضها في Tkinter
                image = Image.fromarray(frame_rgb)
                image = image.resize((640, 480))
                photo = ImageTk.PhotoImage(image=image)
                
                self.camera_label.configure(image=photo)
                self.camera_label.image = photo

    def add_scanned_product(self, product_info):
        if product_info not in self.scanned_products:
            self.scanned_products.append(product_info)
            self.update_scanned_products_display()

    def update_scanned_products_display(self):
        # مسح المحتوى السابق
        for widget in self.scanned_product_frame.winfo_children():
            widget.destroy()

        # عرض المنتجات الممسوحة
        for product_info in self.scanned_products:
            product_frame = ctk.CTkFrame(self.scanned_product_frame)
            product_frame.pack(fill="x", padx=5, pady=5)

            try:
                img = ctk.CTkImage(light_image=Image.open(product_info[2]),
                                 dark_image=Image.open(product_info[2]),
                                 size=(50, 50))
                ctk.CTkLabel(product_frame, image=img, text="").pack(side="left", padx=5)
            except:
                pass

            ctk.CTkLabel(product_frame, 
                        text=f"{product_info[0]}\n{product_info[1]} IQ",
                        font=("Tajawal", 14)).pack(side="left", padx=5)

            # إطار للأزرار
            buttons_frame = ctk.CTkFrame(product_frame, fg_color="transparent")
            buttons_frame.pack(side="right", padx=5)

            # زر إضافة المنتج إلى الفاتورة
            add_to_bill_btn = ctk.CTkButton(buttons_frame, 
                                          text="إضافة إلى الفاتورة",
                                          command=lambda p=product_info: self.add_to_bill(p),
                                          font=("Tajawal", 12))
            add_to_bill_btn.pack(side="left", padx=2)

            # زر حذف المنتج
            delete_btn = ctk.CTkButton(buttons_frame, 
                                     text="حذف المنتج",
                                     command=lambda p=product_info: self.delete_scanned_product(p),
                                     font=("Tajawal", 12),
                                     fg_color="red",
                                     hover_color="darkred")
            delete_btn.pack(side="left", padx=2)

    def delete_scanned_product(self, product_info):
        """حذف المنتج من قائمة المنتجات الممسوحة"""
        if messagebox.askyesno("تأكيد الحذف", f"هل أنت متأكد من حذف المنتج {product_info[0]}؟"):
            self.scanned_products.remove(product_info)
            self.update_scanned_products_display()
            messagebox.showinfo("نجاح", "تم حذف المنتج بنجاح")

    def add_to_bill(self, product_info):
        # البحث عن المنتج في القائمة وإضافة كمية
        for i, (product_id, info) in enumerate(self.products.items()):
            if info == product_info:
                self.counters[i].set(self.counters[i].get() + 1)
                break
        self.generate_bill()

    def setup_records_section(self):
        """إعداد قسم السجلات"""
        # إطار البحث
        search_frame = ctk.CTkFrame(self.records_frame)
        search_frame.pack(fill="x", padx=5, pady=5)

        self.search_var = ctk.StringVar()
        self.search_var.trace('w', self.filter_records)
        
        search_entry = ctk.CTkEntry(search_frame, placeholder_text="🔍 بحث...", textvariable=self.search_var, font=('Tajawal', 14))
        search_entry.pack(side="left", fill="x", expand=True, padx=5)

        # إضافة زر مسح جميع السجلات
        clear_all_btn = ctk.CTkButton(search_frame, text="🗑️ مسح الكل", width=80,
                                    command=self.clear_all_records,
                                    fg_color="red", hover_color="darkred")
        clear_all_btn.pack(side="right", padx=5)

        refresh_btn = ctk.CTkButton(search_frame, text="🔄", width=40,command=self.refresh_records)
        refresh_btn.pack(side="right", padx=5)

        # إطار جدول السجلات
        tree_frame = ctk.CTkFrame(self.records_frame)
        tree_frame.pack(fill="both", expand=True, padx=5, pady=5)
        # إنشاء جدول السجلات
        self.records_tree = ttk.Treeview(tree_frame,columns=('name', 'date', 'phone', 'total'),show='headings',selectmode='browse')
        # تعريف الأعمدة
        self.records_tree.heading('name', text='الاسم')
        self.records_tree.heading('date', text='التاريخ')
        self.records_tree.heading('phone', text='الهاتف')
        self.records_tree.heading('total', text='المجموع')
        # ضبط عرض الأعمدة
        self.records_tree.column('name', width=150)
        self.records_tree.column('date', width=100)
        self.records_tree.column('phone', width=120)
        self.records_tree.column('total', width=100)
        # إضافة شريط التمرير
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.records_tree.yview)
        self.records_tree.configure(yscrollcommand=scrollbar.set)

        # تعبئة الإطار
        self.records_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # إطار الأزرار
        buttons_frame = ctk.CTkFrame(self.records_frame)
        buttons_frame.pack(fill="x", padx=5, pady=5)

        # زر الحذف
        delete_btn = ctk.CTkButton(buttons_frame, text="🗑️ حذف السجل المحدد",command=self.delete_record,fg_color="red",hover_color="darkred")
        delete_btn.pack(fill="x", expand=True, padx=2)
        self.load_records() # تحميل السجلات

    def load_records(self):
        """تحميل السجلات من الملف"""
        try:
            # إنشاء ملف جديد إذا لم يكن موجوداً
            if not os.path.exists('records.json'):
                with open('records.json', 'w', encoding='utf-8') as f:
                    json.dump([], f, ensure_ascii=False, indent=2)
            
            # قراءة السجلات من الملف
            with open('records.json', 'r', encoding='utf-8') as f:
                self.records = json.load(f)
        except Exception as e:
            print(f"خطأ في تحميل السجلات: {str(e)}")
            self.records = []
        self.refresh_records()

    def save_records(self):
        """حفظ السجلات إلى الملف"""
        with open('records.json', 'w', encoding='utf-8') as f:
            json.dump(self.records, f, ensure_ascii=False, indent=2)

    def refresh_records(self):
        """تحديث عرض السجلات"""
        # مسح جميع العناصر من شجرة العرض
        for item in self.records_tree.get_children():
            self.records_tree.delete(item)
            
        # إذا لم تكن هناك سجلات، نعرض رسالة
        if not self.records:
            self.records_tree.insert('', 'end', values=('لا توجد سجلات', '', '', ''))
            return
            
        # إعادة عرض السجلات المتوفرة
        for record in self.records:
            self.records_tree.insert('', 'end', values=(
                record['name'],
                record['date'],
                record['phone'],
                record['total']
            ))

    def filter_records(self, *args):
        """تصفية السجلات حسب البحث"""
        search_term = self.search_var.get().lower()
        for item in self.records_tree.get_children():
            self.records_tree.delete(item)
        for record in self.records:
            if (search_term in record['name'].lower() or
                search_term in record['phone'].lower() or
                search_term in record['total'].lower()):
                self.records_tree.insert('', 'end', values=(
                    record['name'],
                    record['date'],
                    record['phone'],
                    record['total']
                ))

    def delete_record(self):
        """حذف السجل المحدد"""
        selected_item = self.records_tree.selection()
        if not selected_item:
            messagebox.showwarning("تنبيه", "⚠️ الرجاء اختيار سجل للحذف")
            return

        values = self.records_tree.item(selected_item)['values']
        confirmation_message = f"هل أنت متأكد من حذف هذا السجل؟\n\n"
        confirmation_message += f"👤 اسم العميل: {values[0]}\n"
        confirmation_message += f"📅 التاريخ: {values[1]}\n"
        confirmation_message += f"📞 رقم الهاتف: {values[2]}\n"
        confirmation_message += f"💰 المجموع: {values[3]}"

        if messagebox.askyesno("تأكيد الحذف", confirmation_message):
            # حذف السجل من القائمة
            self.records = [record for record in self.records 
                          if not (record['name'] == values[0] and
                                record['date'] == values[1] and
                                record['phone'] == values[2] and
                                record['total'] == values[3])]
            
            # حذف السجل من العرض
            self.records_tree.delete(selected_item)
            
            # حفظ التغييرات في الملف مع معالجة الأخطاء
            try:
                with open('records.json', 'w', encoding='utf-8') as f:
                    json.dump(self.records, f, ensure_ascii=False, indent=2)
                messagebox.showinfo("نجاح", "✅ تم حذف السجل بنجاح")
            except Exception as e:
                messagebox.showerror("خطأ", f"❌ حدث خطأ أثناء حفظ التغييرات في الملف: {str(e)}")
                # في حالة حدوث خطأ، قد ترغب في إعادة تحميل السجلات من الملف
                # لضمان اتساق البيانات بين الذاكرة والملف
                self.load_records()

    def setup_menu(self):
        self.menu_frame = ctk.CTkFrame(self.main_frame, corner_radius=10)
        self.menu_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.menu_frame.grid_columnconfigure((0, 1, 2), weight=1)
        self.menu_frame.grid_rowconfigure(0, weight=0)  # للعنوان
        self.menu_frame.grid_rowconfigure(1, weight=0)  # للتبويبات
        self.menu_frame.grid_rowconfigure(2, weight=1)  # للمنتجات
        self.menu_frame.grid_rowconfigure(3, weight=0)  # للأزرار

        # إطار العنوان
        self.title_frame = ctk.CTkFrame(self.menu_frame, corner_radius=10)
        self.title_frame.grid(row=0, column=0, columnspan=3, sticky="ew", padx=10, pady=(10, 5))
        
        # عنوان البرنامج
        self.title_label = ctk.CTkLabel(self.title_frame, text='💼 برنامج المحاسبة الذكية',font=('Tajawal', 32, 'bold'))
        self.title_label.pack(side="left", padx=20)
        
        # إطار الأزرار في العنوان
        buttons_frame = ctk.CTkFrame(self.title_frame, fg_color="transparent")
        buttons_frame.pack(side="right", padx=20)
        
        # زر تبديل المظهر
        self.switch_var = ctk.BooleanVar(value=False)
        self.switch = ctk.CTkSwitch(buttons_frame, text="☀️ / 🌙",variable=self.switch_var,command=self.switch_event)
        self.switch.pack(side="left", padx=5)

        # إضافة التبويبات
        self.tabview = ctk.CTkTabview(self.menu_frame, height=40)  # تقليل ارتفاع التبويبات
        self.tabview.grid(row=1, column=0, columnspan=3, sticky="ew", padx=10, pady=(0, 5))
        
        # إضافة التبويبات
        self.products_tab = self.tabview.add("المنتجات")
        self.qr_tab = self.tabview.add("QR Code")

        # تكوين الشبكة في كل تبويب
        self.products_tab.grid_rowconfigure(0, weight=1)
        self.products_tab.grid_columnconfigure(0, weight=1)
        self.qr_tab.grid_rowconfigure(0, weight=1)
        self.qr_tab.grid_columnconfigure(0, weight=1)

        # إطار المنتجات القابل للتمرير (في تبويب المنتجات)
        self.products_content_frame = ctk.CTkFrame(self.products_tab)
        self.products_content_frame.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
        
        self.products_scrollable = ctk.CTkScrollableFrame(self.products_content_frame,height=750)
        self.products_scrollable.pack(expand=True, fill="both", padx=5, pady=5)
        self.products_scrollable.grid_columnconfigure((0, 1, 2), weight=1)
        # إعداد محتوى QR Code
        self.setup_qr_content()
        # إطار الأزرار السفلية
        self.buttons_frame = ctk.CTkFrame(self.main_frame, corner_radius=10)
        self.buttons_frame.grid(row=1, column=0, columnspan=2, sticky="ew", padx=10, pady=(5, 10))
        self.buttons_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

        # الأزرار السفلية
        ctk.CTkButton(self.buttons_frame, text='🛒 شراء المواد',command=self.generate_bill,font=('Tajawal', 14)).grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        ctk.CTkButton(self.buttons_frame, text='🧾 فاتورة جديدة',command=self.clear_all,font=('Tajawal', 14)).grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        ctk.CTkButton(self.buttons_frame, text='➕ إضافة منتج',command=self.show_add_product_dialog,font=('Tajawal', 14)).grid(row=0, column=2, padx=5, pady=5, sticky="ew")
        ctk.CTkButton(self.buttons_frame, text='❌ إغلاق البرنامج',command=self.root.quit,font=('Tajawal', 14)).grid(row=0, column=3, padx=5, pady=5, sticky="ew")

        if not hasattr(self, 'products'):
            self.products = {}
        if not os.path.exists('products'):
            os.makedirs('products')
        self.load_products()
        self.counters = [ctk.IntVar(value=0) for _ in range(len(self.products))]
        # إنشاء بطاقات المنتجات
        self.create_product_cards()

    def create_product_cards(self):
        """إنشاء بطاقات المنتجات"""
        for i, (product_id, product_info) in enumerate(self.products.items()):
            row = i // 3
            col = i % 3

            # إنشاء إطار للمنتج
            card = ctk.CTkFrame(self.products_scrollable)
            card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
            
            try:
                # تحميل وعرض صورة المنتج
                img = ctk.CTkImage(light_image=Image.open(f"{product_info[2]}"),dark_image=Image.open(f"{product_info[2]}"),size=(150, 150))  # زيادة حجم الصورة
                ctk.CTkLabel(card, image=img, text="").pack(pady=10)
            except:
                pass
            
            # معلومات المنتج
            ctk.CTkLabel(card, text=f"{product_info[0]}\n{product_info[1]} IQ", 
                        font=('Tajawal', 16, 'bold')).pack(pady=5)  # زيادة حجم الخط
            
            # إطار للعداد
            counter_frame = ctk.CTkFrame(card)
            counter_frame.pack(pady=10)
            
            # أزرار التحكم بالكمية
            minus_button = ctk.CTkButton(counter_frame, text="-", width=40, height=40,  # زيادة حجم الأزرار
                                       command=lambda idx=i: self.counters[idx].set(max(0, self.counters[idx].get() - 1)))
            minus_button.pack(side="left", padx=5)
            
            counter_label = ctk.CTkEntry(counter_frame, textvariable=self.counters[i],
                                       width=60, height=40,  # زيادة حجم مربع الإدخال
                                       justify="center", font=('Tajawal', 16))
            counter_label.pack(side="left", padx=5)
            
            plus_button = ctk.CTkButton(counter_frame, text="+", width=40, height=40,
                                      command=lambda idx=i: self.counters[idx].set(self.counters[idx].get() + 1))
            plus_button.pack(side="left", padx=5)
            
            # زر الحذف
            delete_button = ctk.CTkButton(card, text="🗑️ حذف المنتج",
                                        width=120, height=35,  # زيادة حجم زر الحذف
                                        fg_color="red", hover_color="darkred",
                                        command=lambda pid=product_id: self.delete_product(pid))
            delete_button.pack(pady=10)

    def delete_product(self, product_id): # هذا الدالة الخاصة بحذف المنتج
        """حذف منتج معين"""
        if messagebox.askyesno("تأكيد الحذف", "هل أنت متأكد من حذف هذا المنتج؟"):
            # حذف الصورة إذا كانت موجودة في مجلد products
            image_path = self.products[product_id][2]
            if os.path.exists(image_path) and 'products/' in image_path:
                try:
                    os.remove(image_path)
                except:
                    pass
            # حذف المنتج من القاموس
            del self.products[product_id]
            # إعادة ترقيم المنتجات
            self.products = {i: product for i, product in enumerate(self.products.values())}
            # تحديث المتغيرات
            self.counters = [ctk.IntVar(value=0) for _ in range(len(self.products))]
            # حفظ التغييرات
            self.save_products()
            # تحديث العرض
            self.refresh_products()
            messagebox.showinfo("نجاح", "تم حذف المنتج بنجاح")

    def setup_bill_section(self): # 
        self.bill_frame = ctk.CTkFrame(self.main_frame,width=400, corner_radius=12)
        self.bill_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

        self.bill_tree = ttk.Treeview(self.bill_frame, columns=('price', 'quantity', 'total'), show='headings', height=15)
        self.bill_tree.pack(fill="both", expand=True, padx=5, pady=5)

        self.bill_tree.column('price', width=80, anchor='center')
        self.bill_tree.column('quantity', width=80, anchor='center')
        self.bill_tree.column('total', width=100, anchor='center')

        self.bill_tree.heading('#0', text='المنتج')
        self.bill_tree.heading('price', text='السعر')
        self.bill_tree.heading('quantity', text='الكمية')
        self.bill_tree.heading('total', text='الإجمالي')

#==================================================[الاعداد ينتهي هنا]==================================================#

#==================================================[قائمة الادخال يبداء من هنا]==================================================#
        self.customer_frame = ctk.CTkFrame(self.bill_frame,corner_radius=10)
        self.customer_frame.pack(fill="x", padx=5, pady=5)

        font = ("Tajawal", 15,"bold")
        # تعديل حقول الإدخال لتكون من اليمين إلى اليسار
        self.name_entry = ctk.CTkEntry(self.customer_frame, placeholder_text="👤 اسم العميل", justify="right",font=font)
        self.name_entry.pack(fill="x", padx=5, pady=2)

        self.phone_entry = ctk.CTkEntry(self.customer_frame, placeholder_text="📞 رقم الهاتف", justify="right",font=font)
        self.phone_entry.pack(fill="x", padx=5, pady=2)

        self.address_entry = ctk.CTkEntry(self.customer_frame, placeholder_text="📍 العنوان", justify="right",font=font)
        self.address_entry.pack(fill="x", padx=5, pady=2)

        self.total_entry = ctk.CTkEntry(self.customer_frame, placeholder_text="💰 المجموع الكلي", justify="right",font=font)
        self.total_entry.pack(fill="x", padx=5, pady=2)

        # إضافة إطار لكود الخصم
        discount_frame = ctk.CTkFrame(self.customer_frame)
        discount_frame.pack(fill="x", padx=5, pady=2)

        # إضافة حقل إدخال نسبة الخصم
        self.discount_entry = ctk.CTkEntry(discount_frame, placeholder_text="نسبة الخصم %", justify="right", font=font, width=200)
        self.discount_entry.pack(side="left", fill="x", expand=True, padx=(0, 5))

        # إضافة زر تطبيق الخصم
        self.apply_discount_btn = ctk.CTkButton(discount_frame, text="تطبيق الخصم", font=font, width=100, command=self.apply_discount)
        self.apply_discount_btn.pack(side="right")

        self.date_entry = ctk.CTkEntry(self.customer_frame, placeholder_text="📅 التاريخ", justify="right",font=font)
        self.date_entry.pack(fill="x", padx=5, pady=2)
        self.date_entry.insert(0, datetime.datetime.now().strftime("%Y-%m-%d"))

        self.gender_combo = ctk.CTkComboBox(self.customer_frame, values=['ذكر', 'أنثى'], state="readonly", justify="right",font=font)
        self.gender_combo.pack(fill="x", padx=5, pady=2)
        self.gender_combo.set('ذكر')

        self.bill_buttons = ctk.CTkFrame(self.bill_frame, corner_radius=10)
        self.bill_buttons.pack(fill="x", padx=5, pady=5)

        ctk.CTkButton(self.bill_buttons, text='💾 حفظ الفاتورة', command=self.save_bill).pack(side="left", padx=5, expand=True)
        ctk.CTkButton(self.bill_buttons, text='🧹 مسح الحقول', command=self.clear_fields).pack(side="left", padx=5, expand=True)
#==================================================[قائمة الادخال ينتهي هنا]==================================================#
    def generate_bill(self):
        for item in self.bill_tree.get_children():
            self.bill_tree.delete(item)
        total = 0
        items_added = False
        for i, (product_id, product_info) in enumerate(self.products.items()):
            quantity = self.counters[i].get()
            if quantity > 0:
                price = product_info[1]
                item_total = quantity * price
                total += item_total
                self.bill_tree.insert("", 'end', text=product_info[0], values=(f"{price} IQ", quantity, f"{item_total} IQ"))
                items_added = True
        if not items_added:
            messagebox.showwarning("تحذير", "⚠️ لم يتم اختيار أي منتجات")
            return
        self.total_entry.delete(0, 'end')
        self.total_entry.insert(0, f"{total} IQ")
    def save_bill(self):
        """حفظ الفاتورة"""
        if not self.bill_tree.get_children():
            messagebox.showerror("خطأ", "❌ لا توجد فاتورة لحفظها")
            return

        customer_name = self.name_entry.get()
        phone = self.phone_entry.get()
        total = self.total_entry.get()

        if not all([customer_name, phone, total]):
            messagebox.showerror("خطأ", "❗ الرجاء إدخال جميع البيانات المطلوبة")
            return

        # إنشاء سجل جديد
        new_record = {
            'date': self.date_entry.get(),
            'name': customer_name,
            'phone': phone,
            'address': self.address_entry.get(),
            'total': total,
            'gender': self.gender_combo.get(),
            'items': []
        }

        # إضافة المنتجات المشتراة
        for item in self.bill_tree.get_children():
            values = self.bill_tree.item(item)['values']
            new_record['items'].append({
                'name': self.bill_tree.item(item)['text'],
                'price': values[0],
                'quantity': values[1],
                'total': values[2]
            })

        # إضافة السجل الجديد في بداية القائمة
        self.records.insert(0, new_record)

        # حفظ السجلات في الملف مباشرة
        try:
            with open('records.json', 'w', encoding='utf-8') as f:
                json.dump(self.records, f, ensure_ascii=False, indent=2)
            
            # تحديث العرض
            self.records_tree.delete(*self.records_tree.get_children())
            for record in self.records:
                self.records_tree.insert('', 'end', values=(
                    record['name'],
                    record['date'],
                    record['phone'],
                    record['total']
                ))
            
            messagebox.showinfo("نجاح", "✅ تم حفظ الفاتورة بنجاح")
            self.clear_all()
        except Exception as e:
            messagebox.showerror("خطأ", f"❌ حدث خطأ أثناء حفظ الفاتورة: {str(e)}")

    def clear_fields(self):
        self.name_entry.delete(0, 'end')
        self.phone_entry.delete(0, 'end')
        self.address_entry.delete(0, 'end')
        self.total_entry.delete(0, 'end')
        self.discount_entry.delete(0, 'end')  # تحديث اسم حقل الخصم
        self.date_entry.delete(0, 'end')
        self.date_entry.insert(0, datetime.datetime.now().strftime("%Y-%m-%d"))
        self.gender_combo.set('ذكر')

    def apply_discount(self):
        """تطبيق نسبة الخصم على المجموع الكلي"""
        discount_str = self.discount_entry.get().strip().replace('%', '')  # إزالة علامة % إذا وجدت
        
        if not discount_str:
            messagebox.showwarning("تنبيه", "الرجاء إدخال نسبة الخصم")
            return

        # التحقق من المجموع الكلي
        try:
            current_total = float(self.total_entry.get().replace(" IQ", ""))
        except ValueError:
            messagebox.showerror("خطأ", "الرجاء إنشاء الفاتورة أولاً")
            return

        # التحقق من صحة نسبة الخصم
        try:
            discount_percentage = float(discount_str)
            if discount_percentage <= 0 or discount_percentage > 100:
                messagebox.showerror("خطأ", "نسبة الخصم يجب أن تكون بين 1 و 100")
                return
        except ValueError:
            messagebox.showerror("خطأ", "الرجاء إدخال رقم صحيح لنسبة الخصم")
            return

        # حساب الخصم وتحديث المجموع
        discount_amount = current_total * (discount_percentage / 100)
        new_total = current_total - discount_amount
        
        # تحديث حقل المجموع الكلي
        self.total_entry.delete(0, 'end')
        self.total_entry.insert(0, f"{new_total:.0f} IQ")
        
        # عرض رسالة نجاح
        messagebox.showinfo("نجاح", f"تم تطبيق خصم {discount_percentage}% بنجاح\nمقدار الخصم: {discount_amount:.0f} IQ")

    def clear_all(self):
        self.clear_fields()
        for item in self.bill_tree.get_children():
            self.bill_tree.delete(item)
        for counter in self.counters:
            counter.set(0)
            
    def switch_event(self):
        ctk.set_appearance_mode("light" if self.switch_var.get() else "dark")

    def load_products(self):
        """تحميل المنتجات من الملف"""
        products_file = "products/products.txt"
        if os.path.exists(products_file):
            with open(products_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                self.products = {}
                for i, line in enumerate(lines):
                    if line.strip():
                        name, price, image_path = line.strip().split('|')
                        self.products[i] = [name, int(price), image_path]
        else:
            # المنتجات الافتراضية
            self.products = {
                0: ["Arduino", 12000, "image/arduino_1.png"],
                1: ["Arduino Mini Micro", 10000, "image/Arduino_Mini_Micro.png"],
                2: ["Batter Limet", 3000, "image/Batter_Limet.png"],
                3: ["IR Sensor", 1250, "image/IR_Sensor.png"],
                4: ["motor Device", 3500, "image/motor_Device.png"],
                5: ["motor drive shield", 6000, "image/Servo-Motor-3.png"],
                6: ["Servo Motor", 2500, "image/Arduino_Mini_Micro.png"],
                7: ["Touch switch button", 750, "image/Touch_switch_button.png"],
                8: ["Ultrasonic", 2500, "image/Ultrasonic_1.png"],
            }
            self.save_products()
    def save_products(self):
        #حفظ المنتجات إلى الملف وإنشاء QR Codes
        # إنشاء المجلدات المطلوبة
        if not os.path.exists('products'):
            os.makedirs('products')
        if not os.path.exists('products/qr_codes'):
            os.makedirs('products/qr_codes')
            
        products_file = "products/products.txt"
        try:
            with open(products_file, 'w', encoding='utf-8') as f:
                for product_id, product_info in self.products.items():
                    # التحقق من وجود الصورة
                    if not os.path.exists(product_info[2]):
                        messagebox.showwarning("تحذير", f"لم يتم العثور على صورة المنتج: {product_info[0]}")
                        continue
                        
                    f.write(f"{product_info[0]}|{product_info[1]}|{product_info[2]}\n")
                    
                    # إنشاء QR Code
                    qr = qrcode.QRCode(
                        version=1,
                        error_correction=qrcode.constants.ERROR_CORRECT_L,
                        box_size=10,
                        border=4,
                    )
                    qr.add_data(str(product_id))
                    qr.make(fit=True)
                    
                    # حفظ QR Code كصورة
                    qr_img = qr.make_image(fill_color="black", back_color="white")
                    qr_path = f"products/qr_codes/product_{product_id}.png"
                    qr_img.save(qr_path)
                    
            messagebox.showinfo("نجاح", "تم حفظ المنتجات وإنشاء QR Codes بنجاح")
        except Exception as e:
            messagebox.showerror("خطأ", f"حدث خطأ أثناء حفظ المنتجات: {str(e)}")

    def show_add_product_dialog(self):
        """عرض نافذة إضافة منتج جديد"""
        dialog = ctk.CTkToplevel(self.root)
        dialog.title("إضافة منتج جديد")
        dialog.geometry("400x300")
        dialog.transient(self.root)
        dialog.grab_set()
        # المتغيرات
        product_name_var = ctk.StringVar()
        product_price_var = ctk.StringVar()
        image_path_var = ctk.StringVar()
        # الحقول
        ctk.CTkLabel(dialog, text="اسم المنتج:", font=('Tajawal', 14)).pack(pady=5)
        name_entry = ctk.CTkEntry(dialog, textvariable=product_name_var, font=('Tajawal', 14))
        name_entry.pack(pady=5)
        ctk.CTkLabel(dialog, text="السعر:", font=('Tajawal', 14)).pack(pady=5)
        price_entry = ctk.CTkEntry(dialog, textvariable=product_price_var, font=('Tajawal', 14))
        price_entry.pack(pady=5)
        def select_image(): # هذا الدالة خاصة باختيار الصورة من قائمة اضافة المنتجات
            file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif *.bmp")])
            if file_path:
                # إنشاء مجلد products إذا لم يكن موجوداً
                if not os.path.exists('products'):
                    os.makedirs('products')
                # نسخ الصورة إلى مجلد products
                filename = os.path.basename(file_path)
                new_path = os.path.join('products', filename)
                try:
                    shutil.copy2(file_path, new_path)
                    image_path_var.set(new_path)
                    messagebox.showinfo("نجاح", f"تم حفظ الصورة في: {new_path}")
                except Exception as e:
                    messagebox.showerror("خطأ", f"فشل في حفظ الصورة: {str(e)}")
        ctk.CTkButton(dialog, text="اختيار صورة", command=select_image, font=('Tajawal', 14)).pack(pady=10)
        def save_product(): # هذا الدالة خاصة بحفظ المنتج
            name = product_name_var.get().strip()
            price = product_price_var.get().strip()
            image_path = image_path_var.get().strip()

            if not all([name, price, image_path]):
                messagebox.showerror("خطأ", "الرجاء ملء جميع الحقول")
                return
            try:
                price = int(price)
            except ValueError:
                messagebox.showerror("خطأ", "الرجاء إدخال سعر صحيح")
                return

            # التحقق من وجود الصورة
            if not os.path.exists(image_path):
                messagebox.showerror("خطأ", "لم يتم العثور على الصورة المحددة")
                return

            # إضافة المنتج الجديد
            new_id = len(self.products)
            self.products[new_id] = [name, price, image_path]
            self.save_products()
            
            # تحديث الواجهة
            self.counters.append(ctk.IntVar(value=0))
            self.refresh_products()
            
            dialog.destroy()
            messagebox.showinfo("نجاح", "تم إضافة المنتج بنجاح")
        ctk.CTkButton(dialog, text="حفظ", command=save_product, font=('Tajawal', 14)).pack(pady=10)
    def refresh_products(self): # هذا الدالة خاصة بتحديث عرض المنتجات
        """تحديث عرض المنتجات"""
        # إزالة المنتجات الحالية من الإطار
        for widget in self.products_scrollable.winfo_children():
            widget.destroy()
        
        # إعادة إنشاء بطاقات المنتجات في نفس الإطار
        self.create_product_cards()

    def clear_all_records(self):
        """مسح جميع السجلات"""
        if messagebox.askyesno("تأكيد المسح", "هل أنت متأكد من مسح جميع السجلات؟\nلا يمكن التراجع عن هذه العملية!"):
            try:
                # مسح جميع السجلات من الذاكرة
                self.records = []
                
                # حفظ القائمة الفارغة في الملف
                with open('records.json', 'w', encoding='utf-8') as f:
                    json.dump([], f, ensure_ascii=False, indent=2)
                
                # تحديث العرض
                self.records_tree.delete(*self.records_tree.get_children())
                self.records_tree.insert('', 'end', values=('لا توجد سجلات', '', '', ''))
                
                messagebox.showinfo("نجاح", "✅ تم مسح جميع السجلات بنجاح")
            except Exception as e:
                messagebox.showerror("خطأ", f"❌ حدث خطأ أثناء مسح السجلات: {str(e)}")

app = SmartAccountingApp()
    