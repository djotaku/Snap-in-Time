import snapintime
import unittest

class PriorDays(unittest.TestCase):
  def testWeekly(self):
   result = snapintime.createpriordaysmaster("1","14","weekly")
   self.assertEqual((['1'],[1,2,3,4,5,6,7]),result)
    
if __name__=="__main__":
  unittest.main()