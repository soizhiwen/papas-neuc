import math
from point import Point

class InverseKinematics:
    def __init__(self):
        pass

    def cal(self, ef, pp):
        # servo circles
        pCircle1 = Point(-98, 0)
        pCircle2 = Point(98, 0)
        rCircle1, rCircle2 = 150, 150

        # middle arm circle
        pCircle3, pCircle4 = None, None

        # nozzle circle
        # intersecting with (pCircle1.x, pCircle1.y) and (pCircle2.x, pCircle2.y)
        # maximum y = (0, 387)
        # maximum x = (300, 0)
        pCircle5 = Point(ef[0], ef[1])
        rCircle5 = 260

        nLeft1, nLeft2 = None, None

        intersections = self.getCircleIntersections(
            pCircle1, rCircle1, pCircle5, rCircle5
        )
        if intersections is not None:
            nLeft1, nLeft2 = intersections

        nRight1, nRight2 = None, None

        intersections = self.getCircleIntersections(
            pCircle2, rCircle2, pCircle5, rCircle5
        )
        if intersections is not None:
            nRight1, nRight2 = intersections

        pos = []
        if all(v is not None for v in [nLeft1, nLeft2, nRight1, nRight2]):
            if self.isCollide(nLeft1.x, nRight2.x):
                pos = [(nLeft1, nRight1), (nLeft2, nRight1), (nLeft2, nRight2)]
            elif self.isCollide(nLeft2.x, nRight1.x):
                pos = [(nLeft1, nRight1), (nLeft1, nRight2), (nLeft2, nRight2)]
            else:
                pos = [
                    (nLeft1, nRight1),
                    (nLeft1, nRight2),
                    (nLeft2, nRight1),
                    (nLeft2, nRight2),
                ]

        if pos:
            diff = []
            angle = []
            leftPp, rightPp = pp  # goal - present = abs(distance)
            for p in pos:
                pCircle3, pCircle4 = p
                arm1 = ([pCircle1.x, pCircle1.y], [pCircle3.x, pCircle3.y])
                arm2 = ([pCircle2.x, pCircle2.y], [pCircle4.x, pCircle4.y])
                angle1, angle2 = self.getAngle(arm1), self.getAngle(arm2)
                angle1 = (-180 + angle1) if angle1 >= 0 else (angle1 + 180)
                diffLeft = abs(angle1 - leftPp)
                diffRight = abs(angle2 - rightPp)
                diff.append(diffLeft + diffRight)
                angle.append((angle1, angle2))
            index = diff.index(min(diff))
            angle1 = angle[index][0]
            angle2 = angle[index][1]
            angle1 = round(angle1 * 4096 / 360)
            angle2 = round(angle2 * 4096 / 360)

            return (angle1, angle2)

        print("No point at Circle 3 and Circle 4")
        return (None, None)

    def getCircleIntersections(self, p, rP, q, rQ):
        # circle 1: (p.x, p.y), radius rP
        # circle 2: (q.x, q.y), radius rQ

        d = math.sqrt((q.x - p.x) ** 2 + (q.y - p.y) ** 2)

        # non intersecting
        if d > rP + rQ:
            return None
        # One circle within other
        if d < abs(rP - rQ):
            return None
        # coincident circles
        if d == 0 and rP == rQ:
            return None
        else:
            a = (rP ** 2 - rQ ** 2 + d ** 2) / (2 * d)
            h = math.sqrt(rP ** 2 - a ** 2)
            p1 = Point(None, None)
            p2 = Point(None, None)
            p2.x = p.x + a * (q.x - p.x) / d
            p2.y = p.y + a * (q.y - p.y) / d
            p1.x = p2.x + h * (q.y - p.y) / d
            p1.y = p2.y - h * (q.x - p.x) / d

            p2.x = p2.x - h * (q.y - p.y) / d
            p2.y = p2.y + h * (q.x - p.x) / d

            return (p1, p2)

    def isCollide(self, x1, x2):
        if x2 < x1:
            return True
        return False

    def getAngle(self, line):

        # Angle between line1 and x-axis
        y = line[1][1] - line[0][1]
        x = line[1][0] - line[0][0]
        return math.degrees(math.atan2(y, x))  # Taking only the positive angle
