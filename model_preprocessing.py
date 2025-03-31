"""
this file is used to preprocess the model.
"""

def model_usage_memory_prediction(model_params_num:int, dtype:str) -> float:
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

def model_selection(model_name:str) -> dict:
    """
    this function is used to get the model params-num based on the model name.
    """
    model_dict = {
        "llama-3-8B": {
            "model_path": "xxxxx",
            "tokenizer_path": "xxxxx",
            "config_path": "xxxxx",
            "params_num": 8.3e9,
            "unsplitted_dim": 128
        }
    }
    return model_dict[model_name]