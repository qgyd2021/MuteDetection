## 静音检测

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
git clone https://github.com/qgyd2021/MuteDetection
```
1. 克隆代码
