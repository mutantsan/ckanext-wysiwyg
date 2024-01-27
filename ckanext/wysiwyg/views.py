import logging

import json

from flask import Blueprint, Response, jsonify
from flask.views import MethodView

import ckan.plugins.toolkit as tk


log = logging.getLogger(__name__)
wysiwyg = Blueprint("wysiwyg", __name__)


class Ckeditor5FileUpload(MethodView):
    def post(self) -> Response:
        file = tk.request.files.get("upload")

        if not file:
            return jsonify({"error": {"message": "Missing file object"}})

        try:
            result = tk.get_action("files_file_create")(
                {"ignore_auth": True},
                {
                    "name": file.filename,
                    "upload": file,
                },
            )
        except (tk.ValidationError, OSError) as e:
            tk.ValidationError(str(e))
            return jsonify({"error": {"message": str(e.error_summary)}})

        return jsonify({"url": result["url"]})


wysiwyg.add_url_rule(
    "/ckeditor/upload_file", view_func=Ckeditor5FileUpload.as_view("upload_file")
)
