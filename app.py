"""ระบบยืม-คืนหนังสือห้องสมุด (Flask) - Mini-Project DevOps

รัน: python app.py แล้วเปิด http://localhost:5000
"""
import os

from flask import Flask, flash, redirect, render_template, request, url_for

from library import Library, LibraryError

SAMPLE_BOOKS = [
    ("ปัญญาประดิษฐ์เบื้องต้น", "สมชาย ใจดี"),
    ("DevOps Handbook", "Gene Kim"),
    ("Clean Code", "Robert C. Martin"),
]


def create_app(data_path=None):
    app = Flask(__name__)
    app.secret_key = "library-cicd-demo"
    library = Library(data_path)
    if not library.books:
        for title, author in SAMPLE_BOOKS:
            library.add_book(title, author)
    app.config["LIBRARY"] = library

    @app.route("/")
    def index():
        keyword = request.args.get("q", "")
        return render_template("index.html", books=library.search(keyword),
                               keyword=keyword, stats=library.stats(),
                               overdue=library.overdue())

    @app.post("/books")
    def add_book():
        return run(lambda: library.add_book(request.form.get("title", ""),
                                            request.form.get("author", "")),
                   "เพิ่มหนังสือเรียบร้อย")

    @app.post("/books/<int:book_id>/borrow")
    def borrow(book_id):
        return run(lambda: library.borrow(book_id, request.form.get("borrower", "")),
                   "ยืมหนังสือเรียบร้อย (กำหนดคืน 7 วัน)")

    @app.post("/books/<int:book_id>/return")
    def return_book(book_id):
        return run(lambda: library.return_book(book_id), "คืนหนังสือเรียบร้อย")

    @app.get("/health")
    def health():
        return {"status": "ok", **library.stats()}

    def run(action, message):
        try:
            action()
            flash(message, "ok")
        except LibraryError as error:
            flash(str(error), "error")
        return redirect(url_for("index"))

    return app


if __name__ == "__main__":
    data_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "books.json")
    create_app(data_file).run(host="0.0.0.0", port=5000)
