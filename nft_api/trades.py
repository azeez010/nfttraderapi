from flask import request, jsonify
from nft_api.jwt_auth import token_required, admin_token_required
from nft_api import app, db, models
from nft_api.validate import validate_trades

@app.route("/api/trades/", methods=["POST"])
@token_required
def add_trades(current_user):
    try:
        trades = request.json
        if not trades:
            return {
                "message": "Invalid data, you need to give the trades name, image and address",
                "data": None,
                "error": "Bad Request"
            }, 400
        # if not request.files["cover_image"]:
        #     return {
        #         "message": "cover image is required",
        #         "data": None
        #     }, 400

        # trades["image"] = "" #request.host_url+"static/trades/"+save_pic(request.files["cover_image"])
        trades["owner"] = current_user["id"]
        trades = models.Trades().create(**trades)
        if not trades:
            return {
                "message": "The trades has been created by user",
                "data": None,
                "error": "Conflict"
            }, 400
        return jsonify({
            "message": "successfully created a new trades",
            "data": trades
        }), 201
    except Exception as e:
        return jsonify({
            "message": "failed to create a new trades",
            "error": str(e),
            "data": None
        }), 500

@app.route("/api/admin/trades", methods=["GET"])
@admin_token_required
def admin_get_tradess(current_user):
    try:
        trades = models.Trades().get_all()
        return jsonify({
            "message": "successfully retrieved all trades",
            "data": trades
        })
    except Exception as e:
        return jsonify({
            "message": "failed to retrieve all trades",
            "error": str(e),
            "data": None
        }), 500


@app.route("/api/trades", methods=["GET"])
@admin_token_required
def get_tradess(current_user):
    try:
        trades = models.Trades().user_get_all(current_user["id"])
        return jsonify({
            "message": "successfully retrieved all trades",
            "data": trades
        })
    except Exception as e:
        return jsonify({
            "message": "failed to retrieve all trades",
            "error": str(e),
            "data": None
        }), 500

@app.route("/api/trades/<trades_id>", methods=["GET"])
@token_required
def get_trades(current_user, trades_id):
    try:
        trades = models.Trades().get_by_id(trades_id)
        if not trades:
            return {
                "message": "trades not found",
                "data": None,
                "error": "Not Found"
            }, 404
        return jsonify({
            "message": "successfully retrieved a trades",
            "data": trades
        })
    except Exception as e:
        return jsonify({
            "message": "Something went wrong",
            "error": str(e),
            "data": None
        }), 500

@app.route("/api/trades/<trades_id>", methods=["PUT"])
@token_required
def update_trades(current_user, trades_id):
    try:
        trades = models.Trades().get_by_id(trades_id)
        if not trades or trades["owner"] != current_user["id"]:
            return {
                "message": "trades not found for user",
                "data": None,
                "error": "Not found"
            }, 404
        
        trades = request.json
        is_validated = validate_trades(**trades)
        if is_validated is not True:
            return {
                "message": "Invalid data",
                "data": None,
                "error": is_validated
            }, 400
        
        trades = models.Trades().update_one(trades_id, **trades)
        return jsonify({
            "message": "successfully updated a trades",
            "data": trades
        }), 201
    
    except Exception as e:
        return jsonify({
            "message": "failed to update a trades",
            "error": str(e),
            "data": None
        }), 400

@app.route("/trades/<trades_id>", methods=["DELETE"])
@token_required
def delete_trades(current_user, trades_id):
    try:
        trades = trades().get_by_id(trades_id)
        if not trades or trades["user_id"] != current_user["_id"]:
            return {
                "message": "trades not found for user",
                "data": None,
                "error": "Not found"
            }, 404
        trades().delete(trades_id)
        return jsonify({
            "message": "successfully deleted a trades",
            "data": None
        }), 204
    except Exception as e:
        return jsonify({
            "message": "failed to delete a trades",
            "error": str(e),
            "data": None
        }), 400