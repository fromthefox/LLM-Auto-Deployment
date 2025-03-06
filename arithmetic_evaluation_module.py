"""
该算力模块用于获取每个硬件设备的算力
使用方法：每个硬件设备在算法开始前运行该Demo得到结果
"""
# 思路1：执行一次模型推理，其倒数作为算力标识
import time
import psutil
from llama_cpp import Llama

def benchmark_llama(model_path, prompt, max_tokens=128, n_gpu_layers=0):
    # 初始化模型（强制使用CPU）
    llm = Llama(
        model_path=model_path,
        n_ctx=2048,
        n_threads=psutil.cpu_count(logical=False),  # 使用物理核心数
        n_gpu_layers=0  # 完全禁用GPU
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
        "tokens_per_sec": tokens_generated / elapsed,
        "mem_rss": psutil.Process().memory_info().rss // 1024**2  # MB
    }
