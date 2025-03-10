from flask import Blueprint, jsonify, request
from .tmdb import search_tv_shows
from .watch_history import add_episode_progress, get_progress_for_show, delete_progress_for_show, get_all_progress

bp = Blueprint('api', __name__)

@bp.route('/search')
def search():
    query = request.args.get('query', '')
    if not query:
        return jsonify({'error': 'Missing Query'}), 400
    
    data = search_tv_shows(query)
    return jsonify(data)

# Add progress (POST)
@bp.route("/progress", methods=["POST"])
def save_show_progress():
    data = request.get_json()

    show_id = data.get("show_id")
    name = data.get("name")
    season = data.get("season")
    episode = data.get("episode")

    if not all([show_id, name, season, episode]):
        return jsonify({"error": "Missing one or more required fields: show_id, name, season, episode"}), 400

    try:
        add_episode_progress(show_id, name, season, episode)
        return jsonify({
            "message": "Progress saved",
            "show_id": show_id,
            "name": name,
            "season": season,
            "episode": episode
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Get most recent progress for a show
@bp.route("/progress/<int:show_id>", methods=["GET"])
def fetch_progress(show_id):
    progress = get_progress_for_show(show_id)
    if not progress:
        return jsonify({"error": "No progress found for this show."}), 404
    return jsonify(progress)

# Get all progress
@bp.route("/progress", methods=["GET"])
def list_all_progress():
    return jsonify(get_all_progress())

# Delete progress for a show
@bp.route("/progress/<int:show_id>", methods=["DELETE"])
def delete_progress(show_id):
    try:
        delete_progress_for_show(show_id)
        return jsonify({"message": f"Progress for show {show_id} deleted."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500