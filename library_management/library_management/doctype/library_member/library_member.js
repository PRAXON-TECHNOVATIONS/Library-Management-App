// Copyright (c) 2021, Yanky and contributors
// For license information, please see license.txt

// frappe.ui.form.on('Library Member', {
// 	// refresh: function(frm) {

// 	// }
// });

frappe.ui.form.on('Library Member', {
    refresh: function(frm) {
        frm.add_custom_button('Create Transaction', () => {
            frappe.new_doc('Library Transaction', {
                library_member: frm.doc.name
            })
        })
    }
});