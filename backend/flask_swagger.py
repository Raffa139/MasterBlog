from flask_swagger_ui import get_swaggerui_blueprint

SWAGGER_URL = "/api/docs"
API_URL = "/static/masterblog_swagger.json"


def setup_swagger(app):
    swagger_ui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            "app_name": "Master Blog API"
        }
    )

    app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)
