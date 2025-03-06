# LLM-Auto-Deployment

This code is the algorithmic part of the task automation deployment. The base part is based on another repository “https://github.com/fromthefox/Distributed-Llama-Py” which performs distributed reasoning for llama.

Task automation deployment considers the hardware information of the nodes in the network topology including:
1. computing power
2. bandwidth
3. memory

Where memory determines whether that task allocation is directly allowable on that node, and arithmetic power and bandwidth determine the overall end-to-end latency of the inference.

The purpose of this algorithm is to minimize the overall end-to-end delay of inference.


本代码是任务自动化部署的算法部分。基础部分基于另一个仓库 “https://github.com/fromthefox/Distributed-Llama-Py” 执行llama的分布式推理。

任务自动化部署考虑网络拓扑中的节点的硬件信息包括：
1. 算力
2. 带宽
3. 内存

其中内存决定该任务分配在该节点上能否直接允许，算力和带宽决定推理整体的端到端延迟。

本算法目的是为了尽量缩小推理的整体端到端延迟。