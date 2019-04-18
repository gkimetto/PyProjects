class Smoothie(object):
    YOGURT = 1
    STRAWBERRY = 2
    BANANA = 4
    MANGO = 8

    @staticmethod
    def blend(*mixes):
        return sum(mixes)/len(mixes)

    @staticmethod
    def eternal_sunshine():
        return Smoothie.blend(Smoothie.YOGURT,Smoothie.STRAWBERRY,Smoothie.BANANA)
    @staticmethod
    def mango_lassi():
        return Smoothie.blend(Smoothie.YOGURT,Smoothie.MANGO)

    blend_out = eternal_sunshine()
print ("This is a blend: {}".format(self.blend_out))