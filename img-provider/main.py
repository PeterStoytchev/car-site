import os, uuid, webp, boto3

from PIL import Image
from flask import Flask, request

app = Flask(__name__)

@app.route("/", methods=["POST"])
def root_post():
    file = request.files['file']
    filename = str(uuid.uuid4().hex)

    tmp_path = os.path.join("imgs", f"{filename}.tmp")
    file.save(tmp_path)

    img = Image.open(tmp_path)
    
    new_size = 960*540
    orig_size = img.width * img.height 

    if orig_size > new_size:
        img = img.resize((960,540), Image.Resampling.BOX)
    elif orig_size < new_size:
        img = img.resize((960,540), Image.Resampling.LANCZOS)

    webp_path = os.path.join("imgs", f"{filename}.webp")
    webp.save_image(img, webp_path, quality=75)

    s3 = boto3.client('s3')
    with open(webp_path, "rb") as f:
        s3.upload_fileobj(f, "arn:aws:s3::326782393948:accesspoint/m6ow8xby39me6.mrap", f"{filename}.webp", ExtraArgs={'ACL':'public-read'})

    os.remove(tmp_path)
    os.remove(webp_path)

    return filename, 200

@app.route("/<id>", methods=["GET"])
def root_get(id):
    s3 = boto3.client('s3')
    return s3.generate_presigned_url('get_object', Params={'Bucket': "arn:aws:s3::326782393948:accesspoint/m6ow8xby39me6.mrap", 'Key': f"{id}.webp"}, ExpiresIn=60), 200

@app.route("/<id>", methods=["DELETE"])
def root_del(id):
    s3 = boto3.client('s3')
    s3.delete_object(
        Bucket="arn:aws:s3::326782393948:accesspoint/m6ow8xby39me6.mrap",
        Key=f"{id}.webp"
    )
    return "Deleted!", 200

if __name__ == "__main__":
    if not os.path.exists("imgs"):
        os.mkdir("imgs")
    
    app.run(debug=True, host="0.0.0.0", port=8081)