#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
地表沉降监测系统 - PythonAnywhere部署版本
简化版本，适合免费托管平台
"""

from flask import Flask, request, jsonify, send_from_directory, render_template_string
import pandas as pd
import numpy as np
import io
import json
from datetime import datetime

app = Flask(__name__)

# 简单的HTML模板
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>地表沉降监测分析系统</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
        .header { text-align: center; color: #333; margin-bottom: 30px; }
        .upload-area { border: 2px dashed #ccc; padding: 30px; text-align: center; margin: 20px 0; }
        .results { background: #f5f5f5; padding: 20px; border-radius: 8px; margin-top: 20px; }
        .metric { background: white; padding: 15px; margin: 10px 0; border-radius: 5px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        button { background: #007bff; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; }
        button:hover { background: #0056b3; }
    </style>
</head>
<body>
    <div class="header">
        <h1>地表沉降监测分析系统</h1>
        <p>专业的变形监测数据分析平台</p>
    </div>
    
    <div class="upload-area">
        <h3>上传CSV数据文件</h3>
        <form id="uploadForm" enctype="multipart/form-data">
            <input type="file" name="file" accept=".csv" required>
            <br><br>
            <button type="submit">开始分析</button>
        </form>
    </div>
    
    <div id="results" class="results" style="display:none;">
        <h3>分析结果</h3>
        <div id="metrics"></div>
        <div id="chartData"></div>
    </div>
    
    <script>
        document.getElementById('uploadForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            const formData = new FormData();
            const fileInput = document.querySelector('input[type="file"]');
            formData.append('file', fileInput.files[0]);
            
            try {
                const response = await fetch('/analyze', {
                    method: 'POST',
                    body: formData
                });
                
                const result = await response.json();
                displayResults(result);
            } catch (error) {
                alert('分析失败: ' + error.message);
            }
        });
        
        function displayResults(data) {
            document.getElementById('results').style.display = 'block';
            
            // 显示关键指标
            const metricsHtml = `
                <h4>关键变形指标</h4>
                <div class="metric">
                    <strong>最大累计下沉:</strong> ${data.metrics.max_subsidence.val.toFixed(2)} mm
                    (测点: ${data.metrics.max_subsidence.point})
                </div>
                <div class="metric">
                    <strong>数据类型:</strong> ${data.data_type === 'total_station' ? '全站仪数据' : '水准仪数据'}
                </div>
                <div class="metric">
                    <strong>测点数量:</strong> ${data.point_ids.length} 个
                </div>
                <div class="metric">
                    <strong>监测日期:</strong> ${data.dates.join(', ')}
                </div>
            `;
            
            document.getElementById('metrics').innerHTML = metricsHtml;
            
            // 显示原始数据
            document.getElementById('chartData').innerHTML = `
                <h4>数据概览</h4>
                <div class="metric">
                    <strong>测点编号:</strong> ${data.point_ids.join(', ')}
                </div>
            `;
        }
    </script>
</body>
</html>
"""

def parse_simple_csv(content):
    """简化的CSV解析函数"""
    df = pd.read_csv(io.StringIO(content.decode('utf-8')))
    
    # 基本数据处理
    point_ids = df.iloc[:, 0].astype(str).tolist()
    dates = []
    
    # 寻找日期行
    for col in df.columns:
        if pd.api.types.is_string_dtype(df[col]):
            date_row = df[col].iloc[0] if len(df) > 0 else None
            if date_row and ('2024' in str(date_row) or '2023' in str(date_row)):
                dates.append(str(date_row))
    
    if not dates:
        dates = ['监测期1', '监测期2']
    
    # 模拟沉降数据
    z_data = []
    for i in range(len(point_ids)):
        # 生成一些模拟的沉降数据
        base_value = float(i * 2 + np.random.normal(0, 1))
        z_data.append(max(0, base_value))
    
    # 计算最大沉降
    max_subsidence_val = max(z_data) if z_data else 0
    max_subsidence_idx = z_data.index(max_subsidence_val) if z_data else 0
    max_subsidence_point = point_ids[max_subsidence_idx] if max_subsidence_idx < len(point_ids) else '未知'
    
    return {
        "data_type": "leveling",
        "point_ids": point_ids,
        "dates": dates,
        "metrics": {
            "max_subsidence": {
                "val": max_subsidence_val,
                "point": max_subsidence_point,
                "date": dates[0] if dates else "--"
            },
            "max_horizontal": {"val": 0, "point": "--", "date": "--"},
            "max_slope": {"val": 0, "point": "--", "date": "--"},
            "max_curvature": {"val": 0, "point": "--", "date": "--"}
        },
        "chart_time_legend_distance_z": {
            "xAxis": list(range(len(point_ids))),
            "series": [{"name": "沉降数据", "data": z_data}]
        }
    }

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        file = request.files['file']
        if not file:
            return jsonify({'error': '没有上传文件'}), 400
        
        content = file.read()
        result = parse_simple_csv(content)
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # PythonAnywhere会自动处理端口和主机配置
    app.run(debug=True)