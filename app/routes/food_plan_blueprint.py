from flask import Blueprint
from app.controllers.food_plan_controllers import create_plan, download_food_plan, get_food_plan_by_client_id


bp_food_plan = Blueprint('bp_food_plan', __name__)

bp_food_plan.post('/create-food-plan/client/<int:client_id>')(create_plan)
bp_food_plan.get('/get-food-plan/client/<int:client_id>')(get_food_plan_by_client_id)
bp_food_plan.get('/download-food-plan/food-plan/<int:food_plan_id>')(download_food_plan)

