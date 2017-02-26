from collections import defaultdict


class PhysicalQuantity(object):
    value = 0
    unit = None

    def __init__(self, value, unit_str=None, **kwargs):
        self.value = value
        if unit_str is None:
            self.unit = kwargs['unit_obj']
        else:
            self.unit = Unit(unit_str)

    def __repr__(self):
        return "%s %s"%(self.value.__repr__(), self.unit.__repr__())
    
    def __add__(self, other):
        return PhysicalQuantity(self.value + other.value, unit_obj=self.unit + other.unit)
    
    def __sub__(self, other):
        return PhysicalQuantity(self.value - other.value, unit_obj=self.unit - other.unit)

    def __mul__(self, other):
        return PhysicalQuantity(self.value * other.value, unit_obj=self.unit * other.unit)

    def __div__(self, other):
        return PhysicalQuantity(self.value / other.value, unit_obj=self.unit / other.unit)

    def __truediv__(self, other):
        return PhysicalQuantity(self.value / other.value, unit_obj=self.unit / other.unit)

    def __eq__(self, other):
        if self.value == other.value and self.unit == other.unit:
            return True
        else:
            return False


class Unit(object):
    def __init__(self, unit_str=None, **kwargs):
        if unit_str is None:
            self.powers = kwargs.get('powers', None)
        else: 
            self.powers = Unit.decompose(unit_str)
        if self.powers is None:
            print("creating unit failed. Powers = None")
         
    @classmethod
    def from_dict(cls, _powers):
        return cls(powers=_powers)

    def __eq__(self, other):
        if self.powers == other.powers:
            return True
        else:
            return False
    
    def __add__(self, other):
        if self == other:
            return self
        else:
            print("You can only add units of same type! Returning: None")
            return None

    def __sub__(self, other):
        return self+other

    def __mul__(self, other):
        res=defaultdict(lambda: 0)
        for name in self.powers.keys():
            res[name] += self.powers[name]
        for name in other.powers.keys():
            res[name] += other.powers[name]
        Unit.remove_zero_powers(res)  # dict is passed by reference, hence no return value
        return Unit.from_dict(dict(res))

    def __invert__(self):
        return Unit.from_dict(dict((i, -k) for i, k in self.powers.items()))

    def __div__(self, other):
        return self*(~other)

    def __truediv__(self, other):
        return self*(~other)

    def __repr__(self):

        if self.powers == {}:
            return "(no unit)"
        retpos = []
        retneg = []
        for name,power in self.powers.items():
            if float(power) == 1.:
                retpos.append(str(name))
            elif float(power).is_integer():
                if float(power) >= 0:
                    retpos.append(str(name)+'^'+str(int(power)))
                else:
                    retneg.append(str(name)+'^'+str(int(power)))
            else:
                if float(power) >= 0:
                    retpos.append(str(name)+"^"+str(power))
                else:
                    retneg.append(str(name)+"^"+str(power))
        retpos.extend(retneg)
        return '*'.join(retpos)

    @staticmethod
    def remove_zero_powers(power_dict):
        for key, val in power_dict.items():
            if val == 0:
                power_dict.pop(key)

    @staticmethod
    def decompose(unit_str):
        power_dict = {}
        if unit_str == "" or unit_str.isspace():
            return power_dict
        factors = unit_str.split('*')
        for fac in factors:
            divs = fac.split('/')
            try:
                name, power = divs[0].split('^')
                power_dict[name] = float(power)
            except:
                power_dict[divs[0]] = 1.
                
            for div in divs[1:]:
                try:
                    name, power = div.split('^')
                    power_dict[name] = -float(power)
                except:
                    power_dict[div] = -1.
        if '1' in power_dict:
            power_dict.pop('1')
        Unit.remove_zero_powers(power_dict)
        return power_dict

