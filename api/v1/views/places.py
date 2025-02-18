#!/usr/bin/python3
"""
Handles all default RESTful API actions for Place objects.
"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State
from models.place import Place
from models.city import City
from models.user import User


@app_views.route('/cities/<city_id>/places',
                 methods=['GET'], strict_slashes=False)
def get_places_by_city(city_id):
    """Retrieves the list of all Place objects in a City"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    places = [place.to_dict() for place in city.places]
    return jsonify(places)


@app_views.route('/places/<place_id>',
                 methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """Retrieves a specific Place object by ID"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    """Deletes a Place object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places',
                 methods=['POST'], strict_slashes=False)
def create_place(city_id):
    """Creates a new Place object"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 400
    if "user_id" not in data:
        return jsonify({"error": "Missing user_id"}), 400
    user = storage.get(User, data["user_id"])
    if not user:
        abort(404)
    if "name" not in data:
        return jsonify({"error": "Missing name"}), 400

    new_place = Place(city_id=city_id, **data)
    storage.new(new_place)
    storage.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """Updates a Place object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 400

    ignored_keys = ["id", "user_id", "city_id", "created_at", "updated_at"]
    for key, value in data.items():
        if key not in ignored_keys:
            setattr(place, key, value)

    place.save()
    return jsonify(place.to_dict()), 200


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def search_places():
    """
    Retrieves Place objects based on JSON filters (states, cities, amenities)
    """
    if not request.is_json:
        return jsonify({"error": "Not a JSON"}), 400

    data = request.get_json()

    if not data or (
            not data.get("states") and
            not data.get("cities") and
            not data.get("amenities")
    ):
        return jsonify(
                [place.to_dict() for place in storage.all(Place).values()]
        )

    places = set()

    state_ids = data.get("states", [])
    for state_id in state_ids:
        state = storage.get(State, state_id)
        if state:
            for city in state.cities:
                places.update(city.places)

    city_ids = data.get("cities", [])
    for city_id in city_ids:
        city = storage.get(City, city_id)
        if city:
            places.update(city.places)

    amenity_ids = data.get("amenities", [])
    if amenity_ids:
        places = [place for place in places if all(
            storage.get(Amenity, amenity_id) in place.amenities
            for amenity_id in amenity_ids
            )
        ]

    return jsonify([place.to_dict() for place in places])
