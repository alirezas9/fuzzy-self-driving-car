import numpy as np 

class FuzzyController:

    def __init__(self):
        pass

    def dist_fuzzify(self, dist):
        """
        Fuzzify the distance to an obstacle into three fuzzy sets: close, medium, and far.
        """
        if dist <= 35:
            return {'close': (1 - dist/50), 'medium': 0.0, 'far': 0.0}
        elif dist > 35 and dist <= 50:
            return {'close': (1 - dist/50), 'medium': (dist/15 - 7/3), 'far': 0.0}
        elif dist > 50 and dist <= 65:
            return {'close': 0.0, 'medium': (-dist/15 + 13/3), 'far': (dist/50 - 1.0)}
        elif dist > 65 and dist <= 100 :
            return {'close': 0.0, 'medium': 0.0, 'far': (dist/50 - 1.0)}
        else :
            return {'close': 0.0, 'medium': 0.0, 'far': 0.0}

    def fuzzify(self, left_dist, right_dist):
        """
        Fuzzify the distance to an obstacle into three fuzzy sets: close, medium, and far.
        """
        l = self.dist_fuzzify(left_dist)
        r = self.dist_fuzzify(right_dist)
        cl = l['close']
        ml = l['medium']
        fl = l['far']
        cr = r['close']
        mr = r['medium']
        fr = r['far']
        return {'cl':cl, 'ml':ml, 'fl':fl, 'cr':cr, 'mr':mr, 'fr':fr}

    def inference(self ,dist):
        """
        Inference the distance to an obstacle into three fuzzy sets: close, medium, and far.
        """
        cl = dist['cl']
        ml = dist['ml']
        fl = dist['fl']
        cr = dist['cr']
        mr = dist['mr']
        fr = dist['fr']
        lr = min(cl, mr)
        hr = min(cl, fr)
        ll = min(ml, cr)
        hl = min(fl, cr)
        noth =min(ml, mr)
        return {'lr':lr, 'hr':hr, 'll':ll, 'hl':hl, 'noth':noth}
    
    def high_right(self,i ,hr):
        if i >-50 and i < -5:
            if i < -20 :
                return min(hr ,(i+50)/30)
            else:
                return min(hr ,-(i+5)/15)   
        else:
            return 0
    def low_right(self,i ,lr):
        if i >-20 and i < 0:
            if i < -10 :
                return min(lr , (i/10 + 2))
            else:
                return min(lr ,-(i/10))   
        else:
            return 0
    def nothing(self,i ,noth):
        if i >-10 and i < 10:
            if i < 0 :
                return min(noth ,(i/10 + 1))
            else:
                return min(noth ,(1 - i/10))   
        else:
            return 0
    def low_left(self,i ,ll):
        if i >0 and i < 20:
            if i < 10 :
                return min(ll , (i/10))
            else:
                return min(ll ,(2-(i/10)))
        else:
            return 0
        
    def high_left(self,i ,hl):
        if i > 5 and i < 50:
            if i < 20 :
                return min(hl ,(i-5)/15)
            else:
                return min(hl ,(50-i)/30)   
        else:
            return 0

    def defuzzify(self, mfx):
        """
        Defuzzify the distance to an obstacle into three fuzzy sets: close, medium, and far.
        """
        lr = mfx['lr']
        hr = mfx['hr']
        ll = mfx['ll']
        hl = mfx['hl']
        noth = mfx['noth']
        num = 0.0
        denum = 0.0
        
        x = np.linspace(-50,50,1000)
        delta = x[1] - x[0]
        for i in x:
            u = max(self.high_right(i, hr) , self.low_right(i, lr) , \
                    self.nothing(i, noth) , self.low_left(i, ll) , self.high_left(i, hl))
            num += u * i * delta
            denum += u * delta
        return num/denum if denum != 0 else 0

    
    def decide(self, left_dist,right_dist):
        """
        main method for doin all the phases and returning the final answer for rotation
        """
        fuzz = self.fuzzify(left_dist,right_dist)
        infer = self.inference(fuzz)
        rot = self.defuzzify(infer)
        return rot
    