import tkinter as tk
from tkinter import messagebox
import requests
from PIL import Image, ImageTk
from io import BytesIO

root = tk.Tk()
root.title("Book Search")
root.configure(bg="#d1aee6")
root.geometry("600x700")  

cover_dic = {}

def get_cover(cover_id, size='M'):
    if cover_id in cover_dic:
        return cover_dic[cover_id]
    url = f"https://covers.openlibrary.org/b/id/{cover_id}-{size}.jpg"
    try:
        r = requests.get(url)
        imgdata = r.content
        img = Image.open(BytesIO(imgdata))
        img = img.resize((180, 260))
        tkimg = ImageTk.PhotoImage(img)
        cover_dic[cover_id] = tkimg
        return tkimg
    except Exception as e:
        print("Couldn't find book cover:", e)
        return None

def search_book():
    query = entry.get().strip()
    if not query:
        messagebox.showwarning("Input Error", "Please enter a book name")
        return

    try:
        r = requests.get(f"https://openlibrary.org/search.json?title={query}", timeout=8)
        data = r.json()
        docs = data.get("docs", [])

        if not docs:
            messagebox.showinfo("No Results", "No books found with that title.")
            return

        book = docs[0]
        title = book.get("title", "Unknown title")
        author = ", ".join(book.get("author_name", ["Unknown author"]))
        year = book.get("first_publish_year", "N/A")
        cover_id = book.get("cover_i")

        text = f"\nTitle: {title}\n\nAuthor: {author}\n\nYear: {year}\n"

        detailstext.configure(state="normal")
        detailstext.delete("1.0", "end")
        detailstext.insert("end", text)

        if cover_id:
            tkimg = get_cover(cover_id, size='L')
            if tkimg:
                lbl = tk.Label(detailstext, image=tkimg, bg="#f0e6f6")
                lbl.image = tkimg
                detailstext.window_create("end", window=lbl)

        detailstext.configure(state="disabled")

    except Exception as e:
        print("Book search error:", e)
        messagebox.showerror("Error", str(e))


frame = tk.Frame(root, bg="#f0e6f6")
frame.pack(expand=True)

header = tk.Label(frame, text=" Book Finder", font=( 28, ), bg="#d5a7f0")
header.pack(pady=20)

entry_label = tk.Label(frame, text="Enter Book Title:", font=( 16), bg="#f0e6f6")
entry_label.pack(pady=5)

entry = tk.Entry(frame, width=30, font=( 16), justify="center")
entry.pack(pady=10, ipady=5)

search_button = tk.Button(frame, text="Search", font=( 16), command=search_book)
search_button.pack(pady=15)

result_label = tk.Label(frame, text="Book Details:", font=( 18, ), bg="#c99fe1")
result_label.pack(pady=10)

detailstext = tk.Text(frame, height=18, width=55, wrap="word", font=( 14), bg="#c997e1")
detailstext.pack(pady=10)


root.mainloop()
