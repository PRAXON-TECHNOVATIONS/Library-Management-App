import frappe
import json


@frappe.whitelist()
def createArticles():
    data = json.loads(frappe.request.data)
    frappe.msgprint(data)
    if data.get("books"):
        books = data.get("books")
        for book in books:
            if not frappe.db.exists('Article', {'isbn': book.get('isbn')}):
                article = frappe.new_doc('Article')
                article.isbn = book.get('isbn')
            else:
                article = frappe.get_doc('Article', {'isbn': book.get('isbn')})
            if book.get('title'):
                article.title = book.get('title')
            if book.get('author'):
                article.author = book.get('author')
            if book.get('isbn'):
                article.isbn = book.get('isbn')
            if book.get('publisher'):
                article.publisher = book.get('publisher')
            if book.get('page'):
                article.page = book.get('page')
            if book.get('total_quantity'):
                article.total_quantity = book.get('total_quantity')
            if book.get('language'):
                article.language = book.get('language')
            article.stock = book.get('total_quantity')
            article.save(ignore_permissions=True)
            frappe.db.commit()