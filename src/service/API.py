from flask import Flask, request, jsonify
from cloudinary_service import upload_image
from src.database.DAO.admin.ProductAdminDAO import ProductDAO

app = Flask(__name__)

@app.route('/')
def home():
    return "API is running!"

@app.route('/upload-image', methods=['POST'])
def upload_image_endpoint():
    if 'image' not in request.files:
        return jsonify({'error': 'No image file'}), 400

    image_file = request.files['image']
    image_url = upload_image(image_file)
    if not image_url:
        return jsonify({'error': 'Upload failed'}), 500

    id_prod = request.form.get('id_prod')
    if not id_prod:
        return jsonify({'error': 'No product id'}), 400

    product = ProductDAO.get_product_by_id(id_prod)
    if not product:
        return jsonify({'error': 'Product not found'}), 404

    product_data = {
        "id_prod": id_prod,
        "name": product.name,
        "unit": product.unit,
        "price": product.price,
        "description": product.description,
        "id_category": product.id_category,
        "image_url": image_url
    }

    success = ProductDAO.update_product(product_data)
    if success:
        return jsonify({'message': 'Upload and update successful', 'image_url': image_url}), 200
    else:
        return jsonify({'error': 'Update DB failed'}), 500

if __name__ == '__main__':
    app.run(debug=True)
