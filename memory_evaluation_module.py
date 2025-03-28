import psutil
import torch
from typing import Dict, Union

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


def hw_memory_evaluation(safety_margin: float = 0.1) -> Dict[str, Union[float, str]]:
    """
    获取当前设备的可用存储资源信息（优先检测GPU显存）
    
    参数:
        safety_margin (float): 安全保留比例（默认保留10%）
        
    返回:
        dict: 包含以下键值对的结构化信息:
            - 'type' (str): 'gpu'/'cpu'
            - 'total' (float): 总容量（GB）
            - 'used' (float): 已使用量（GB）
            - 'free' (float): 空闲量（GB）
            - 'available' (float): 考虑安全边际后的可用量（GB）
    """
    mem_info = {}
    
    try:
        # 优先检测GPU显存
        if torch.cuda.is_available():
            device = torch.cuda.current_device()
            total = torch.cuda.get_device_properties(device).total_memory
            allocated = torch.cuda.memory_allocated(device)
            reserved = torch.cuda.memory_reserved(device)
            
            mem_info.update({
                'type': 'gpu',
                'total': total / 1024**3,
                'used': allocated / 1024**3,
                'free': (total - reserved) / 1024**3,
                'reserved': reserved / 1024**3
            })
        else:
            raise RuntimeError("No GPU available")
            
    except (RuntimeError, AssertionError):
        # 当GPU不可用时转为检测系统内存
        virtual_mem = psutil.virtual_memory()
        mem_info.update({
            'type': 'cpu',
            'total': virtual_mem.total / 1024**3,
            'used': virtual_mem.used / 1024**3,
            'free': virtual_mem.available / 1024**3
        })
    
    # 计算安全可用量（保留safety_margin比例的空闲内存）
    if mem_info['type'] == 'gpu':
        available = mem_info['free'] * (1 - safety_margin)
    else:
        # 对系统内存采用固定保留策略（至少保留2GB或10%）
        reserve = max(2.0, mem_info['free'] * safety_margin)
        available = mem_info['free'] - reserve
    
    mem_info['available'] = max(0, round(available, 2))
    
    return mem_info
