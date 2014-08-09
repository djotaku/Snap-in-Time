import snapintime
import unittest
 
#run with -v for verbose output
 
class PriorDays(unittest.TestCase):
  def testDaily(self):
    """createpriordaysmaster should produce the right days for a daily test in the middle of the month"""
    result = snapintime.createpriordaysmaster("1","14","daily")
    self.assertEqual(('1',[12]),result)
    
  def testDailyMonthDay1Feb(self):
    """createpriordaysmaster should produce the right days for a daily test first of the month"""
    result = snapintime.createpriordaysmaster("2","1","daily")
    self.assertEqual(('1',[30]),result) 
 
  def testDailyMonthDay2Feb(self):
    """createpriordaysmaster should produce the right days for a daily test first of the month"""
    result = snapintime.createpriordaysmaster("2","2","daily")
    self.assertEqual(('1',[31]),result)
  
  def testWeekly(self):
   """createpriordaysmaster should produce the right days for a weekly test"""
   result = snapintime.createpriordaysmaster("1","14","weekly")
   self.assertEqual((['1'],[1,2,3,4,5,6,7]),result)

  def testWeekly2(self):
   """createpriordaysmaster should produce the right days for a weekly test - 7 days later"""
   result = snapintime.createpriordaysmaster("1","21","weekly")
   self.assertEqual((['1'],[8,9,10,11,12,13,14]),result)

  def testWeeklyEarlyinMonthFeb(self):
   """createpriordaysmaster should produce the right days for a weekly test if it has to go to the previous month."""
   result = snapintime.createpriordaysmaster("2","13","weekly")
   self.assertEqual((['1','2'],[[31],[1,2,3,4,5,6]]),result)

  def testWeeklyEarlyinMonthFeb2(self):
   """createpriordaysmaster should produce the right days for a weekly test if it has to go to the previous month."""
   result = snapintime.createpriordaysmaster("2","12","weekly")
   self.assertEqual((['1','2'],[[30,31],[1,2,3,4,5]]),result)

  def testWeeklyEarlyinMonthFeb3(self):
   """createpriordaysmaster should produce the right days for a weekly test if it has to go to the previous month."""
   result = snapintime.createpriordaysmaster("2","8","weekly")
   self.assertEqual((['1','2'],[[26,27,28,29,30,31],[1]]),result)

  def testWeeklyEarlyinMonthFeb3(self):
   """createpriordaysmaster should produce the right days for a weekly test if it has to go to the previous month."""
   result = snapintime.createpriordaysmaster("2","7","weekly")
   self.assertEqual((['1','2'],[[25,26,27,28,29,30,31],[]]),result)

  def testWeeklyEarlyinMonthFeb4(self):
   """createpriordaysmaster should produce the right days for a weekly test if it has to go to the previous month."""
   result = snapintime.createpriordaysmaster("2","6","weekly")
   self.assertEqual((['1','2'],[[24,25,26,27,28,29,30],[]]),result)

  def testWeeklyEarliestinMonthFeb(self):
   """createpriordaysmaster should produce the right days for a weekly test if it has to go to the previous month, even if it's day 1"""
   result = snapintime.createpriordaysmaster("2","1","weekly")
   self.assertEqual((['1','2'],[[19,20,21,22,23,24,25],[]]),result)

  def testWeeklyEarlyinMonthMarch(self):
    """createpriordaysmaster should produce the right days for a weekly test if it has to go to the previous month"""
    result = snapintime.createpriordaysmaster("3","9","weekly")
    self.assertEqual((['2','3'],[[24,25,26,27,28],[1,2]]),result)

  def testWeeklyEarlyinMonthApril(self):
   """createpriordaysmaster should produce the right days for a weekly test if it has to go to the previous month"""
   result = snapintime.createpriordaysmaster("4","9","weekly")
   self.assertEqual((['3','4'],[[27,28,29,30,31],[1,2]]),result)

  def testWeeklyEarlyinMonthAug(self):
   """createpriordaysmaster should produce the right days for a weekly test if it has to go to the previous month"""
   result = snapintime.createpriordaysmaster("8","9","weekly")
   self.assertEqual((['7','8'],[[27,28,29,30,31],[1,2]]),result)
   
  #def testFirstQuarter(self):
   #"""createpriordaysmaster should produce the right days for a weekly test if it has to go to the previous month"""
   #result = snapintime.createpriordaysmaster("1","9","quarterly")
   #self.assertEqual((['10','11','12'],[]),result)   

  def testSecondQuarterApril(self):
   """createpriordaysmaster should produce the right days for a quartly test """
   result = snapintime.createpriordaysmaster("4","9","quarterly")
   self.assertEqual((['1','2','3'],[]),result)

  def testSecondQuarterMay(self):
   """createpriordaysmaster should produce the right days for a quartly test """
   result = snapintime.createpriordaysmaster("5","9","quarterly")
   self.assertEqual((['1','2','3'],[]),result)
   
  def testSecondQuarterJune(self):
   """createpriordaysmaster should produce the right days for a quartly test """
   result = snapintime.createpriordaysmaster("6","9","quarterly")
   self.assertEqual((['1','2','3'],[]),result)   

  def testThirdQuarterJuly(self):
   """createpriordaysmaster should produce the right days for a quartly test """
   result = snapintime.createpriordaysmaster("7","9","quarterly")
   self.assertEqual((['4','5','6'],[]),result)

  def testThirdQuarterAugust(self):
   """createpriordaysmaster should produce the right days for a quartly test """
   result = snapintime.createpriordaysmaster("8","9","quarterly")
   self.assertEqual((['4','5','6'],[]),result)
   
  def testThirdQuarterSeptember(self):
   """createpriordaysmaster should produce the right days for a quartly test """
   result = snapintime.createpriordaysmaster("9","9","quarterly")
   self.assertEqual((['4','5','6'],[]),result)   
   
  def testFourthQuarterOctober(self):
   """createpriordaysmaster should produce the right days for a quartly test """
   result = snapintime.createpriordaysmaster("10","9","quarterly")
   self.assertEqual((['7','8','9'],[]),result) 

  def testFourthQuarterNovember(self):
   """createpriordaysmaster should produce the right days for a quartly test """
   result = snapintime.createpriordaysmaster("11","9","quarterly")
   self.assertEqual((['7','8','9'],[]),result) 

  def testFourthQuarterDecember(self):
   """createpriordaysmaster should produce the right days for a quartly test """
   result = snapintime.createpriordaysmaster("12","9","quarterly")
   self.assertEqual((['7','8','9'],[]),result)    
   
if __name__=="__main__":
  unittest.main()