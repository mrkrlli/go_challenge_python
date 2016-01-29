# -*- coding: utf-8 -*-
import unittest
import decoder

#run "python decoder_test.py" in command line while in this file's directory
#these tests check that each decoded pattern matches the given pattern on the Go challenge page

class TestDecodeFile(unittest.TestCase):

	def test_pattern_1(self):
	  	pattern = decoder.decode_file('fixtures/pattern_1.splice')

		expected_pattern = "Saved with HW Version: 0.808-alpha\n" + \
						   "Tempo: 120\n" + \
						   "(0) kick     |x---|x---|x---|x---|\n" + \
						   "(1) snare    |----|x---|----|x---|\n" + \
						   "(2) clap     |----|x-x-|----|----|\n" + \
						   "(3) hh-open  |--x-|--x-|x-x-|--x-|\n" + \
						   "(4) hh-close |x---|x---|----|x--x|\n" + \
						   "(5) cowbell  |----|----|--x-|----|"

		#print expected_pattern
	  	self.assertEqual(pattern, expected_pattern)


	def test_pattern_2(self):
	  	pattern = decoder.decode_file('fixtures/pattern_2.splice')

		expected_pattern = "Saved with HW Version: 0.808-alpha\n" + \
						   "Tempo: 98.4\n" + \
						   "(0) kick    |x---|----|x---|----|\n" + \
						   "(1) snare   |----|x---|----|x---|\n" + \
						   "(3) hh-open |--x-|--x-|x-x-|--x-|\n" + \
						   "(5) cowbell |----|----|x---|----|"

		#print expected_pattern
	  	self.assertEqual(pattern, expected_pattern)


	def test_pattern_3(self):
	  	pattern = decoder.decode_file('fixtures/pattern_3.splice')

		expected_pattern = "Saved with HW Version: 0.808-alpha\n" + \
						   "Tempo: 118\n" + \
							"(40) kick    |x---|----|x---|----|\n" + \
							"(1) clap     |----|x---|----|x---|\n" + \
							"(3) hh-open  |--x-|--x-|x-x-|--x-|\n" + \
							"(5) low-tom  |----|---x|----|----|\n" + \
							"(12) mid-tom |----|----|x---|----|\n" + \
							"(9) hi-tom   |----|----|-x--|----|"

		#print expected_pattern
	  	self.assertEqual(pattern, expected_pattern)


	def test_pattern_4(self):
	  	pattern = decoder.decode_file('fixtures/pattern_4.splice')

		expected_pattern = "Saved with HW Version: 0.909\n" + \
							"Tempo: 240\n" + \
							"(0) SubKick       |----|----|----|----|\n" + \
							"(1) Kick          |x---|----|x---|----|\n" + \
							"(99) Maracas      |x-x-|x-x-|x-x-|x-x-|\n" + \
							"(255) Low Conga   |----|x---|----|x---|"

		#print expected_pattern
	  	self.assertEqual(pattern, expected_pattern)


	def test_pattern_5(self):
	  	pattern = decoder.decode_file('fixtures/pattern_5.splice')

		expected_pattern = "Saved with HW Version: 0.708-alpha\n" + \
							"Tempo: 999\n" + \
							"(1) Kick    |x---|----|x---|----|\n" + \
							"(2) HiHat   |x-x-|x-x-|x-x-|x-x-|"

		#print expected_pattern
	  	self.assertEqual(pattern, expected_pattern)



if __name__ == '__main__':
    unittest.main()