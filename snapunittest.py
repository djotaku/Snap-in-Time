import snapintime
import unittest
 
#run with -v for verbose output
 
class PriorDays(unittest.TestCase):
  def testWeekly(self):
   """createpriordaysmaster should produce the right days for a weekly test"""
   result = snapintime.createpriordaysmaster("1","14","weekly")
   self.assertEqual((['1'],[1,2,3,4,5,6,7]),result)

  def testWeekly2(self):
   """createpriordaysmaster should produce the right days for a weekly test - 7 days later"""
   result = snapintime.createpriordaysmaster("1","21","weekly")
   self.assertEqual((['1'],[8,9,10,11,12,13,14]),result)

  def testWeeklyEarlyinMonth(self):
   """createpriordaysmaster should produce the right days for a weekly test if it has to go to the previous month"""
   result = snapintime.createpriordaysmaster("2","13","weekly")
   self.assertEqual((['1','2'],[[31],[1,2,3,4,5,6]]),result)

  def testWeeklyEarliestinMonth(self):
   """createpriordaysmaster should produce the right days for a weekly test if it has to go to the previous month, even if it's day 1"""
   result = snapintime.createpriordaysmaster("2","1","weekly")
   self.assertEqual((['1','2'],[[19,20,21,22,23,24,25],[]]),result)

    
if __name__=="__main__":
  unittest.main()