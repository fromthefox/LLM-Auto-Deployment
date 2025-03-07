"""
bandwidth可以：
1. 默认Klonet的拓扑搭建获得带宽
2. 手动使用iperf3方法获得带宽
3. 以下脚本（未测试）
"""

import paramiko
import re
import getpass
from typing import Tuple

def measure_bandwidth(ip_a: str, ip_b: str, 
                      username: str = "ubuntu",
                      password: str = None) -> Tuple[float, float]:
    """
    测量两台设备间的双向最大带宽（单位：Mbps）
    
    参数:
        ip_a: 设备A的IP地址
        ip_b: 设备B的IP地址
        username: SSH用户名（默认ubuntu）
        password: SSH密码（如果未提供会提示输入）
        
    返回:
        (a_to_b_bandwidth, b_to_a_bandwidth) 双向带宽元组
    """
    
    def run_ssh_command(ip: str, command: str) -> str:
        """执行SSH命令并返回输出"""
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        # 安全密码处理
        pw = password or getpass.getpass(f"请输入 {ip} 的SSH密码: ")
        
        try:
            client.connect(ip, username=username, password=pw, timeout=10)
            _, stdout, _ = client.exec_command(command)
            output = stdout.read().decode()
            return output
        except paramiko.AuthenticationException:
            raise ValueError(f"认证失败，请检查 {ip} 的用户名/密码")
        finally:
            client.close()

    def parse_iperf(output: str) -> float:
        """解析iperf3输出获取带宽"""
        match = re.search(r'(\d+\.\d+) Mbits/sec\s+sender', output)
        return float(match.group(1)) if match else 0.0

    # 测试A到B方向
    run_ssh_command(ip_b, "iperf3 -s -D")  # 启动服务端
    a_to_b = run_ssh_command(ip_a, f"iperf3 -c {ip_b} -t 5")  # 5秒测试
    run_ssh_command(ip_b, "pkill iperf3")  # 清理服务端

    # 测试B到A方向  
    run_ssh_command(ip_a, "iperf3 -s -D")
    b_to_a = run_ssh_command(ip_b, f"iperf3 -c {ip_a} -t 5")
    run_ssh_command(ip_a, "pkill iperf3")

    return parse_iperf(a_to_b), parse_iperf(b_to_a)

# 使用示例（两种方式）：
if __name__ == "__main__":
    # 方式1：运行时输入密码
    bw1, bw2 = measure_bandwidth("192.168.1.101", "192.168.1.102")
    
    # 方式2：代码中传递密码（不建议，因有安全风险）
    # bw1, bw2 = measure_bandwidth("192.168.1.101", "192.168.1.102", password="your_password")
    
    print(f"A->B带宽: {bw1:.2f} Mbps")
    print(f"B->A带宽: {bw2:.2f} Mbps")
