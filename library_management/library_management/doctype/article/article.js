// Copyright (c) 2021, Yanky and contributors
// For license information, please see license.txt

frappe.ui.form.on('Article', {
	total_quantity(frm) {
		cur_frm.set_value('stock', frm.doc.total_quantity);
	}
});
