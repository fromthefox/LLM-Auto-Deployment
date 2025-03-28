"""
this file is used to preprocess the model.
"""

def model_memory_prediction(model_params_num:int, dtype:str) -> float:
    """
    this function is used to predict the usage of the model.
    """
    dtype_dict = {
        "float32": 4,
        "float16": 2,
        "bfloat16": 2,
        "int8": 1
    }
    # Bytes
    return model_params_num * dtype_dict[dtype] / 1024**3
    # GB