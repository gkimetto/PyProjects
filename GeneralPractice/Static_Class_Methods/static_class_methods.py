class Smoothie(object):
    YOGURT = 1
    STRAWBERRY = 2
    BANANA = 4
    MANGO = 8

    @staticmethod
    def blend(*mixes):
        return sum(mixes)/len(mixes)
    @classmethod
    def eternal_sunshine(cls):
        return cls.blend(cls.YOGURT, cls.STRAWBERRY,cls.BANANA)
    @classmethod
    def mango_lassi(cls):
        return cls.blend(cls.YOGURT, cls.MANGO)

class SmoothieMix(Smoothie):
    YOGURT = 'yogurt'
    STRAWBERRY = 'strawberry'
    BANANA = 'banana'
    MANGO = 'mango'

    @staticmethod
    def blend(*mixes):
        return ',  '.join(mixes)
