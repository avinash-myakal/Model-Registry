import uuid
from typing import List

from flask import jsonify
from flask_smorest import Blueprint
from flask.views import MethodView
from werkzeug.exceptions import abort

from tno.mmvib_registry.db.memorydb import ModelNotFoundException
from tno.mmvib_registry.models.modeladapter import ModelAdapter, ModelAdapterSearchArgsSchema
from tno.mmvib_registry.db import db

from tno.shared.log import get_logger

logger = get_logger(__name__)

api = Blueprint("MMvIB Registry", "registry", url_prefix="/registry")


@api.route("/")
class RegistryAPI(MethodView):

    @api.response(200, ModelAdapter.Schema(many=True))
    def get(self):
        """Get the list of Model Adapters currently registered in the registry"""

        response = ModelAdapter.Schema().dump(db.get_all(), many=True)
        return jsonify(response)

    @api.arguments(ModelAdapter.Schema())
    @api.response(201, ModelAdapter.Schema())
    def post(self, data):
        """Register a new model adapter"""
        data.id = str(uuid.uuid4())
        db.add_model(data)
        response = ModelAdapter.Schema().dump(data) # serialize correctly, including enums etc.
        return jsonify(response)


@api.route("/<model_id>")
class UpdateRegistryAPI(MethodView):
    def get(self, model_id):
        """Get the model adapter by its ID from the registry"""
        try:
            item = db.get_by_id(model_id)
            response = ModelAdapter.Schema().dump(item, many=False)
            return jsonify(response)
        except ModelNotFoundException as e:
            abort(404, e.message)

    @api.arguments(ModelAdapter.Schema())
    @api.response(201, ModelAdapter.Schema())
    def put(self, update_data, model_id):
        """Update a model adapter by its ID"""
        try:
            item = db.get_by_id(model_id)
            item.update(update_data)
            response = ModelAdapter.Schema().dump(item, many=False)
            return jsonify(response)
        except ModelNotFoundException as e:
            abort(404, e.message)

    @api.response(204)
    def delete(self, model_id):
        """Delete a model adapter from the repository"""
        try:
            db.delete(model_id)
        except ModelNotFoundException as e:
            abort(404, e.message)

@api.route("/search")
class SearchRegistryAPI(MethodView):
    @api.arguments(ModelAdapterSearchArgsSchema())
    @api.response(200, ModelAdapter.Schema(many=True))
    def post(self, data):
        """Search for a model adapter with specific attributes"""
        print ("search:", data)
        result = db.search(data)
        response = ModelAdapter.Schema().dump(result, many=True)
        return jsonify(response)

