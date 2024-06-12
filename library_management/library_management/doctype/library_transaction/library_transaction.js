// Copyright (c) 2021, Yanky and contributors
// For license information, please see license.txt

// frappe.ui.form.on('Library Transaction', {
// 	// refresh: function(frm) {

// 	// }
// });

frappe.ui.form.on('Library Transaction','refresh',
	function(frm) {
		if(frm.doc.return_date)
			{
				var duration = frappe.datetime.get_day_diff(frm.doc.return_date, frm.doc.from_date)
			}
		else
			{
				var duration = frappe.datetime.get_day_diff(frm.doc.to_date, frm.doc.from_date)
			}
		var cost = frm.doc.rate * duration;
        cur_frm.set_value("amount", cost);
		if(frm.doc.paid == 1)
		{
			cur_frm.set_value("debt", 0);
		}
		else
		{
			cur_frm.set_value("debt", cost);
		}
	}
);
