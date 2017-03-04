#The only function in this module is the printer function.
#Functions as a pretty printer for Nested Dictionaries and Nested Lists

#Recursive Function printer. Accpts the structure and the number of tabs so far.
def printer(a, tab = 0):
	#Handling lists
	if type(a) == type(list()):
		for i in a:
			printer(i, tab)
	#Handling dictionaries
	elif type(a) == type(dict()):
		#Scans all the elements in the dictionary
		for i in a:
			#Recursively calls the printer function with the new data structure and an incremented tab count.
			if(type(a[i]) == type(dict())):
				for j in xrange(tab):
					print '\t',
				print i,': '
				printer(a[i], tab+1)
			elif type(a[i]) == type(list()):
				for j in xrange(tab):
					print '\t',
				print i,': '
				printer(a[i], tab+1)
			else:
				for j in xrange(tab):
					print '\t',
				print i, ': ', a[i]
	#Handling any other type format
	else:
		for i in xrange(tab+1):
			print '\t',
		print a
