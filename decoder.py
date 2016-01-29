# -*- coding: utf-8 -*-
import struct

def decode_file(file_location):
	#firstly, open the file
	f = open(file_location, "rb")

	#now read the binary file
	data = f.read()

	#now extract the relevant information from the data
	drum_info = {
		'version': extract_version(data),
		'tempo': extract_tempo(data),
		'tracks': extract_tracks(data)
	}

	#format each track's information, and add it to the total tracks pattern string
	tracks_pattern_string = ""

	#loop through all the track+id pattern strings to determine which track has the longest one 
	#this will be used to know how many spaces to add to the track name and 16 steps later on
	track_name_and_id_length = []
	for x in drum_info['tracks']:
		id_and_name_pattern_string = "({0}) {1}".format(x['track_id'], x['track_name'])
		track_name_and_id_length.append(len(id_and_name_pattern_string))

	for x in drum_info['tracks']:

		#create the 16 step pattern string
		step_pattern_string = ""

		#add in the triggered and nontriggered step pattern characters
		for y in x['track_16_steps']:
			if y =="01":
				step_pattern_string = step_pattern_string + "x"
			else:
				step_pattern_string = step_pattern_string + "-"

		#now add in the pipes separators
		step_pattern_string = '|'.join(step_pattern_string[i:i+4] for i in range(0, len(step_pattern_string), 4))

		#add the pipe characters to the end and start as well
		step_pattern_string = "|" + step_pattern_string + "|"

		#create the id and name pattern string
		id_and_name_pattern_string = "({0}) {1}".format(x['track_id'], x['track_name'])

		#figure out how much space b/t the end of the track name and the start of the 16 steps pattern string
		#for 808-alpha, it seems that the space is determined by adding 1 space to the longest track + id string
		#for 909 and 708, it's 3 spaces
		if "808" in drum_info['version']:
			spaces_added = 1
		else:
			spaces_added = 3

		spaces_needed = (max(track_name_and_id_length) + spaces_added) - len(id_and_name_pattern_string)

		#the 16 steps pattern string is always 13 spaces from the start of each track's pattern string
		#spaces_needed = 13 - len(id_and_name_pattern_string)

		#create the track's full pattern string
		individual_track_pattern = id_and_name_pattern_string + (" " * spaces_needed) + step_pattern_string
		
		tracks_pattern_string = tracks_pattern_string + "\n" + individual_track_pattern


	#now create the whole drum pattern string
	drum_pattern = """Saved with HW Version: {0}\nTempo: {1}{2}""".format(drum_info['version'], drum_info['tempo'], tracks_pattern_string)

	print drum_pattern
	return drum_pattern

def extract_version(data):
	#start at offset/index 14 for the data, and end when you reach the first hexadecimal value == 00
	#Use a loop to find the offset/index where the version information ends
	#start at index 14 and keep going until you reach a hexadecimal value of 00
	index = 14
	while data[index].encode('hex') != "00":
		index += 1

	#now we know where the version data starts and ends
	#return this data encoded in ascii
	return data[14:index].encode('ascii')


def extract_tempo(data):
	#encode the byte data from index points 46 to 50 as a floating point number with little endian byte order
	tempo_floating = struct.unpack('<f', data[46:50])[0]

	#any insignificant trailing zeros and decimal points need to be removed in the returned string
	#format type 'g' does this in Python
	return '{0:g}'.format(tempo_floating)


def extract_tracks(data):
	#the tracks' data starts at index 50
	track_starting_index = 50

	#extract each track data (id, name, 16 steps) sequentially, until you reach the end of the data
	tracks = []

	while track_starting_index < len(data):
		#there seems to be a bug or anomaly in pattern_5, where there is extra repeated data at the end
		#this will make sure that this loop will stop if if encounters this repeated data
		if track_starting_index + 6 < len(data) and data[track_starting_index: track_starting_index+6].encode('hex')=="53504c494345":
			break

		#track id data is the first byte for the given track (index 0 for the given track). Going to encode it as a hex (base 16) and then convert it to an decimal
		track_id = int(data[track_starting_index].encode('hex'), 16)

		#the name data for the track starts at index 5 (for the given track) and ends right before the first hexadecimal value of 00 or 01 (this is where the 16 steps data starts)
		#find where the data for the track name ends by finding the index of the first 00 or 01 hexadecimal value
		track_name_ending_index = track_starting_index + 5
		while data[track_name_ending_index].encode('hex') not in ["00", "01"]:
			track_name_ending_index += 1

		#encode the bytes in ascii to give the track name
		track_name = data[track_starting_index + 5: track_name_ending_index].encode('ascii')

		#the next 16 bytes will be the 16 steps data. Hexadecimal value of 01 represnts a triggered step, and 00 represents an untriggered step
		#create a list, adding each steps hexadecimal value sequentially to the list to represent the 16 steps
		track_16_steps = []
		i = 0
		while i<16:
			track_16_steps.append(data[track_name_ending_index + i].encode('hex'))
			i += 1

		# add this track's information (as a dictionary) to the tracks list
		tracks.append(
			{
				"track_id": track_id,
				"track_name": track_name,
				"track_16_steps": track_16_steps
			}
		)

		#set the next track's starting index
		track_starting_index = track_name_ending_index + 16

	return tracks
