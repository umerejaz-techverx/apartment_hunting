import csv

def add_step(prev, current, reverse=False):
    if reverse:
        if current is not None:
            return min(prev + 1, current)
        return prev + 1
    if isinstance(current, bool):
        if current:
            return 0
    if prev is not None:
        return prev + 1
    return None


def generate_dict(req):
    tmp = dict()
    for i in req:
        tmp[i] = None
    return tmp


def calculate_distance(blocks, req, reverse=False):
    result = []
    prev_values = generate_dict(req)
    if reverse:
        blocks = blocks[::-1]
        prev_values = blocks.pop(0)
        result.append(prev_values.copy())
    for i in blocks:
        sample = generate_dict(req)
        for s_req in req:
            sample[s_req] = add_step(prev_values[s_req], i[s_req], reverse)
            prev_values[s_req] = sample[s_req]
        result.append(sample)
    if reverse:
        result = result[::-1]
    return result


def is_possible(data, req):
    tmp = generate_dict(req)
    for i in data:
        for s_req in req:
            if not tmp[s_req]:
                tmp[s_req] = i.get(s_req)
    if all(tmp.values()):
        return True
    return False


def get_apartment(blocks, req):
    if is_possible(blocks, req):
        result = calculate_distance(blocks, req)
        result_rev = calculate_distance(result, req, reverse=True)
        minimum_distance = None
        minimum_distance_index = None
        for index, i in enumerate(result_rev):
            current_distance = max(i.values())
            if minimum_distance is None:
                minimum_distance = current_distance
                minimum_distance_index = index
                continue
            elif minimum_distance > current_distance:
                minimum_distance = current_distance
                minimum_distance_index = index
        return minimum_distance_index
    else:
        return "All facilities are not avilable in the provided blocks"


def read_appartment_haunting_csv(file_path):
    # Open the CSV file in read mode
    with open(file_path, 'r') as file:

        # Create a CSV reader object
        reader = csv.reader(file)

        # Convert the reader object to a list
        data = list(reader)

    blocks = []
    req = []
    for index, block in enumerate(data[0]):
        if block != 'req':
            blocks.append(eval(data[1][index]))
        else:
            req = eval(data[1][index])

    return blocks, req


if __name__ == '__main__':

    file_path = 'input.csv'
    blocks, req = read_appartment_haunting_csv(file_path)
    print(get_apartment(blocks, req))
