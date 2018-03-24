from __future__ import unicode_literals
from django.db import models
import re
from datetime import datetime
import bcrypt

class UserManager(models.Manager):
	def register(self, name, username, password, confirm):
		response = {
			"valid": True,
			"errors": [],
			"user": None
		}

		if len(name) < 1:
			response["errors"].append("Name is required")
		elif len(name) < 3:
			response["errors"].append("Name must be 3 characters or longer")

		if len(username) < 1:
			response["errors"].append("Username is required")
		elif len(username) < 3:
			response["errors"].append("Username must be 3 characters or longer")
		else:
			username_list = User.objects.filter(username = username.lower())
			if(len(username_list) > 0):
				response["errors"].append("Username is already in use")

		if len(password) < 1:
			response["errors"].append("Password is required")
		elif len(password) < 8:
			response["errors"].append("Password must be 8 characters or longer")

		if len(confirm) < 1:
			response["errors"].append("Confirm Password is required")
		elif confirm != password:
			response["errors"].append("Confirm Password must match Password")

		if len(response["errors"]) > 0:
			response["valid"] = False
		else:
			response["user"] = User.objects.create(
				name=name,
				username=username.lower(),
				password=bcrypt.hashpw(password.encode(), bcrypt.gensalt())
			)

		return response

	def login(self, username, password):
		response = {
			"valid": True,
			"errors": [],
			"user": None
		}

		if len(username) < 1:
			response["errors"].append("Username is required")
		else:
			username_list = User.objects.filter(username=username.lower())
			if len(username_list) == 0:
				response["errors"].append("Username not found")

		if len(password) < 1:
			response["errors"].append("Password is required")
		elif len(password) < 8:
			response["errors"].append("Password must be 8 characters or longer")

		if len(response["errors"]) == 0:
			hashed_pw = username_list[0].password
			if bcrypt.checkpw(password.encode(), hashed_pw.encode()):
				response["user"] = username_list[0]
			else:
				response["errors"].append("Incorrect Password")

		if len(response["errors"]) > 0:
			response["valid"] = False

		return response

class TravelManager(models.Manager):
	def addTravel(self, destination, description, from_date, to_date, planned_by):
		response = {
			"valid": True,
			"errors": [],
			"travel": None
		}

		if len(destination) < 1:
			response["errors"].append("Destination is required")
		if len(description) < 1:
			response["errors"].append("Description is required")
		if len(from_date) < 1:
			response["errors"].append("Travel Date From is required")
		if len(to_date) < 1:
			response["errors"].append("Travel Date To is required")

		if(len(response["errors"]) == 0):
			today = datetime.now()
			if(today > datetime.strptime(from_date, "%Y-%m-%d")):
				response["errors"].append("Travel Date From must be in the future")
			if(today > datetime.strptime(to_date, "%Y-%m-%d")):
				response["errors"].append("Travel Date To must be in the future")
			if(datetime.strptime(from_date, "%Y-%m-%d") > datetime.strptime(to_date, "%Y-%m-%d")):
				response["errors"].append("Travel Date To must be after Travel Date From")

		if len(response["errors"]) > 0:
			response["valid"] = False
		else:
			response["travel"] = Travel.objects.create(
				destination=destination,
				description=description,
				travel_date_from = from_date,
				travel_date_to = to_date,
				planned_by_id = planned_by
				#joined_users_id = planned_by
			)
			#response["travel"].planned_by = User.objects.get(id = planned_by)
			response["travel"].joined_users.add(User.objects.get(id = planned_by))
		return response

	def joinTravel(self, travel_id, joiner_id):
		response = {
			"valid": True,
			"errors": [],
		}

		travel = Travel.objects.get(id = travel_id)
		if len(travel.joined_users.all().filter(id = joiner_id)) > 0:
			response["errors"].append("You have already joined this trip!")

		if len(response["errors"]) > 0:
			response["valid"] = False
		else:
			travel.joined_users.add(User.objects.get(id = joiner_id))
		return response

class User(models.Model):
	name = models.CharField(max_length=255)
	username = models.CharField(max_length=255)
	password = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = UserManager()
	def __repr__(self):
		return "<User object: {}>".format(self.username)

class Travel(models.Model):
	destination = models.CharField(max_length = 255)
	description = models.TextField(max_length = 1000)
	travel_date_from = models.DateField()
	travel_date_to = models.DateField()
	planned_by = models.ForeignKey(User, related_name = "planned_travels")
	joined_users = models.ManyToManyField(User, related_name = "joined_travels")
	created_at = models.DateTimeField(auto_now = True)
	updated_at = models.DateTimeField(auto_now_add = True)
	objects = TravelManager()
	def __repr__(self):
		return "<Travel object: {}>".format(self.destination)