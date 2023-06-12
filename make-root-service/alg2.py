import datetime

def order_by_time(nodes):
    sorted_keys = [(key, str(value)) for key, value in sorted(nodes.items(), key=lambda item: item[1])]
    return sorted_keys

def convert_time_to_minutes(time):
	if(time == None):
		return None
	else:
		return time.hour * 60 + time.minute

def compact(uncompacted_route, dist_matrix, node_limit):
	fixed_nodes = [k for k, v in node_limit.items()]
	right_free_nodes = [node for node in uncompacted_route if node not in fixed_nodes]

	nodes = {}

	n = uncompacted_route[0]

	if(len(node_limit) != 0):
		n = list(node_limit.keys())[0]
		if(node_limit[n][0] is None):
			nodes[n] = node_limit[n][1]
		elif(node_limit[n][1] is None):
			nodes[n] = node_limit[n][0]
	else:
		nodes[n] = 0
		
	
	for i in range(uncompacted_route.index(n) + 1, len(uncompacted_route)):
		new_time = nodes[uncompacted_route[i - 1]] + dist_matrix[int(uncompacted_route[i - 1])][int(uncompacted_route[i])]
		nodes[uncompacted_route[i]] = new_time
	

	for i in range(0, uncompacted_route.index(n))[::-1]:
		new_time = nodes[uncompacted_route[i + 1]] - dist_matrix[int(uncompacted_route[i])][int(uncompacted_route[i + 1])]
		nodes[uncompacted_route[i]] = new_time
		

	route = order_by_time(nodes)

	right_time_shift_possible = {k : 0 for k in node_limit}

	for k, limit in node_limit.items():
		if(limit[1] is not None):
			if(nodes[k] < limit[1]):
				right_time_shift_possible[k] += limit[1] - nodes[k]
			else:
				right_time_shift_possible[k] = 0
		else:
			right_time_shift_possible[k] = 9999

	left_time_shift_possible = {k : 0 for k in node_limit}

	for k, limit in node_limit.items():
		if(limit[0] is not None):
			if(nodes[k] > limit[0]):
				left_time_shift_possible[k] +=  - limit[0] + nodes[k]
			else:
				left_time_shift_possible[k] = 0
		else:
			left_time_shift_possible[k] = 9999

	time_shift = {k : 0 for k in node_limit}

	for k, limit in node_limit.items():
		if(limit[0] is not None):
			if(nodes[k] < limit[0]):
				time_shift[k] += limit[0] - nodes[k]
		if(limit[1] is not None):
			if(nodes[k] > limit[1]):
				time_shift[k] += limit[1] - nodes[k]

	if(time_shift != {}):
		needed_shift = max(0, max(time_shift.values())) + min(0, min(time_shift.values()))

		print("needed_shift: " + str(needed_shift))

		shift = 0
		if(needed_shift > 0):
			shift = min(needed_shift, min(right_time_shift_possible.values()))
			print("shift: " + str(shift))
			for k in nodes:
				nodes[k] += shift
		elif(needed_shift < 0):
			shift = max(needed_shift, -min(left_time_shift_possible.values()))
			print("shift: " + str(shift))
			for k in nodes:
				nodes[k] += shift

		if(needed_shift < 15 and needed_shift > -15 and shift == 0):
			for k in nodes:
				nodes[k] += needed_shift/2
	
	route = order_by_time(nodes)

	travel_time = nodes[route[-1][0]] - nodes[route[0][0]]
	acceptable_deviances = []
	unacceptable_deviances = []
	for k, v in node_limit.items():
		lb , ub = v
		print("lb: " + str(lb) + " ub: " + str(ub) + " node: " + str(nodes[k]))
		if(lb is not None):
			if(nodes[k] < lb):
				unacceptable_deviances.append(lb - nodes[k])
			else:
				acceptable_deviances.append(nodes[k] - lb)
		if(ub is not None):
			if(nodes[k] > ub):
				unacceptable_deviances.append(nodes[k] - ub)
			else:
				acceptable_deviances.append(ub - nodes[k])
	if(len(node_limit) != 0):
		mean_acceptable_deviance = round(sum(acceptable_deviances) / len(node_limit), 2)
		mean_unacceptable_deviance = round(sum(unacceptable_deviances) / len(node_limit), 2)
	else:
		mean_acceptable_deviance = 0
		mean_unacceptable_deviance = 0


	if acceptable_deviances == []:
		max_acceptable_deviances = 0
	else:
		max_acceptable_deviances = max(acceptable_deviances)
	if unacceptable_deviances == []:
		max_unacceptable_deviances = 0
	else:
		max_unacceptable_deviances = max(unacceptable_deviances)
	n_tardy = len(unacceptable_deviances)
	return (route, travel_time, n_tardy ,mean_unacceptable_deviance, max_unacceptable_deviances, mean_acceptable_deviance, max_acceptable_deviances)


if __name__ == "__main__":
	dist_matrix =  [[0, 20, 10, 30, 20, 30],
					[20, 0, 10, 20, 10, 20],
					[10, 10, 0, 20, 10, 20],
					[30, 20, 20, 0, 10, 10],
					[20, 10, 10, 10, 0, 10],
					[30, 20, 20, 10, 10, 0]]
	pred_hash = {'0': ['1'], '1': [], '2': ['3'], '3': [], '4': ['5'], '5': []}
	node_limit = {'1': (None, datetime.time(13, 55)),
			'3': (datetime.time(14, 10), datetime.time(14, 40)),
			'5': (datetime.time(14, 45), None)}
	
	node_limit_min = {k : (convert_time_to_minutes(v[0]), convert_time_to_minutes(v[1])) for k, v in node_limit.items()}

	
	print(compact(['0', '1', '2', '4', '3', '5'], dist_matrix, {}))
	