import unittest
import rect_areas as ra

def addpoint(p1, p2):
    return (p1[0]+p2[0], p1[1]+p2[1])

class TestImageFocus(unittest.TestCase):
    r1 = ((10, 10), (90, 80))
    r2 = ((10, 90), (90, 160))
    r3 = ((100, 50), (150, 120))
    rectangles = [r1, r2, r3]

    def test_opposite(self):
        self.assertEqual(ra.DOWN, ra.getopposite(ra.UP))

    def test_start(self):
        self.assertEqual(ra.find_start_rect(self.rectangles), self.r1)


    def test_edge(self):
        r = ((10, 20), (90, 110))
        edger = (90, 20, 110)
        edgel = (10, 20, 110)
        edgeu = (20, 10, 90)
        edged = (110, 10, 90)
        self.assertEqual(ra.get_edge(r, ra.UP), edgeu)
        self.assertEqual(ra.get_edge(r, ra.RIGHT), edger)
        self.assertEqual(ra.get_edge(r, ra.DOWN), edged)
        self.assertEqual(ra.get_edge(r, ra.LEFT), edgel)

    def test_collision_edge(self):
        e = (614, 1034, 1484)
        p = (1012, 606)
        ce = ra.get_collision_edge(e, ra.UP, ra.RIGHT, p)
        self.assertEqual((e[0]-ra.AREA_GAP, 1012, 1484+ra.AREA_GAP), ce)

        e = (1514, 14, 1169)
        p = (1514-ra.AREA_BORDER, 614-ra.AREA_BORDER)
        ce = ra.get_collision_edge(e, ra.LEFT, ra.UP, p)
        self.assertEqual((e[0]-ra.AREA_GAP, e[1]-ra.AREA_GAP, p[1]), ce)

    #     cp = ra.get_collision_point(ra.get_edge(self.r1, ra.RIGHT), ra.RIGHT, ra.DOWN, ra.get_edge(self.r3, ra.UP))
    #     self.assertEqual(cp, (self.r1[1][0]+ra.AREA_BORDER, self.r3[0][1]-ra.AREA_BORDER))

    # def test_collision(self):
    #     rectangles = [self.r1, self.r2, self.r3]
    #     self.assertEqual(ra.turn_after_collision(rectangles, ra.get_edge(self.r1, ra.UP), ra.UP, ra.RIGHT), None)

    #     collision = ra.turn_after_collision(rectangles, ra.get_edge(self.r1, ra.RIGHT), ra.RIGHT, ra.DOWN)
    #     self.assertEqual(collision[0], (self.r1[1][0]+ra.AREA_BORDER, self.r3[0][1]-ra.AREA_BORDER), msg='collision point')
    #     self.assertEqual(collision[1], ra.get_edge(self.r3, ra.UP), msg='collision next edge')
    #     self.assertEqual(collision[2], (ra.UP, ra.RIGHT), msg='collision next edge name-direction')
        
    #     collision = ra.turn_after_collision(rectangles, ra.get_edge(self.r3, ra.DOWN), ra.DOWN, ra.LEFT)
    #     self.assertEqual(collision[0], (self.r1[1][0]+ra.AREA_BORDER, self.r3[1][1]+ra.AREA_BORDER), msg='collision point')
    #     self.assertEqual(collision[1], ra.get_edge(self.r2, ra.RIGHT), msg='collision next edge')
    #     self.assertEqual(collision[2], (ra.RIGHT, ra.DOWN), msg='collision next edge name-direction')

    def test_continue_on(self):
        rectangles = [self.r1, self.r2, self.r3]

        nextedge = ra.continue_on(rectangles, ra.get_edge(self.r1, ra.UP), ra.UP, ra.RIGHT)
        self.assertEqual(nextedge, None)

        nextedge = ra.continue_on(rectangles, ra.get_edge(self.r2, ra.LEFT), ra.LEFT, ra.UP)
        self.assertEqual(nextedge, (ra.get_edge(self.r1, ra.LEFT), ra.LEFT, ra.UP))

    def test_points(self):
        b = ra.AREA_BORDER
        points = ra.find_traverse_points(self.rectangles)
        mypoints = [addpoint(self.r1[0],(-b,-b)), 
            addpoint((self.r1[1][0],self.r1[0][1]),(b,-b)), 
            addpoint((self.r1[1][0],self.r3[0][1]),(b,-b)), 
            addpoint((self.r3[1][0],self.r3[0][1]),(b,-b)), 
            addpoint((self.r3[1][0],self.r3[1][1]),(b,b)),
            addpoint((self.r2[1][0],self.r3[1][1]),(b,b)),
            addpoint(self.r2[1],(b,b)), 
            addpoint((self.r2[0][0],self.r2[1][1]),(-b,b))]
        self.assertEqual(points, mypoints, msg='CM area')

        r64 = ((554, 1034), (764, 1169))
        r65 = ((793, 1033), (1004, 1169))
        points = ra.find_traverse_points([r64,r65])
        mypoints = [addpoint(r64[0],(-b,-b)), 
            addpoint((r65[1][0], r65[0][1]),(b,-b)), 
            addpoint(r65[1],(b,b)), 
            addpoint((r64[0][0], r64[1][1]),(-b,b))]
        self.assertEqual(points, mypoints, 'tools area')

        r50 = ((554, 764), (1004, 1004)) 
        r43 = ((1034, 614), (1484, 884)) 
        r14 = ((554, 179), (1004, 734))          
        r5 = ((1514, 14), (1799, 1169))  
        points = ra.find_traverse_points([r50,r43,r14,r5])
        self.assertEqual(len(points), 12, 'CM area length')


        


if __name__ == '__main__':
    unittest.main()
