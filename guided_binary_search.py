import random

inRange_counter = 0
obtained_range = [0,0]
loop_times = 0

def estimate_element_position(data,target,low,high):
	# omit the parameter check
	# since it will not exposed to user
	minVal = data[low]
	maxVal = data[high]
	if (target <= minVal):
		return low
	elif(target >= maxVal):
		return high
	else: # epos must between (low,high)
		epos = low + (high - low) * float(target - minVal)/(maxVal - minVal)
		return int(epos)

def guided_binary_search(data,target,alpha):
	global obtained_range, inRange_counter, loop_times
	# data is a list
	# target is value user want to search in the list
	# check the parameter
	if (data  == []):
		print "Invalid Input"
		return -1
	elemNum = len(data)
	low = 0
	high = elemNum - 1
	loop_counter = 0
	## statistical part##
	leftPos = 0
	rightPos = 0
	## statistical part##
	while (low <= high):
		if (loop_counter == 0):
			# estimate the postion for the first time
			mid = estimate_element_position(data,target,low,high)
			leftPos = mid
		elif(loop_counter == 1):
			# estimate the postion for the second time
			newMid = estimate_element_position(data,target,low,high)
			# add a offset to this new estimation position
			mid = int (newMid + (newMid-mid)*alpha)
			# dut to the offset, mid may bigger than high
			if (mid > high):
				mid = high
			if (mid < low):
				mid = low

			rightPos = mid
		else:
			# after est imated the position two times
			# use binary search strategy
			mid = low + ( (high-low)>>1 )

		loop_counter += 1
		if (data[mid] < target):
			low = mid+1
		elif (data[mid] > target) :
			high = mid-1
		else:
			### statistical part ####
			loop_times = loop_counter
			if (loop_counter <= 2):
				obtained_range = [mid , mid]
				inRange_counter += 1
			else:
				if (leftPos > rightPos):
					leftPos,rightPos = rightPos,leftPos
				obtained_range = [leftPos , rightPos]
				if (data[obtained_range[0]] <= target and target <= data[obtained_range[1]]):
					inRange_counter += 1
			### statistic part ####

			return mid

	### statistical part ####
	loop_times = loop_counter
	if (loop_counter <= 2):
		obtained_range = [0 , 0]
		inRange_counter += 1
	else:
		if (leftPos > rightPos):
			leftPos,rightPos = rightPos,leftPos
		obtained_range = [leftPos , rightPos]
		if (data[obtained_range[0]] <= target and target <= data[obtained_range[1]]):
			inRange_counter += 1
	### statistic part ####
	# not find
	return -1


if __name__ == '__main__':
	data = []
	alpha = 1
	dataLen = 2**20
	for i in range(dataLen):
		data.append(random.randint(1,0xffffFFFF))
	data.sort()
	print "Generate Completed, starting seach test"
	'''
	target = data[5]
	guided_binary_search(data,target,1)
	print obtained_range
	print loop_times
	print inRange_counter
	'''
	while alpha >= 0:
		rangeLen = 0
		totalComparsion = 0
		inRange_counter = 0
		for target in data:
			guided_binary_search(data,target,alpha)
			rangeLen += obtained_range[1]-obtained_range[0]
			totalComparsion += loop_times
		# print "Avg Range Length: %f, Probability: %f, Avg Comparsion:%f" \
		print "|%f | %f | %f|%f |" \
					  % (alpha, float(rangeLen)/dataLen,float(inRange_counter)/dataLen,float(totalComparsion)/dataLen)
		alpha -= 0.1


