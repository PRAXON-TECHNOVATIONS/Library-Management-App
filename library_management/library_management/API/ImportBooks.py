import frappe
import json


@frappe.whitelist()
def createArticles():
    data = json.loads(frappe.request.data) 
    frappe.msgprint(data)
    if not frappe.db.exists('Article', {'isbn': data.get('isbn')}):
        article = frappe.new_doc('Article')
        article.isbn = data.get('isbn')
    else:
        article = frappe.get_doc('Article', {'isbn': data.get('isbn')})
    if data.get('title'):
        article.title = data.get('title')
    if data.get('author'):
        article.author = data.get('author')
    if data.get('isbn'):
        article.isbn = data.get('isbn')
    if data.get('publisher'):
        article.publisher = data.get('publisher')
    if data.get('page'):
        article.page = data.get('page')
    if data.get('total_quantity'):
        article.total_quantity = data.get('total_quantity')
    if data.get('language'):
        article.language = data.get('language')
    article.stock = data.get('total_quantity')
    article.save(ignore_permissions=True)
    frappe.db.commit()