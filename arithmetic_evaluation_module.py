"""
This arithmetic module is used to obtain the arithmetic power of each hardware device
Usage: Each hardware device runs the demo to get the result before the algorithm starts.
"""
# 思路1：执行一次模型推理，其倒数作为算力标识
import time
from llama_cpp import Llama

def benchmark_llama(model_path, prompt, max_tokens=128, n_gpu_layers=0):
    # 初始化模型（强制使用CPU）
    llm = Llama(
        model_path=model_path,
        n_ctx=2048,
        n_threads=4,
        verbose=False
    )
    
    # 预热运行
    llm.create_chat_completion([{"role": "user", "content": "1+1="}])
    
    # 正式测试
    start_time = time.perf_counter()
    output = llm.create_chat_completion(
        [{"role": "user", "content": prompt}],
        max_tokens=max_tokens
    )
    elapsed = time.perf_counter() - start_time
    
    # 关键指标
    tokens_generated = len(output['choices'][0]['message']['content'].split())
    return {
        "time_total": elapsed,
        "tokens_per_sec": tokens_generated / elapsed
    }

"""
root@f00266bf6e59:/app/scripts# python3 aem.py
{'time_total': 12.673236443000178, 'tokens_per_sec': 4.813292979607604} 
Use the inverse of token_per_sec as its arithmetic identifier
"""

def get_compute_power(node:str) -> float:
    """
    Get the arithmetic of the corresponding node and return
    """
    pass