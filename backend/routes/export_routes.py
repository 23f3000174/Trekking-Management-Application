import os
from flask import Blueprint, send_from_directory
from flask_restful import Api, Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.models import User
from celery_app import export_csv

export_bp = Blueprint('export', __name__, url_prefix='/api/exports')
api = Api(export_bp)

class TriggerExport(Resource):
    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user:
            return {'message': 'User not found'}, 404

        task = export_csv.delay(user.id, user.email)
        return {
            'message': 'Export job triggered successfully. You will receive an email once it is complete.',
            'task_id': task.id
        }, 202

class DownloadExport(Resource):
    def get(self, filename):
        if ".." in filename or filename.startswith("/"):
            return {'message': 'Invalid filename'}, 400

        exports_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "exports")
        if not os.path.exists(os.path.join(exports_dir, filename)):
            return {'message': 'File not found'}, 404

        return send_from_directory(exports_dir, filename, as_attachment=True)

api.add_resource(TriggerExport, '/trigger')
api.add_resource(DownloadExport, '/download/<string:filename>')
