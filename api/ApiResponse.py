
from flask import jsonify

class ApiResponse:
    def __init__(self, data=None, message=None, status=200):
        self.data = data
        self.message = message
        self.status = status

    def to_dict(self):
        return {
            'data': self.data,
            'message': self.message,
            'status': self.status
        }

    @staticmethod
    def success(data=None):
        return ApiResponse(data=data, message='Success', status=200).to_json()
    
    @staticmethod
    def serverError(message='Internal Server Error'):
        return ApiResponse(data=None, message=message, status=500).to_json()

    @staticmethod
    def customResponse(data=None, message=None, status=200):
        return ApiResponse(data=data, message=message, status=status).to_json()

    def to_json(self):
        return jsonify(self.to_dict()), self.status