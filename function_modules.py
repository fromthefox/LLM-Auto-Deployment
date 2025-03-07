"""
some modules to use
"""


def calculating_memory_estimates(dtype: str, A_shape: tuple, B_shape: tuple) -> int:
    dsize_dict = {
        "fp32": 4,
        "fp16": 2
    }
    dsize = dsize_dict[dtype]
    return (A_shape[0] * A_shape[1] + B_shape[0] * B_shape[1] + A_shape[0] * B_shape[1]) * dsize
