import sys
print(sys.path)

from common.my_logger import my_logger


@my_logger
def extract_max_value(list_num : list[int]) -> int:
    return max(list_num)

extract_max_value([1,4,7,2,6])
