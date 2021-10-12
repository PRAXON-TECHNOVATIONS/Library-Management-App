# Copyright (c) 2013, Yanky and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import flt, cint

def execute(filters=None):
	columns, data = [], []
	columns = get_columns()
	member_data = get_member_data(filters)
	for member in member_data:
		temp_dict = {
		"library_member":member.get("name"),
		"full_name":member.get("full_name"),
		"email":member.get("email"),
		"phone":member.get("phone"),
		"total_spending":member.get("total_spending")
		}
		data.append(temp_dict)
	chart = get_chart()	
	return columns, data, None, chart

def get_columns():
	columns = ["" for column in range(5)]
	columns[0] = {
		"label": ("Library Member"),
		"fieldname": "library_member",
		"fieldtype": "Link",
		"options": "Library Member",
		"width": 150
	}
	columns[1] = {
		"label": ("Full Name"),
		"fieldname": "full_name",
		"width": 200
	}
	columns[2] = {
		"label": ("E-mail"),
		"fieldname": "email",
		"width": 250
	}
	columns[3] = {
		"label": ("Contact Number"),
		"fieldname": "phone",
		"width": 150
	}
	columns[4] = {
		"label": ("Total Spending"),
		"fieldname": "total_spending",
		"fieldtype": "currency",
		"width": 150
	}
	return columns

def get_member_data(filters) :
	if filters:
		query = "select name, full_name, email, phone, total_spending from `tabLibrary Member` where name = '" + str(filters.get("member_filter")) + "'"
		member_data  = frappe.db.sql(query, as_dict=1) 
	else:
		member_data  = frappe.db.sql("""select name, full_name, email, phone, total_spending from `tabLibrary Member` """, as_dict=1) 
	
	return member_data

def get_chart():
	chart_data = {
		"labels": [frappe.db.get_values('Library Member', 'name')],
   		"datasets": [
        {
            'name': "Total Spending",
            'values': [frappe.db.get_values('Library Member','total_spending')]
        }
    ]
}

	# attributes = [d.get("fieldname") for d in columns]

	# dimensions = [
	# 	[
	# 	value.get(attr) for value in data if value["xAxisField"] > int(fltr.xAxisField)
	# 	] for attr in attributes
	# ]
	# chart_data = {
	# 	'labels': [{
	# 		'name': ('Library Member'), 'values': [frappe.db.get_value('Library Member', 'name')]
	# 	}],
	# 	'datasets': [{
	# 		'name': ('Total Spending'), 'values': [frappe.db.get_value('Library Member', 'total_spending')]
	# 		}
	# 	]
	# }
		
	chart = {
		"title": "Total Spending",
		"data": chart_data,
		"type": 'bar',
		"height": 250,
		"color": '#7cd6fd'
	}
	return chart