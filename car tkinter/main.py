from tkinter import *
from flask import *
import requests

ENDP = "192.168.1.114:8080"
API_ENDPOINT = f"http://{ENDP}"


# Basic tkinter configuration
root = Tk()
root.title("Add car AD")
root.geometry("600x450")

# Input boxes & label
brand = Entry(root, width=50)
brand.place(x=95, y=50)
brand_label = Label(root, text="Brand:")
brand_label.place(x=20, y=50)

model = Entry(root, width=50)
model.place(x=95, y=75)
model_label = Label(root, text="Model:")
model_label.place(x=20, y=75)

year = Entry(root, width=50)
year.place(x=95, y=100)
year_label = Label(root, text="Year:")
year_label.place(x=20, y=100)

km = Entry(root, width=50)
km.place(x=95, y=125)
km_label = Label(root, text="KM:")
km_label.place(x=20, y=125)

descr = Entry(root, width=50)
descr.place(x=95, y=150)
descr_label = Label(root, text="Description:")
descr_label.place(x=20, y=150)

id = Entry(root, width=50)
id.place(x=95, y=175)
id_label = Label(root, text="id:")
id_label.place(x=20, y=175)

img = Entry(root, width=50)
img.place(x=95, y=200)
img_label = Label(root, text="img(<link>):")
img_label.place(x=20, y=200)
img_label2 = Label(root, text="Please seperate the links using <,> if you have multiple pics", fg="red")
img_label2.place(x=20, y=220)


# What to do when btn is clicked
img_list = []
def btn_clicked():
    bt = brand.get()
    mo = model.get()
    ye = year.get()
    k_m = km.get()
    de = descr.get()
    im = img.get()
    i_d=id.get()

    items = {"brand":bt,
            "cardescr":de,
            "imgs":im,
            "km":k_m,
            "model":mo,
            "year":ye}
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    resp = requests.post(f"{API_ENDPOINT}/edit/1",data=json.dumps(items), headers=headers)
    print(resp.content)

# BTN
btn = Button(root, text="Upload to the website!", command=btn_clicked)
btn.place(x=225, y=350)

root.mainloop()