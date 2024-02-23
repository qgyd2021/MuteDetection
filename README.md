## 静音检测


### 从 Dockerfile 构建

```text
mkdir -p /data/tianxing/PycharmProjects
cd /data/tianxing/PycharmProjects
git clone https://github.com/qgyd2021/MuteDetection.git
```
1.克隆代码

```text
docker build -t mute_detection:v20240223_0953 .
```
1.创建镜像

```text
docker run -itd \
--name MuteDetection \
-p 30090:30090 \
mute_detection:v20240223_0953 \
/bin/bash
```
1.启动容器

### 从 Docker 容器启动

```shell
docker run -itd \
--name MuteDetection \
-p 30090:30090 \
python:3.8 \
/bin/bash
```
1. 创建容器

```text
mkdir -p /data/tianxing/PycharmProjects
cd /data/tianxing/PycharmProjects
git clone https://github.com/qgyd2021/MuteDetection.git
```
1. 克隆代码



```text
Running 10s test @ http://127.0.0.1:30090/voice/event/on_pcm
  1 threads and 1 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency     9.03ms  199.10us  12.19ms   80.15%
    Req/Sec   110.50      3.45   121.00     89.00%
  Latency Distribution
     50%    9.04ms
     75%    9.10ms
     90%    9.19ms
     99%    9.53ms
  1103 requests in 10.02s, 316.68KB read
Requests/sec:    110.09
Transfer/sec:     31.61KB


Running 10s test @ http://127.0.0.1:30090/voice/event/on_pcm
  10 threads and 10 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency    86.98ms    4.68ms 125.92ms   95.28%
    Req/Sec    11.45      3.56    20.00     85.06%
  Latency Distribution
     50%   87.29ms
     75%   88.24ms
     90%   88.96ms
     99%  101.40ms
  1145 requests in 10.02s, 328.74KB read
Requests/sec:    114.28
Transfer/sec:     32.81KB


Running 10s test @ http://127.0.0.1:30090/voice/event/on_pcm
  50 threads and 50 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency   428.08ms   49.56ms 486.09ms   96.25%
    Req/Sec     2.00      1.10    20.00     98.43%
  Latency Distribution
     50%  435.97ms
     75%  439.55ms
     90%  443.14ms
     99%  446.92ms
  1146 requests in 10.10s, 329.03KB read
Requests/sec:    113.47
Transfer/sec:     32.58KB


Running 10s test @ http://127.0.0.1:30090/voice/event/on_pcm
  100 threads and 100 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency   840.06ms  150.14ms   1.06s    91.23%
    Req/Sec     1.16      1.19    20.00     97.30%
  Latency Distribution
     50%  877.49ms
     75%  881.89ms
     90%  898.77ms
     99%  970.21ms
  1151 requests in 10.10s, 330.46KB read
Requests/sec:    113.95
Transfer/sec:     32.72KB


```