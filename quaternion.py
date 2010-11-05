import numpy as np
def AutoFloatProperties(*props):
	class _AutoFloatProperties(type):
		def __init__(cls, name, bases, cdict):
			super(_AutoFloatProperties, cls).__init__(name, bases, cdict)
			for attr in props:
				def fget(self, _attr='_'+attr): return getattr(self, _attr)
				def fset(self, value, _attr='_'+attr): setattr(self, _attr, float(value))
				setattr(cls, attr, property(fget, fset))
	return _AutoFloatProperties

class Vector():
	"""
		Vector class. Implemented:
		 - vector summ
		 - vector scalar multiplication
		 - vector vectorial multiplication
		 - vector multiplication by scalar value (left + right)
		 - vector negative
		 - all input converted to floats by a metaclass
	"""
	__metaclass__ = AutoFloatProperties('x','y','z')
	def __init__(self, vector):
		self.x, self.y, self.z = vector
	
	def __add__(self, other):
		"""Vector summing"""
		if isinstance(other, Vector):
			return Vector((self.x + other.x, self.y + other.y, self.z + other.z))
		else:
			raise TypeError('Vector can be added only to vector')
	
	def __sub__(self, other):
		"""Vector subtraction"""
		if isinstance(other, Vector):
			return Vector((self.x - other.x, self.y - other.y, self.z - other.z))
		else:
			raise TypeError('Vector can be subtracted only from vector')
	
	def __mul__(self, other):
		"""Scalar multiplication"""
		if (isinstance(other, Vector)):
			return self.x * other.x + self.y * other.y + self.z * other.z
		elif isinstance(other, (int, float)):
			return Vector((self.x * other, self.y * other, self.z * other))
		else:
			raise TypeError('Vector can be multiplied only by vector or scalar value (int, float)')
	
	def __rmul__(self, other):
		"""Scalar multiplication from the right side"""
		if isinstance(other, (int, float)):
			return Vector((self.x * other, self.y * other, self.z * other))
		else:
			raise TypeError('Vector right side multiplication only by scalar value (int, float)')
	
	def __pow__(self, other):
		"""Vector cross product"""
		if isinstance(other, Vector):
			return Vector(((self.y * other.z - self.z * other.y), (self.z * other.x - self.x * other.z), (self.x * other.y - self.y * other.x)))
		else:
			raise TypeError('Vector cross product can be done only with another vector')
	
	def __neg__(self):
		return self * (-1)
	
	def __abs__(self):
		"""Absolute vector value - length"""
		"""Can be replaced with """
		return np.sqrt(self * self)
	
	def __getitem__(self, index):
		"""Get value listwise"""
		data = [self.x, self.y, self.z]
		if index in range(3):
			return data[index]
		else:
			raise IndexError('Index error: [vector.x, vector.y, vector.z]')
	
	def __setitem__(self, key, item):
		"""Set value listwise"""
		if (key == 0):
			self.x = item
		elif (key == 1):
			self.y = item
		elif (key == 2):
			self.z = item
		else:
			raise IndexError('Index error: [vector.x, vector.y, vector.z]')
	
	def __repr__(self):
		return "(%.2f, %.2f, %.2f)" % (self.x, self.y, self.z)
	
	def unitize(self):
		"""Unit vector"""
		return Vector(self * (1 / abs(self)))

"""
	TODO: Implement Functions of a quaternion variable http://en.wikipedia.org/wiki/Quaternion
"""
class Quaternion():
	"""
		Quaternion class. Implemented:
		 - multiple constructors
		 TODO: write full description here
	
	"""
	def __init__(self, scalar, vector):
		vector = vector
		if isinstance(vector, Vector):
			self.s = scalar
			self.v = vector
		elif isinstance(vector, (list, tuple)):
			self.s = scalar
			self.v = Vector(vector)
		else:
			raise TypeError('Quaternion takes scalar part and vector part represented as vector or tuple/list')
	
	def __add__(self, other):
		if (isinstance(other, Quaternion)):
			return Quaternion(self.s + other.s, self.v + other.v)
		else:
			raise TypeError('Quaternion must be added only to quaternion')
	
	def __mul__(self, other):
		if isinstance(other, Quaternion):
			return Quaternion((self.s * other.s) - (self.v * other.v), (self.s * other.v) + (other.s * self.v) + (self.v ** other.v))
		elif isinstance(other, (int, float)):
			return Quaternion(self.s * other, self.v * other)
		elif isinstance(other, (list, tuple)) and len(other) == 3:
			return self * Quaternion(0, Vector(other))
		elif isinstance(other, Vector):
			return self * Quaternion(0, other)
		else:
			raise TypeError('Quaternion must be multiplyed only with quaternion, vector, list, tuple')		
	
	def __neg__(self):
		"""Quaternion conjugation"""
		return Quaternion(self.s, -self.v)
	
	def __abs__(self):
		"""Quaternion absolute value"""
		return np.sqrt((self * -self).s)
	
	def __invert__(self):
		"""Reciprocal of a quaternion"""
		return -self * (1 / abs(self)**2)
	
	def __getitem__(self, index):
		"""Get value listwise"""
		data = [slef.s, self.v.x, self.v.y, self.v.z]
		if index in range(4):
			return data[index]
		else:
			raise IndexError('Index error: [scalar, vector.x, vector.y, vector.z]')
	
	def __setitem__(self, key, item):
		"""Set value listwise"""
		if (key == 0):
			self.s = item
		elif (key == 1):
			self.v.x = item
		elif (key == 2):
			self.v.y = item
		elif (key == 3):
			self.v.z = item
		else:
			raise IndexError('Index error: [scalar, vector.x, vector.y, vector.z]')
	
	def __repr__(self):
		if self.s != 0:
			return "(%.2f, (%.2f, %.2f, %.2f))" % (self.s, self.v.x, self.v.y, self.v.z)
		else:
			return "(%.2f, %.2f, %.2f)" % (self.v.x, self.v.y, self.v.z)
	
	def transformPoint(self, point):
		"""Transforms point with current quaternion"""
		if (len(point) == 3):
			return (~self * point * self).v
		else:
			raise TypeError('Please specify point of 3 coordinates')

