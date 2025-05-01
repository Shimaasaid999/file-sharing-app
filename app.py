import os
from flask import Flask, request, jsonify, send_from_directory
import boto3
from werkzeug.utils import secure_filename

from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

# إعدادات AWS S3
AWS_ACCESS_KEY = 'AKIAZALAU5PAGNDO6KBH'
AWS_SECRET_KEY = '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'
AWS_BUCKET_NAME = 'files-uplode'
AWS_REGION = 'us-east-1'

# إعدادات الملف المسموح به
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'txt'}

# التحقق من امتداد الملفات
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# إعداد S3 client
s3_client = boto3.client('s3', 
                         aws_access_key_id=AWS_ACCESS_KEY, 
                         aws_secret_access_key=AWS_SECRET_KEY, 
                         region_name=AWS_REGION)

# مسار رفع الملفات
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"message": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"message": "No selected file"}), 400
    if file and allowed_file(file.filename):
        # حفظ الملف في S3
        filename = secure_filename(file.filename)
        try:
            s3_client.upload_fileobj(file, AWS_BUCKET_NAME, filename)
            file_url = f"https://{AWS_BUCKET_NAME}.s3.{AWS_REGION}.amazonaws.com/{filename}"
            return jsonify({"message": "File uploaded successfully", "url": file_url}), 200
        except Exception as e:
            return jsonify({"message": "Upload failed", "error": str(e)}), 500
    else:
        return jsonify({"message": "Invalid file type"}), 400


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
    
    
    
