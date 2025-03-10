from flask import Blueprint, jsonify, request
from .tmdb import search_tv_shows
from .models import get_progress, update_progress, load_progress, delete_progress

bp = Blueprint('api', __name__)

@bp.route('/search')
def search():
    query = request.args.get('query', '')
    if not query:
        return jsonify({'error': 'Missing Query'}), 400
    
    data = search_tv_shows(query)
    return jsonify(data)

@bp.route("/progress/<int:show_id>", methods=["GET"])
def fetch_progress(show_id):
    progress = get_progress(show_id)
    if not progress:
        return jsonify({"error": "No progress found for this show."}), 404
    return jsonify(progress)

@bp.route("/progress", methods=["POST"])
def save_show_progress():
    data = request.get_json()

    show_id = data.get("show_id")
    season = data.get("season")
    episode = data.get("episode")

    if not all([show_id, season, episode]):
        return jsonify({"error": "Missing one or more required fields."}), 400

    updated = update_progress(show_id, season, episode)
    return jsonify(updated)

@bp.route("/progress", methods=["GET"])
def get_all_progress():
    return jsonify(load_progress())

@bp.route("/progress/<int:show_id>", methods=["DELETE"])
def delete_show_progress(show_id):
    success = delete_progress(show_id)
    if success:
        return jsonify({"message": f"Progress for show {show_id} deleted."})
    else:
        return jsonify({"error": "No progress found for that show."}), 404