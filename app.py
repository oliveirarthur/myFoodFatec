from flask import Flask, jsonify, abort, make_response, request

app = Flask(__name__)

db_restaurants = [
    {
	    "id": 1,
	    "name": "Lanchonete Rafael",
	    "address": "Rua dos Testes",
	    "zipcode": "18045530",
	    "tags": ["aconchegante", "cerveja", "cervejeiro", "cervejaria", "cervejada", "bar", "partiu"],
	    "stars": 5,
	},
	{
	    "id": 2,
	    "name": "Lanchonete Rafael",
	    "address": "Rua dos Testes",
	    "zipcode": "18045530",
	    "tags": ["aconchegante", "cerveja", "cervejeiro", "cervejaria", "cervejada", "bar", "partiu"],
	    "stars": 5,
	},
	{
	    "id": 3,
	    "name": "Lanchonete Rafael",
	    "address": "Rua dos Testes",
	    "zipcode": "18045530",
	    "tags": ["aconchegante", "cerveja", "cervejeiro", "cervejaria", "cervejada", "bar", "partiu"],
	    "stars": 5,
	},
]


@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad Request'}), 400)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/v1/restaurants', methods=['GET'])
def get_restaurants():
    restaurants = {'total': len(db_restaurants), 'objects': db_restaurants}
    return jsonify(restaurants), 200


def search_restaurant(restaurant_id):
    """Find restaurants by id in db_restaurants"""
    for restaurant in db_restaurants:
        if restaurant['id'] == restaurant_id:
            return restaurant
    return None


@app.route('/v1/restaurants/<int:restaurant_id>', methods=['GET'])
def get_restaurant(restaurant_id):
    restaurant = search_restaurant(restaurant_id)
    if not restaurant:
        abort(404)
    return jsonify(restaurant), 200


@app.route('/v1/restaurants', methods=['POST'])
def create_restaurant():
    if not request.json or ('title' not in request.json):
        abort(400)
    restaurant = {
	    'name': request.json['name'],
		'address': request.json['address'],
		'zipcode': request.json['zipcode'],
		'tags': request.json['tags'],
		'stars': request.json['stars'],
    }
    db_restaurants.append(restaurant)
    return jsonify(restaurant), 201


@app.route('/v1/restaurants/<int:restaurant_id>', methods=['PUT'])
def update_restaurant(restaurant_id):
    restaurant = search_restaurant(restaurant_id)

    # basic validations
    if not restaurant:
        abort(404)

    if not request.json:
        abort(400)

    restaurant.update(**request.json)
    return jsonify(restaurant), 200


@app.route('/v1/restaurants/<int:restaurant_id>', methods=['DELETE'])
def delete_restaurant(restaurant_id):
    restaurant = search_restaurant(restaurant_id)
    if not restaurant:
        abort(404)

    db_restaurants.remove(restaurant)
    return ('', 204)


if __name__ == '__main__':
    app.run(debug=True)