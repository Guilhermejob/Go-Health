from flask import Flask
from flask_migrate import Migrate


def init_app(app: Flask):

    from app.models.client_model import ClientModel
    from app.models.deficiency_model import DeficiencyModel
    from app.models.surgery_model import SurgeryModel
    from app.models.diseases_model import DiseaseModel

    Migrate(app, app.db)
