"""
This arithmetic module is used to obtain the arithmetic power of each hardware device
Usage: Each hardware device runs the demo to get the result before the algorithm starts.
"""
# Idea 1: Perform model inference once and its reciprocal is used as the arithmetic marker
import time
import torch
# from llama_cpp import Llama
from psutil import cpu_count
import numpy as np

# def benchmark_llama(model_path, prompt, max_tokens=128, n_gpu_layers=0):
#     # 初始化模型（强制使用CPU）
#     llm = Llama(
#         model_path=model_path,
#         n_ctx=2048,
#         n_threads=4,
#         verbose=False
#     )
    
#     # 预热运行
#     llm.create_chat_completion([{"role": "user", "content": "1+1="}])
    
#     # 正式测试
#     start_time = time.perf_counter()
#     output = llm.create_chat_completion(
#         [{"role": "user", "content": prompt}],
#         max_tokens=max_tokens
#     )
#     elapsed = time.perf_counter() - start_time
    
#     # 关键指标
#     tokens_generated = len(output['choices'][0]['message']['content'].split())
#     return {
#         "time_total": elapsed,
#         "tokens_per_sec": tokens_generated / elapsed
#     }

"""
root@f00266bf6e59:/app/scripts# python3 aem.py
{'time_total': 12.673236443000178, 'tokens_per_sec': 4.813292979607604} 
Use the inverse of token_per_sec as its arithmetic identifier
"""

# Idea 2: Design a multidimensional multiplication operation for evaluating the computational power of a hardware device
# in this way we don't need to download the model and run it.
def benchmark_tensor(N=4096, dtype=torch.float32, threads=None):
    """CPU矩阵乘法算力测试"""
    
    # Set the number of threads (all physical cores are used by default)
    if threads is None:
        threads = cpu_count(logical=False)
    torch.set_num_threads(threads)
    
    # Initialise tensor (ensure stable memory allocation)
    A = torch.randn(N, N, dtype=dtype)
    B = torch.randn(N, N, dtype=dtype)
    
    # Warm-up (to avoid cold start bias)
    for _ in range(3):
        C = A @ B
    
    # START
    times = []
    for _ in range(20):
        start = time.perf_counter()
        C = A @ B
        times.append(time.perf_counter() - start)
    
    # GFLOPS
    avg_time = np.mean(times)
    flops = 2 * N**3 / avg_time  # floating point operand
    gflops = flops / 1e9

    arithmetic_info = {
        "Matrix Size": f"{N}x{N}",
        "Threads": threads,
        "Time (s)": f"{avg_time:.3f} ± {np.std(times):.2f}",
        "GFLOPS": round(gflops, 1)
    }
    
    return arithmetic_info
