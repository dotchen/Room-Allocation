from __future__ import unicode_literals

import datetime
from django.db import models
from django.conf import settings


class Case(models.Model):
	name = models.CharField(max_length=200, primary_key=True)
	created_date = models.DateTimeField(default=datetime.datetime.now, blank=True)
	img = models.ImageField(default=None)
	rent = models.IntegerField(default=0)

	def __unicode__(self):
		return "{}, {}".format(self.name, self.created_date)

class Room(models.Model):
	case = models.ForeignKey(Case, on_delete=models.CASCADE)
	name = models.CharField(max_length=200)

	def __unicode__(self):
		return self.name

		
class Group(models.Model):
	case = models.ForeignKey(Case, on_delete=models.CASCADE)
	name = models.CharField(max_length=200)
	num_of_renters = models.IntegerField(default=1)

	def __unicode__(self):
		return self.name

   
class Scheme(models.Model):
	room = models.ForeignKey(Room, on_delete=models.CASCADE)
	rent = models.IntegerField(default=0)

class Choice(models.Model):
	group = models.ForeignKey(Group, on_delete=models.CASCADE)
	scheme = models.ForeignKey(Scheme, on_delete=models.CASCADE) 


class Allocation(models.Model):
	case = models.OneToOneField(Case, on_delete=models.CASCADE, primary_key=True)
	prev_choices = models.ManyToManyField(Choice, related_name="prev_allocation")
	curr_choices = models.ManyToManyField(Choice, related_name="curr_allocation")

	def is_turn_finished(self):
		num_of_groups = Group.objects.filter(case=self.case).count()
		num_of_votes = self.curr_choices.count()
		return num_of_votes == num_of_groups

	def vote(self, group, scheme):
		# Make each group is only allowed to vote once during each turn
		assert len(Choice.objects.filter(curr_allocation=self, group=group)) == 0
		choice = Choice.objects.create(group=group, scheme=scheme)
		self.curr_choices.add(choice)

	def next_turn(self):
		



	def __init__(self, case_name, *args, **kwargs):
		super(Allocation, self).__init__(*args, **kwargs)
		self.case = Case.objects.get(pk=case_name)

	def __unicode__(self):
		return "Allocation for {}".format(self.case)