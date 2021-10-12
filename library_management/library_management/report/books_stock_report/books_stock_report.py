# Copyright (c) 2013, Yanky and contributors
# For license information, please see license.txt

import frappe

def execute(filters=None):
	columns, data = [], []
	columns = get_columns()
	article_data = get_article_data(filters)
	for article in article_data:
		temp_dict = {
		"title":article.get("title"),
		"isbn":article.get("isbn"),
		"stock":article.get("stock"),
		"total_quantity":article.get("total_quantity"),
		"issued_count":article.get("total_quantity") - article.get("stock")
		}
		data.append(temp_dict)
	return columns, data

def get_columns():
	columns = ["" for column in range(5)]
	columns[0] = {
		"label": ("Title"),
		"fieldname": "title",
		"fieldtype": "Link",
		"options": "Article",
		"width": 200
	}
	columns[1] = {
		"label": ("Isbn"),
		"fieldname": "isbn",
		"width": 200
	}
	columns[2] = {
		"label": ("Stock"),
		"fieldname": "stock",
		"width": 150
	}
	columns[3] = {
		"label": ("Total Quantity"),
		"fieldname": "total_quantity",
		"width": 150
	}
	columns[4] = {
		"label": ("Issued Count"),
		"fieldname": "issued_count",
		"width": 150
	}
	return columns

def get_article_data(filters) :
	if filters:
		query = "select title, isbn, stock, total_quantity from tabArticle where title = '" + str(filters.get("title_filter")) + "'"
		article_data  = frappe.db.sql(query, as_dict=1) 
	else:
		article_data  = frappe.db.sql("""select title, isbn, stock, total_quantity from tabArticle """, as_dict=1) 
	
	return article_data