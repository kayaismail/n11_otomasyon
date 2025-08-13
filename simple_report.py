#!/usr/bin/env python3
"""
Basit HTML test raporu oluşturucu.
Test sonuçlarını basit HTML formatında gösterir.
"""

import json
import os
from datetime import datetime
import pickle

class SimpleReporter:
    def __init__(self, results_file="reports/test_results.pkl"):
        self.results_file = results_file
        self.test_results = []
        self.load_existing_results()
        
    def load_existing_results(self):
        """Önceki test sonuçlarını yükle."""
        try:
            if os.path.exists(self.results_file):
                with open(self.results_file, 'rb') as f:
                    self.test_results = pickle.load(f)
                print(f"📂 Loaded {len(self.test_results)} existing test results")
            else:
                print("🆕 Starting with empty test results")
        except Exception as e:
            print(f"⚠️ Could not load existing results: {e}")
            self.test_results = []
    
    def save_results(self):
        """Test sonuçlarını dosyaya kaydet."""
        try:
            os.makedirs(os.path.dirname(self.results_file), exist_ok=True)
            with open(self.results_file, 'wb') as f:
                pickle.dump(self.test_results, f)
        except Exception as e:
            print(f"⚠️ Could not save results: {e}")
    
    def clear_results(self):
        """Tüm test sonuçlarını temizle."""
        self.test_results = []
        try:
            if os.path.exists(self.results_file):
                os.remove(self.results_file)
            print("🗑️ All test results cleared")
        except Exception as e:
            print(f"⚠️ Could not clear results: {e}")
        
    def add_result(self, test_name, status, duration=0, error_msg="", logs=""):
        """Test sonucu ekle."""
        # Aynı test varsa güncelle, yoksa ekle
        existing_index = None
        for i, result in enumerate(self.test_results):
            if result['name'] == test_name:
                existing_index = i
                break
        
        new_result = {
            'name': test_name,
            'status': status,  # 'PASS' or 'FAIL'
            'duration': duration,
            'error': error_msg,
            'logs': logs,  # Detaylı log bilgileri
            'timestamp': datetime.now().strftime('%H:%M:%S'),
            'date': datetime.now().strftime('%Y-%m-%d')
        }
        
        if existing_index is not None:
            # Aynı test varsa güncelle
            self.test_results[existing_index] = new_result
            print(f"🔄 Updated test result: {test_name}")
        else:
            # Yeni test ekle
            self.test_results.append(new_result)
            print(f"➕ Added new test result: {test_name}")
        
        # Sonuçları kaydet
        self.save_results()
    
    def generate_html(self, output_path="reports/simple_report.html"):
        """Basit HTML rapor oluştur."""
        
        # Test istatistikleri
        total_tests = len(self.test_results)
        passed_tests = len([r for r in self.test_results if r['status'] == 'PASS'])
        failed_tests = total_tests - passed_tests
        
        html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>🛒 N11 Test Raporu</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 0;
        }}
        
        .container {{
            max-width: 1000px;
            margin: 0 auto;
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }}
        
        h1 {{
            text-align: center;
            color: #333;
            margin-bottom: 30px;
            font-size: 2.5em;
        }}
        
        .summary {{
            display: flex;
            justify-content: space-around;
            margin: 30px 0;
            gap: 20px;
        }}
        
        .summary-card {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            flex: 1;
            border-top: 4px solid;
        }}
        
        .total {{ border-top-color: #007bff; }}
        .passed {{ border-top-color: #28a745; }}
        .failed {{ border-top-color: #dc3545; }}
        
        .summary-card h3 {{
            margin: 0 0 10px 0;
            color: #666;
        }}
        
        .summary-card .number {{
            font-size: 2.5em;
            font-weight: bold;
            margin: 0;
        }}
        
        .total .number {{ color: #007bff; }}
        .passed .number {{ color: #28a745; }}
        .failed .number {{ color: #dc3545; }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 30px 0;
            background: white;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }}
        
        th {{
            background: linear-gradient(45deg, #4CAF50, #45a049);
            color: white;
            padding: 15px;
            text-align: left;
            font-weight: 600;
        }}
        
        td {{
            padding: 12px 15px;
            border-bottom: 1px solid #eee;
        }}
        
        tr:hover {{
            background-color: #f5f5f5;
        }}
        
        .status-pass {{
            background: #d4edda;
            color: #155724;
            padding: 5px 10px;
            border-radius: 15px;
            font-weight: bold;
        }}
        
        .status-fail {{
            background: #f8d7da;
            color: #721c24;
            padding: 5px 10px;
            border-radius: 15px;
            font-weight: bold;
        }}
        
        .error {{
            color: #dc3545;
            font-size: 0.9em;
            max-width: 300px;
            word-break: break-word;
        }}
        
        .logs-section {{
            margin-top: 10px;
        }}
        
        .logs-toggle {{
            background: #007bff;
            color: white;
            border: none;
            padding: 5px 12px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 0.85em;
            margin-right: 5px;
        }}
        
        .logs-toggle:hover {{
            background: #0056b3;
        }}
        
        .logs-content {{
            display: none;
            margin-top: 10px;
            background: #2d3748;
            color: #e2e8f0;
            padding: 15px;
            border-radius: 8px;
            font-family: 'Courier New', monospace;
            font-size: 0.85em;
            line-height: 1.4;
            max-height: 400px;
            overflow-y: auto;
            white-space: pre-wrap;
            word-wrap: break-word;
        }}
        
        .logs-content.show {{
            display: block;
        }}
        
        .step-log {{
            color: #81c784;
            font-weight: bold;
        }}
        
        .success-log {{
            color: #66bb6a;
        }}
        
        .info-log {{
            color: #90caf9;
        }}
        
        .error-log {{
            color: #ef5350;
            font-weight: bold;
        }}
        
        .footer {{
            text-align: center;
            margin-top: 30px;
            color: #666;
            border-top: 1px solid #eee;
            padding-top: 20px;
        }}
        
        .timestamp {{
            text-align: center;
            color: #666;
            margin-bottom: 20px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🛒 N11 Test Raporu</h1>
        
        <div class="timestamp">
            📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        </div>
        
        <div class="summary">
            <div class="summary-card total">
                <h3>Toplam Test</h3>
                <div class="number">{total_tests}</div>
            </div>
            <div class="summary-card passed">
                <h3>✅ Başarılı</h3>
                <div class="number">{passed_tests}</div>
            </div>
            <div class="summary-card failed">
                <h3>❌ Başarısız</h3>
                <div class="number">{failed_tests}</div>
            </div>
        </div>
        
        <table>
            <thead>
                <tr>
                    <th>Test Adı</th>
                    <th>Durum</th>
                    <th>Süre</th>
                    <th>Tarih</th>
                    <th>Saat</th>
                    <th>Detaylar</th>
                </tr>
            </thead>
            <tbody>
"""
        
        # Test sonuçlarını ekle
        for i, result in enumerate(self.test_results):
            status_class = "status-pass" if result['status'] == 'PASS' else "status-fail"
            status_text = "✅ PASS" if result['status'] == 'PASS' else "❌ FAIL"
            error_text = result['error'][:50] + "..." if len(result['error']) > 50 else result['error']
            
            # Log içeriğini formatla
            logs_content = result.get('logs', '')
            if logs_content:
                formatted_logs = logs_content.replace('\n', '<br>')
            else:
                formatted_logs = "Log bilgisi bulunamadı."
            
            test_date = result.get('date', datetime.now().strftime('%Y-%m-%d'))
            
            html_content += f"""
                <tr>
                    <td><strong>{result['name']}</strong></td>
                    <td><span class="{status_class}">{status_text}</span></td>
                    <td>{result['duration']:.2f}s</td>
                    <td>{test_date}</td>
                    <td>{result['timestamp']}</td>
                    <td>
                        {f'<div class="error">{error_text}</div>' if error_text else ""}
                        <div class="logs-section">
                            <button class="logs-toggle" onclick="toggleLogs('logs-{i}')">
                                📋 Detaylı Loglar
                            </button>
                            <div id="logs-{i}" class="logs-content">
                                {formatted_logs}
                            </div>
                        </div>
                    </td>
                </tr>
            """
        
        html_content += """
            </tbody>
        </table>
        
        <div class="footer">
            <p>🚀 N11 Automation Framework</p>
            <p>Powered by Python + Selenium</p>
        </div>
    </div>
    
    <script>
        function toggleLogs(logsId) {{
            var logsDiv = document.getElementById(logsId);
            var button = logsDiv.previousElementSibling;
            
            if (logsDiv.classList.contains('show')) {{
                logsDiv.classList.remove('show');
                button.innerHTML = '📋 Detaylı Loglar';
            }} else {{
                logsDiv.classList.add('show');
                button.innerHTML = '📋 Logları Gizle';
            }}
        }}
        
        // Automatically color log lines
        document.addEventListener('DOMContentLoaded', function() {{
            var logContents = document.querySelectorAll('.logs-content');
            logContents.forEach(function(logDiv) {{
                var content = logDiv.innerHTML;
                
                // Color different types of log lines
                content = content.replace(/(STEP \d+:|📱|📋|🏷️|📊|📈|🔍|🚚|📦)/g, '<span class="step-log">$1</span>');
                content = content.replace(/(✅ SUCCESS|✅ ALL|✅ Product)/g, '<span class="success-log">$1</span>');
                content = content.replace(/(INFO.*?-)/g, '<span class="info-log">$1</span>');
                content = content.replace(/(ERROR|FAIL|❌)/g, '<span class="error-log">$1</span>');
                
                logDiv.innerHTML = content;
            }});
        }});
    </script>
</body>
</html>"""
        
        # HTML dosyasını kaydet
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✅ Basit HTML raporu oluşturuldu: {output_path}")
        return output_path

# Demo kullanım
def create_demo():
    """Demo rapor oluştur."""
    reporter = SimpleReporter()
    
    # Örnek test sonuçları
    reporter.add_result("test_search_and_add_to_cart", "PASS", 8.45, "", "Demo log for search test...")
    reporter.add_result("test_phone_search_filter", "PASS", 11.02, "", "Demo log for phone test...")
    reporter.add_result("test_filter_and_click_random_store", "FAIL", 17.21, "StaleElementReferenceException: stale element not found", "Demo error log...")
    reporter.add_result("test_home_page_load", "PASS", 3.12, "", "Demo home page log...")
    reporter.add_result("test_stores_navigation", "PASS", 5.67, "", "Demo stores log...")
    
    return reporter.generate_html()

def clear_all_results():
    """Tüm test sonuçlarını temizle."""
    reporter = SimpleReporter()
    reporter.clear_results()
    return reporter.generate_html()

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "clear":
        clear_all_results()
        print("🗑️ All results cleared and report regenerated")
    else:
        create_demo()
