from tkinter import *
from flask import *
import requests

ENDP = "carsite.shop:8080"
API_ENDPOINT = f"http://{ENDP}"


# Basic tkinter configuration
root = Tk()
root.title("Edit car AD")
root.geometry("600x450")

# Input boxes & label
bhp = Entry(root, width=50)
bhp.place(x=160, y=50)
bhp_label = Label(root, text="Brake HorsePower (BHP):")
bhp_label.place(x=20, y=50)

cardescr = Entry(root, width=50)
cardescr.place(x=160, y=75)
cardescr_label = Label(root, text="Description:")
cardescr_label.place(x=20, y=75)

emaill = Entry(root, width=50)
emaill.place(x=160, y=100)
emaill_label = Label(root, text="Email:")
emaill_label.place(x=20, y=100)

km = Entry(root, width=50)
km.place(x=160, y=125)
km_label = Label(root, text="Km:")
km_label.place(x=20, y=125)

modell = Entry(root, width=50)
modell.place(x=160, y=150)
modell_label = Label(root, text="Model(<1-24>):")
modell_label.place(x=20, y=150)

price = Entry(root, width=50)
price.place(x=160, y=175)
price_label = Label(root, text="price:")
price_label.place(x=20, y=175)

year = Entry(root, width=50)
year.place(x=160, y=200)
year_label = Label(root, text="year:")
year_label.place(x=20, y=200)

# What to do when btn is clicked
img_list = []
def btn_clicked():
    bh = bhp.get()
    ca = cardescr.get()
    em = emaill.get()
    k_m = km.get()
    mo = modell.get()
    pr = price.get()
    ye = year.get()
    # im = img.get()

    items = {
            "bhp":bh,
            "cardescr":ca,
            "email":em,
            "km":k_m,
            "model":mo,
            "price":pr,
            "year":ye
            }
            
    header = {'Content-type': 'application/json'}
    print(items)
    # get /models/<brand_id> for all available models
    resp = requests.post(f"{API_ENDPOINT}/edit/{mo}",data=json.dumps(items), headers=header)
    print(resp)

# BTN
btn = Button(root, text="Upload to the website!", command=btn_clicked)
btn.place(x=225, y=350)

root.mainloop()