from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from pymongo import MongoClient
from bson.objectid import ObjectId
import datetime
import os

app = Flask(__name__)
CORS(app)

# MongoDB Connection
# client = MongoClient('mongodb://localhost:27017/')
client = MongoClient('mongodb+srv://ys7709995_db_user:M4mnir5IzF1AjMJv@vimala.9c8xz3l.mongodb.net/?appName=Vimala')
db = client['cine_rental']

# Helper to convert MongoDB documents to JSON serializable format
def serialize_doc(doc):
    if not doc:
        return None
    if isinstance(doc, list):
        return [serialize_doc(d) for d in doc]
    
    doc['id'] = str(doc['_id'])
    del doc['_id']
    return doc

# ================= EQUIPMENT API =================

@app.route('/api/equipment', methods=['GET'])
def get_equipment():
    equipment = list(db.equipment.find())
    return jsonify({
        'success': True,
        'data': serialize_doc(equipment)
    })

@app.route('/api/equipment', methods=['POST'])
def add_equipment():
    data = request.json
    
    new_equipment = {
        'name': data['name'],
        'type': data['type'],
        'price': float(data['price']),
        'image': data.get('image', ''),
        'description': data.get('description', ''),
        'stock': int(data['stock']),
        'created_at': datetime.datetime.now().isoformat(),
        'updated_at': datetime.datetime.now().isoformat()
    }
    
    result = db.equipment.insert_one(new_equipment)
    new_equipment['_id'] = result.inserted_id
    
    return jsonify({
        'success': True,
        'message': 'Equipment added successfully',
        'data': serialize_doc(new_equipment)
    })

@app.route('/api/equipment/<string:id>', methods=['DELETE'])
def delete_equipment(id):
    try:
        db.equipment.delete_one({'_id': ObjectId(id)})
        return jsonify({'success': True, 'message': 'Equipment deleted successfully'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ================= BOOKINGS API =================

@app.route('/api/bookings', methods=['GET'])
def get_bookings():
    bookings = list(db.bookings.find())
    return jsonify({
        'success': True,
        'data': serialize_doc(bookings)
    })

@app.route('/api/bookings', methods=['POST'])
def create_booking():
    data = request.json
    
    try:
        booking_id = 'BK' + str(int(datetime.datetime.now().timestamp()))[-8:]
        
        # Update stock for each item
        for item in data['equipmentItems']:
            db.equipment.update_one(
                {'_id': ObjectId(item['id'])},
                {'$inc': {'stock': -item['quantity']}}
            )
            
        new_booking = {
            'bookingId': booking_id,
            'customer': data['customer'],
            'equipmentItems': data['equipmentItems'],
            'projectDetails': data['projectDetails'],
            'totalAmount': data['totalAmount'],
            'status': 'pending',
            'createdAt': datetime.datetime.now().isoformat(),
            'updatedAt': datetime.datetime.now().isoformat()
        }
        
        result = db.bookings.insert_one(new_booking)
        new_booking['_id'] = result.inserted_id
        
        return jsonify({
            'success': True, 
            'message': 'Booking created successfully',
            'data': serialize_doc(new_booking)
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/bookings/<string:booking_id>', methods=['PUT'])
def update_booking_status(booking_id):
    data = request.json
    result = db.bookings.update_one(
        {'bookingId': booking_id},
        {'$set': {'status': data['status'], 'updatedAt': datetime.datetime.now().isoformat()}}
    )
    
    if result.modified_count:
        return jsonify({'success': True, 'message': 'Booking updated successfully'})
    else:
        return jsonify({'success': False, 'error': 'Booking not found'}), 404

# ================= GALLERY API =================

@app.route('/api/gallery', methods=['GET'])
def get_gallery():
    gallery = list(db.gallery.find())
    return jsonify({
        'success': True,
        'data': [item['image_url'] for item in gallery]
    })

@app.route('/api/gallery', methods=['POST'])
def update_gallery():
    data = request.json
    
    db.gallery.delete_many({})
    if data:
        db.gallery.insert_many([{'image_url': url} for url in data])
    
    return jsonify({
        'success': True, 
        'message': 'Gallery updated successfully',
        'data': data
    })

# ================= CONTACT API =================

@app.route('/api/contact', methods=['GET'])
def get_contact():
    contact = db.contact_info.find_one({}, sort=[('_id', -1)])
    return jsonify({
        'success': True,
        'data': serialize_doc(contact) if contact else {}
    })

@app.route('/api/contact', methods=['POST'])
def update_contact():
    data = request.json
    
    db.contact_info.insert_one({
        'address': data['address'],
        'phone': data['phone'],
        'email': data['email'],
        'hours': data['hours']
    })
    
    return jsonify({
        'success': True, 
        'message': 'Contact information updated successfully',
        'data': data
    })

# ================= AUTH API =================

@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email', data.get('username'))
    password = data['password']
    
    user = db.users.find_one({'email': email, 'password': password})
    
    if user:
        return jsonify({
            'success': True,
            'message': 'Login successful',
            'data': {
                'token': 'mock-jwt-token-' + str(user['_id']),
                'user': serialize_doc(user)
            }
        })
    else:
        return jsonify({'success': False, 'error': 'Invalid credentials'}), 401

@app.route('/api/auth/register', methods=['POST'])
def register():
    data = request.json
    
    if db.users.find_one({'email': data['email']}):
        return jsonify({'success': False, 'error': 'Email already exists'}), 400
        
    new_user = {
        'name': data['name'],
        'email': data['email'],
        'password': data['password'],
        'phone': data.get('phone', ''),
        'company': data.get('company', ''),
        'role': 'user',
        'created_at': datetime.datetime.now().isoformat()
    }
    
    db.users.insert_one(new_user)
    return jsonify({'success': True, 'message': 'Registration successful'})

if __name__ == '__main__':
    print("Starting Flask server with MongoDB...")
    app.run(debug=True, port=5000)
