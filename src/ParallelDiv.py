
def parallel_divide(resistances: list[float]):
    res_sum = 0
    for resistance in resistances:
        res_sum += (1/resistance)
    return 1/res_sum