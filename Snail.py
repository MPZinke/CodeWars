

# https://www.codewars.com/kata/521c2db8ddc89b9b7a0000c1


def snail(snail_map):
    snail_trail = []
    current_coordinates = [0, 0]
    coordinates_increments = [[0, 1], [1, 0], [0, -1], [-1, 0]]
    for x in range(len(snail_map) * len(snail_map)):
        snail_trail.append(snail_map[current_coordinates[0]][current_coordinates[1]])

        next_coordinates = [current_coordinates[y] + coordinates_increments[0][y] for y in [0, 1]]
        if(not(0 <= next_coordinates[0] < len(snail_map)) or not(0 <= next_coordinates[1] < len(snail_map))
          or snail_map[next_coordinates[0]][next_coordinates[1]] in snail_trail
        ):
            coordinates_increments = coordinates_increments[1:] + coordinates_increments[0:1]

        current_coordinates = [current_coordinates[y] + coordinates_increments[0][y] for y in [0, 1]]
        
    return snail_trail


def snail(snail_map):
    snail_trail = []
    while(snail_map):
        snail_trail += snail_map.pop(0)
        snail_trail += [row.pop(-1) for row in snail_map]
        if(not snail_map):
            break

        snail_trail += snail_map.pop(-1)[::-1]
        snail_trail += [row.pop(0) for row in snail_map[::-1]]

    return snail_trail


array = [[1,2,3],
         [4,5,6],
         [7,8,9]]
print(snail(array)) #=> [1,2,3,6,9,8,7,4,5]


array = [[1,2,3],
         [8,9,4],
         [7,6,5]]
print(snail(array)) #=> [1,2,3,4,5,6,7,8,9]


array = [[ 1, 2, 3,4],
         [12,13,14,5],
         [11,16,15,6],
         [10, 9, 8,7]]
print(snail(array)) #=> [1,2,3,4,5,6,7,8,9]
