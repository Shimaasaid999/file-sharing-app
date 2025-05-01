import os
from flask import Flask, request, jsonify, send_from_directory
import boto3
from werkzeug.utils import secure_filename
from flask import Flask, render_template

app = Flask(__name__)

# إعدادات AWS S3
AWS_BUCKET_NAME = 'files-uplode'
AWS_REGION = 'us-east-1'

# إعدادات الملف المسموح به
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'txt'}

# التحقق من امتداد الملفات
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# إعداد S3 client (باستخدام IAM Role)
s3_client = boto3.client('s3', region_name=AWS_REGION)

# مسار الصفحة الرئيسية
@app.route('/')
def index():
    return render_template('index.html')

# مسار رفع الملفات
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"message": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"message": "No selected file"}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        try:
            file.stream.seek(0)  # Reset the file pointer
            s3_client.put_object(Body=file.stream, Bucket=AWS_BUCKET_NAME, Key=filename)
            file_url = f"https://{AWS_BUCKET_NAME}.s3.{AWS_REGION}.amazonaws.com/{filename}"
            print(f"File uploaded successfully: {file_url}")  # Debug
            return jsonify({"message": "File uploaded successfully", "url": file_url}), 200
        except Exception as e:
            print(f"Upload error: {str(e)}")  # Debug
            return jsonify({"message": "Upload failed", "error": str(e)}), 500
    else:
        return jsonify({"message": "Invalid file type"}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)

    
    
    
