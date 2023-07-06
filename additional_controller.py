import numpy as np
class FuzzyGasController:
    """
    # emtiazi todo
    write all the fuzzify,inference,defuzzify method in this class
    """

    def __init__(self):
        pass

    def fuzzify(self, dist):
        """
        Fuzzify the distance to an obstacle into three fuzzy sets: close, medium, and far.
        """
        if dist <= 0:
            return {'close': 0.0, 'medium': 0.0, 'far': 0.0}
        elif dist > 0 and dist <= 40:
            return {'close': (1 - dist/50), 'medium': 0.0 , 'far': 0.0}
        elif dist > 40 and dist <= 50:
            return {'close': (1 - dist/50), 'medium': (dist/10 - 4), 'far': 0.0}
        elif dist > 50 and dist <= 90 :
            return {'close': 0.0, 'medium': (- dist/50 + 2), 'far': 0.0}
        elif dist > 90 and dist <= 100 :
            return {'close': 0.0, 'medium': (- dist/50 + 2), 'far': (dist/110 - 9/11)}
        elif dist > 100  :
            return {'close': 0.0, 'medium': 0.0 , 'far': max(1.0 ,(dist/110 - 9/11))}

    def inference(self, dist):
        """
        Inference the gas value based on the distance to an obstacle.
        """
        low = dist['close']
        med = dist['medium']
        high = dist['far']
        return {'low': low, 'med': med, 'high': high}

    def low(self,i ,l):
        if i >0 and i < 10:
            if i < 5 :
                return min(l ,i/5)
            else:
                return min(l ,-i/5 + 2)   
        else:
            return 0 
    def med(self,i ,m):
        if i >0 and i < 30:
            if i < 15 :
                return min(m , i/15)
            else:
                return min(m , -i/15 + 2)   
        else:
            return 0 
    def high(self,i ,h):
        if i > 25 and i < 90:
            if i < 30 :
                return min(h , i/5 - 5)
            else:
                return min(h ,i/60 + 1.5)   
        else:
            return 0

    def defuzzify(self, mfx):
        """
        Defuzzify the distance to an obstacle into three fuzzy sets: close, medium, and far.
        """
        l = mfx['low']
        m = mfx['med']
        h = mfx['high']

        num = 0.0
        denum = 0.0
        
        x = np.linspace(0,90,1000)
        delta = x[1] - x[0]
        for i in x:
            u = max(self.low(i,l),self.med(i,m),self.high(i,h))
            num += u * i * delta
            denum += u * delta
        return num/denum if denum != 0 else 0   
    
    def decide(self, center_dist):
        """
        main method for doin all the phases and returning the final answer for gas
        """
        fuzz = self.fuzzify(center_dist)
        infer = self.inference(fuzz)
        gas = self.defuzzify(infer)
        return  gas
    