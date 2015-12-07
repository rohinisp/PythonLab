from pint import UnitRegistry
ureg = UnitRegistry()
distance = 24.0 * ureg.meter
print(distance)
print(distance.magnitude)
print(distance.units)
print(distance.dimensionality)
time = 8.0 * ureg.second
print(time)
print(repr(time))
speed = distance / time
print(speed)
speed.to(ureg.inch / ureg.minute )
print(speed)
speed.ito(ureg.inch / ureg.minute )
print(speed)
#speed.to(ureg.joule)
