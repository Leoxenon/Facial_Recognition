from flask import Flask, request, jsonify
from flask_cors import CORS
from routes import auth, user
from services import rekognition_service, s3_service, dynamodb_service, auth_service
import io
from dotenv import load_dotenv
from flask_restx import Api, Resource, fields
import base64

load_dotenv()
load_dotenv()

app = Flask(__name__)
CORS(app)  # 允许所有来源的请求

# 注册路由
app.register_blueprint(auth.bp)
app.register_blueprint(user.bp)

s3_service = s3_service.S3Service()
db_service = dynamodb_service.DynamoDBService()

api = Api(app, version='1.0', title='Facial Auth API',
    description='A facial recognition authentication API'
)

auth_ns = api.namespace('auth', description='Authentication operations')

login_model = api.model('Login', {
    'username': fields.String(required=True),
    'password': fields.String(required=True),
    'faceImage': fields.String(required=True)
})

def handle_file_upload(request_files, field_name):
    if field_name not in request_files:
        return None, ({"error": f"No {field_name} part"}, 400)
    
    file = request_files[field_name]
    if file.filename == '':
        return None, ({"error": "No selected file"}, 400)
        
    return file, None

@app.route("/detect_faces/", methods=['POST'])
@handle_errors
def detect_faces():
    try:
        data = request.get_json()
        if not data or 'image' not in data:
            return jsonify({"error": "No image data provided"}), 400
            
        # 解析 base64 图像数据
        try:
            image_data = base64.b64decode(data['image'].split(',')[1])
        except Exception as e:
            return jsonify({"error": f"Invalid image format: {str(e)}"}), 400

        # 检测人脸
        try:
            faces = rekognition_service.detect_faces(image_data)
            return jsonify({
                "faces_detected": len(faces),
                "details": faces
            })
        except Exception as e:
            return jsonify({"error": f"Face detection failed: {str(e)}"}), 500
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/compare_faces/", methods=['POST'])
def compare_faces():
    if 'source' not in request.files or 'target' not in request.files:
        return jsonify({"error": "Missing source or target file"}), 400
    source = request.files['source']
    target = request.files['target']
    if source.filename == '' or target.filename == '':
        return jsonify({"error": "No selected file"}), 400
    if source and target:
        try:
            source_image = source.read()
            target_image = target.read()
            matches = rekognition_service.compare_faces(source_image, target_image)
            return jsonify({"matches": len(matches), "details": matches})
        except Exception as e:
            return jsonify({"error": str(e)}), 400

@app.route("/upload_face/", methods=['POST'])
def upload_face():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    if file:
        try:
            contents = file.read()
            file_url = s3_service.upload_file(io.BytesIO(contents), file.filename)
            faces = rekognition_service.detect_faces(contents)

            if len(faces) != 1:
                return jsonify({"error": "Image must contain exactly one face"}), 400

            face_id = rekognition_service.index_face(file_url)

            db_entry = {
                "FaceID": face_id,
                "ImageURL": file_url,
                "Confidence": faces[0]['Confidence']
            }
            db_service.add_entry(db_entry)

            return jsonify({"message": "Face uploaded and indexed successfully", "face_id": face_id})
        except Exception as e:
            return jsonify({"error": str(e)}), 400

# 创建 Rekognition 集合
rekognition_service.create_collection()

# 创建 DynamoDB 表（如果不存在）
db_service.create_table_if_not_exists()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
