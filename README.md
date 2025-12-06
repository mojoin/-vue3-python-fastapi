# 地表沉降监测分析系统

这是一个专业的地表沉降变形监测分析平台，支持全站仪和水准仪数据的智能分析。

## 功能特点

- 📊 支持全站仪(XYZ三维)和水准仪(Z一维)数据格式
- 📈 自动生成沉降、水平位移、坡度、曲率等关键指标
- 📋 一键生成专业监测报告(DOCX格式)
- 🎨 学术风格图表导出功能
- 📱 响应式设计，支持移动端访问

## 部署说明

### 本地运行
```bash
pip install -r requirements.txt
python main.py
```

### 在线访问
部署后可通过提供的URL直接访问使用。
https://vue3-python-fastapi.onrender.com/
> 注：该网站部署于render免费web服务，网页15分钟内未有人访问将进入休眠，休眠状态再次访问会将重启服务器界面展示如下。此情况只需耐心重启即可，中国区域白天约1分钟内重启成攻，晚上约3-4分钟
<img width="1912" height="948" alt="61539845595189312dc207deebaba426" src="https://github.com/user-attachments/assets/fb79e90a-7bd8-406d-8f51-96c551f2210f" />

## 使用说明

1. 上传CSV格式的监测数据文件
2. 系统自动分析并生成可视化图表
3. 查看关键变形指标
4. 下载专业监测报告
<img width="1912" height="948" alt="image" src="https://github.com/user-attachments/assets/cc5fbcf1-27b0-423c-8e7b-b420368a6775" />


## 数据格式

支持两种数据格式：
- 全站仪格式：包含X、Y、Z坐标数据
- 水准仪格式：包含Z方向沉降数据
- 可以导出学术论文风格图片
<img width="2952" height="1752" alt="学术图表_累计沉降_2025-12-05" src="https://github.com/user-attachments/assets/95089be2-ed63-4181-8e71-d3f299edbc21" />


详细格式请参考项目中的示例文件。
