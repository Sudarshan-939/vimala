from pymongo import MongoClient
import datetime
import bcrypt

# Connect to MongoDB
# client = MongoClient('mongodb://localhost:27017/')
client = MongoClient('mongodb+srv://ys7709995_db_user:M4mnir5IzF1AjMJv@vimala.9c8xz3l.mongodb.net/?appName=Vimala')
db = client['cine_rental']

def seed_database():
    print("Seeding database...")
    
    # 1. Users
    users_collection = db['users']
    if users_collection.count_documents({'email': 'vimala'}) == 0:
        # Hash the admin password
        hashed_password = bcrypt.hashpw('vimala'.encode('utf-8'), bcrypt.gensalt())
        
        users_collection.insert_one({
            'email': 'vimala',
            'password': hashed_password,
            'name': 'Vimala Admin',
            'role': 'admin',
            'created_at': datetime.datetime.now().isoformat()
        })
        print("Admin user created with hashed password.")
    else:
        print("Admin user already exists.")

    # 2. Contact Info
    contact_collection = db['contact_info']
    if contact_collection.count_documents({}) == 0:
        contact_collection.insert_one({
            'address': '123 Film Street, Mumbai, India',
            'phone': '+91 98765 43210',
            'email': 'info@vimalaenterprises.com',
            'hours': 'Mon-Sat: 9AM-7PM'
        })
        print("Contact info seeded.")
    else:
        print("Contact info already exists.")

    # 3. Gallery
    gallery_collection = db['gallery']
    if gallery_collection.count_documents({}) == 0:
        images = [
            'https://images.unsplash.com/photo-1594909122845-11baa439b7bf?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80',
            'https://images.unsplash.com/photo-1517077304055-6e89abbf09b0?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80',
            'https://images.unsplash.com/photo-1588681664899-f142ff2dc9b1?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80',
            'https://images.unsplash.com/photo-1591862719729-6e15bd642900?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80',
            'https://images.unsplash.com/photo-1571844307880-751c6d86f3f3?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80',
            'https://images.unsplash.com/photo-1563298258-c2c4df7b9070?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80'
        ]
        gallery_collection.insert_many([{'image_url': img} for img in images])
        print(f"{len(images)} gallery images seeded.")
    else:
        print("Gallery already has data.")

    # 4. Equipment
    equipment_collection = db['equipment']
    if equipment_collection.count_documents({}) == 0:
        equipment_list = [
            {
                "name": "Sony FX6 Cinema Camera", 
                "type": "camera", 
                "price": 13500, 
                "image": "", 
                "description": "Full-frame cinema camera with advanced autofocus and 4K 120p recording", 
                "stock": 5
            },
            {
                "name": "ARRI SkyPanel S60-C", 
                "type": "light", 
                "price": 9000, 
                "image": "", 
                "description": "High-output LED soft light with full color spectrum control", 
                "stock": 3
            },
            {
                "name": "Canon C70 Cinema Camera", 
                "type": "camera", 
                "price": 11250, 
                "image": "", 
                "description": "Compact cinema camera with RF mount and dual gain output", 
                "stock": 4
            },
            {
                "name": "Kino Flo Celeb 200", 
                "type": "light", 
                "price": 6375, 
                "image": "", 
                "description": "LED fixture with high CRI and flicker-free operation", 
                "stock": 7
            },
            {
                "name": "Sigma 18-35mm T2 Cine Lens", 
                "type": "lens", 
                "price": 6750, 
                "image": "", 
                "description": "High-speed zoom lens with consistent T-stop throughout range", 
                "stock": 2
            },
            {
                "name": "Blackmagic Ursa Mini Pro 12K", 
                "type": "camera", 
                "price": 18750, 
                "image": "", 
                "description": "Professional cinema camera with 12K sensor and EF lens mount", 
                "stock": 2
            }
        ]
        
        for item in equipment_list:
            item['created_at'] = datetime.datetime.now().isoformat()
            item['updated_at'] = datetime.datetime.now().isoformat()
            
        equipment_collection.insert_many(equipment_list)
        print(f"{len(equipment_list)} equipment items seeded.")
    else:
        print("Equipment already has data.")

    print("Database seeding completed.")

if __name__ == '__main__':
    seed_database()
