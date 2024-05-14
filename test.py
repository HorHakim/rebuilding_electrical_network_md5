def min_bricolage(list_of_values):
	current_min = list_of_values[0]
	index_min = 0
	
	for index, value in enumerate(list_of_values[1: ]):
		if value <= current_min:
			current_min = value 
			index_min = index+1

	return current_min, index_min


L = [45, 22, 17, 32, 17]
print(min_bricolage(list_of_values=L))