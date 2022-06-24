import json

def write_splineit_json(path, data, attributes):
    print(f"{path=}")
    print(f"{data=}")
    print(f"{attributes=}")


    def array2list(arr):
        return [[coord[0],coord[1]] for coord in arr]

    # marshal the data
    json_data = [array2list(arr) for arr in data]

    # marshal the interpolator
    interpolator = attributes['metadata']['interpolator']
    name = type(interpolator).name
    args = interpolator.marshal()

    json_dict = {
        "data": json_data,
        "method":{
            "name" : name,
            "args" : args
        }
    }

    with open(path, 'w') as f:
        json.dump(json_dict,f, indent=4)

    return path