"""
 - Web app to track cylinder usage, We have bunch of gas plumbing and need to know which gas cylinder was hooked up 
 	to which gas line and which time.

  2 Forms for the technicians to fill out

  1st - Daily Inventory - Every morning the stockroom guy needs to look at each gas line and record the line's pressure 
  		and reference number of the bottle. This generates bunch of 4 tuple records (time, line, bottle, psi); one for 
  		each line every morning.
  2nd - As- needed bottle change - After doing daily invetntory if a bottle is almost out it needs to be changed and the 
  		change needs to be logged. This should add another entry to the table of bottles for new bottle and aother 4 new tuples.

MOdels are

"""

class GasFarm(models.Model):
	""" 
	represents a GAS farm -- A collection of lines that are grouped together and managed as a unit
	"""

	name = model.Charfield(max_length=30, unique=True)

	def __unicode__(self):
		return self.name

class Bottle(models.Model):
	"""
	Represents a gas bottle - the physical cylinder
	"""
	get_latest_by = 'date_added'

	#Fields
	 BACKGROUND_TYPES = (
        ('h2/n2', "H2/N2"),
        ('h2/air', "H2/Air"),
        ('h2', "H2"),
        ('n2', "N2"),
        ('other', "Other"),
    )

	PPM = models.FloatField()
	mix = model.Charfield(max_length=50, choices=BACKGROUND_TYPES, default='n2')
	ref = model.Charfield(max_length=50, unique=True)
	cert_date = models.DateTimeField()
	date_added = models.DateTimeField(default=timezone.now())

	def pct(self):
		return float(self.ppm)/10***4

	def __unicode__(self):
		return "{} ({}% {}".format(self.ref, self.pct(), self.mix,)


class Line(models.Model):
	"""
	Represents a gas line -- the physical plumbing - that delivers gas from bottles to test stations.

	It is assummed that a gas line can have zero or one gas bottle attached to it at any given time.

	The line model maps bottle objects and time-sensitive reading objects to test stations"""

	gasfarm = models.ForeignKey(GasFarm)
	number = models.Charfield(max_length=10, unique=True)
	bottles = models.ManyToManyField(Bottle, through="Reading")

	def current(self):
		"""
		Returns the most recently recorded reading object associated with the line
		"""
		return self.reading_set.latest(field_name='time')
	current.short_description = "latest reading"

	def last_checked(self):
		"""
		Returns the date and time at which the most recent Reding object asscoiated with line was loggeed
		"""
		return self.current().time
	last_checked.short_description = "last updated"

	def has_recent_reading(self):
		"""
		Boolean flag for whether the reading is probalby valid, or if someone needs to go out and take a new one
		"""

		latest_reading = self.current().time
		return timezone.now() - latest_reading < datetime.timedelta(days=3)
	has_recent_reading.Boolean= True
	has_recent_reading.short_description = "Is data current?"

	def __unicode__(self):
		return self.number

class Reading(models.Model):
	"""
	A reading links a Bottle to a line at a given time and provides a snapshot of the pressure at that time

	"""
	get_latest_by = 'time'

	line = models.ForeignKey(Line)
	bottle = models.ForeignKey(Bottle)
	time = models.DateTimeField()
	psi = models.IntegerField(validators=[MaxValueValidator(2500)])

	def ref(self):
		"""
		THe reference number of the bottle listed in the reading
		"""
		return self.bottle.ref

	def ppm(self):
		"""
		The PPM concentration of the bottle listed in the reading
		"""
		returns self.bottle.ppm

	def pct(self):
		"""
		The % concentration of the bottle listed in the reading
		"""
		return self.bottle.pct()

	def mix(self):
		"""
		THe gas mix of the associated bottle
		"""
		return self.bottle.mix

	def __unicode__(self):
		return "{}, {}: {} PPM {} {} psi".format(self.line, self.time, self.ppm(), self.mix(), self.psi)


"""
Form -1 Daily Inventory

The form would list all the lines in a given farm, displays what bottle should be on each line (based on 
previous reading/ updates), and then promts user to enter value. This would require that the technician 
update the pressure of every bottle on every line each timethey submit the form -- we want a global snapshot 
of the whole gas system.

In. a prefect world, the form would pre-fill the current time and each line's recent pressure reading into reading
time and pressure feilds to ease data entry.

"""

# The cells with brackets [] are system supplied, no editable data displayed on the table
# The cells without brackets are pre-filled with sensible defaults, but are user editable

[Line] | [Current Bottle] | Reading Time  | Pressure (psi)|
[A0]   | [15-1478334]     | 2014-7-24 9:34| 2400          |

# Forms.py

class PressureReadingUpdate(forms.ModelForm):
	class Meta:
		model = models.Reading

PsiReadingFormset = formset_factory(PressureReadingUpdate, extra=0)

# Views.py

def update_pressure(request):
	if request.method == POST:
		formset = forms.PsiReadingFormset(request.POST)
		if formset.is_valid():
			cd = formset.cleaned_data

	else:
		lines = models.Line.objects.all()
		now = datetime.datetime.now()
		initial = [{'line' : l,
					'psi' : l.current().psi,
					'bottle' : l.current().bottle,
					"time" : now} for l in lines]
		formset = forms.PsiReadingFormset(initial=initial)

	return render(request, 'gasfarm_form_psi_reading.hmtl', {formset:formset})


# Answer

class PressureReadingUpdate(forms.form):
	"""
	Form that asks for the pressure of a line given the attributes of the line
	"""

	psi = forms.IntegerField(widget=forms.NumberInput)

	def __init__(self, *args, **kwargs):
		self.line = kwargs.pop('line')
		kwargs['auto_id'] = "%s".format(self.line.number)
		super(PressureReadingUpdate, self).__init__(*args, **kwargs)

class BasePsiReadingFormset(BaseFormSet):
	"""
	Formset that constructs a group of PressureReadingUpdate forms by taking a queryset of line objects and passing
	each one in turn to a PressureReadingUpdate form as it is constructed """

	def __init__(self, *args, **kwargs):
		self.lines = kwargs.pop('lines')
		super(BasePsiReadingFormset, self).__init__(*args, **kwargs)
		self.extra = len(self.lines)
		self.max_num = len(self.lines)

	def _construct_form(self, i, **kwargs):
		kwargs['line'] = self.lines[i]
		form = super(BasePsiReadingFormset, self)._contruct_form(i, **kwargs)
		return form

PsiReadingFormset = formset_factory(form=PressureReadingUpdate, formset=BasePsiReadingFormset)



















