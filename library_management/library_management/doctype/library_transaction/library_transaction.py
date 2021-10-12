# Copyright (c) 2021, Yanky and contributors
# For license information, please see license.txt

from __future__ import unicode_literals

import frappe
from frappe.model.document import Document
from datetime import date

class LibraryTransaction(Document):
    def before_submit(self):
        if self.type == "Issue":
            self.validate_issue()
            self.validate_maximum_limit()
            self.count += 1
            loan_period = frappe.db.get_single_value("Library Setting", "loan_period")
            self.to_date = frappe.utils.add_days(self.from_date, loan_period or 50)
            self.return_date = frappe.utils.add_days(self.from_date, loan_period or 50)
            # set the article status to be Issued
            article = frappe.get_doc("Article", self.title)
            article.stock -= 1
            if article.stock != 0:
                article.status = 'Available'
                article.save()
            elif article.stock == 0:
                article.status = 'Issued'
                article.save()

        elif self.type == "Return":
            self.validate_return()
            loan_period = frappe.db.get_single_value("Library Setting", "loan_period")
            # set the article status to be Available
            article = frappe.get_doc("Article", self.title)
            article.status = "Available"
            article.stock += 1
            article.save()
            self.to_date = frappe.utils.add_days(self.from_date, loan_period or 50)
            if date.fromisoformat(self.return_date) > date.fromisoformat(self.to_date):
                self.debt += 500
                self.amount += 500
                frappe.msgprint(("Oustanding Debt including late fee of Rs 500 = Rs ") + str(self.amount))
            else:
                frappe.msgprint(("Outstanding Debt = Rs ") + str(self.amount))
            member = frappe.get_doc("Library Member", self.library_member)
            member.total_spending = member.total_spending + self.amount - 250
            member.save()
    

    def on_update_after_submit(self):
        if self.type == "Return":
            self.validate_return()
            self.paid = 1
            loan_period = frappe.db.get_single_value("Library Setting", "loan_period")
            # set the article status to be Available
            article = frappe.get_doc("Article", self.title)
            article.status = "Available"
            article.stock += 0.5
            article.save()
            self.to_date = frappe.utils.add_days(self.from_date, loan_period or 50)
            if date.fromisoformat(self.return_date) > date.fromisoformat(self.to_date):
                self.debt += 500
                self.amount += 500
                frappe.msgprint(("Oustanding Debt including late fee of Rs 500 = Rs ") + str(self.amount))
            else:
                frappe.msgprint(("Outstanding Debt = Rs ") + str(self.amount))
            member = frappe.get_doc("Library Member", self.library_member)
            member.total_spending = member.total_spending + self.amount - 250
            member.save()



    def validate_issue(self):
        article = frappe.get_doc("Article", self.title)
        # article cannot be issued if it is already issued
        if article.status == "Issued":
            frappe.throw("Article is already issued to other members")

    def validate_return(self):
        article = frappe.get_doc("Article", self.title)
        # article cannot be returned if it is not issued first
        if article.total_quantity == article.stock:
        	frappe.throw("Article cannot be returned without being issued first")

    def validate_maximum_limit(self):
        max_articles = frappe.db.get_single_value("Library Setting", "max_articles")
        count = frappe.db.count(
            "Library Transaction",
            {"library_member": self.library_member, "type": "Issue", "docstatus": 1},
        )
        if count >= max_articles:
            frappe.throw("Maximum limit reached for issuing articles")