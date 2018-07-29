from __future__ import unicode_literals
import frappe
from frappe.utils import cint, get_gravatar, format_datetime, now_datetime,add_days,today,formatdate,date_diff,getdate,get_last_day
from frappe import throw, msgprint, _
from frappe.utils.password import update_password as _update_password
from frappe.desk.notifications import clear_notifications
from frappe.utils.user import get_system_managers
import frappe.permissions
import frappe.share
import re
import string
import random
import json
import time
from datetime import datetime
from datetime import date
from datetime import timedelta
import collections
import math
import logging


@frappe.whitelist()
def customerPermission(doc,method):
	if doc.sales_person:
		addUserPermission(doc.name,doc.sales_person)
	else:
		removeUserPermission(doc.name)
	




@frappe.whitelist()
def addUserPermission(allow_val,employee):
	d=frappe.get_doc({
				 	"docstatus": 0,
				 	"doctype": "User Permission",
				 	"name": "New User Permission 1",
				 	"__islocal": 1,
				 	"__unsaved": 1,
				 	"owner": "Administrator",
				 	"apply_for_all_roles": 0,
				 	"user": getUserIdFromEmployeeId(employee),
				 	"allow":"Customer",
				 	"for_value": str(allow_val)
				 })
	d.insert(ignore_permissions=True)

@frappe.whitelist()
def removeUserPermission(customer):
	frappe.db.sql("""delete from `tabUser Permission` where allow='Customer' and for_value=%s""",customer)
	
	


@frappe.whitelist()
def getUserIdFromEmployeeId(emp_code):
	userid=frappe.db.sql("""select user_id from `tabEmployee` where name=%s""",emp_code)
	if userid:
		return userid[0][0]


@frappe.whitelist()
def addCustomerInGL(doc,method):
	glentries=frappe.db.sql("""select name,party from `tabGL Entry` where voucher_no='"""+doc.name+"""'""")
	if glentries:
		for gl in glentries:
			frappe.msgprint(str(gl[0]))
			if doc.doctype=="Sales Invoice":
				updateGL(gl[0],doc.customer)
			if doc.doctype=="Payment Entry":
				updateGL(gl[0],doc.party)
			if doc.doctype=="Journal Entry":
				updateGL(gl[0],gl[1])





@frappe.whitelist()
def updateGL(name,party):
	frappe.db.commit()
	#frappe.client.set_value("GL Entry",name,"customer",str(party))
	if not party==None:
		frappe.msgprint(str(party))
		frappe.db.sql("""update `tabGL Entry` set customer='"""+str(party)+"""' where name='"""+str(name)+"""'""")
		frappe.db.commit()



	

	
	
