// Copyright (c) 2016, Yanky and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Books Stock Report"] = {
	"filters": [
		{
			"label": ("Title"),
			"fieldname": "title_filter",
			"fieldtype": "Link",
			"options": "Article"
		}
	]
};