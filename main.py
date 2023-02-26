from flask import Flask,render_template,request,redirect,flash,send_from_directory
from flask_bootstrap import Bootstrap
import os
import numpy as np
from werkzeug.utils import secure_filename
from rembg import remove
from PIL import Image,ImageDraw
import qrcode








ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg', 'gif']

app=Flask(__name__)
bootstrap=Bootstrap(app)
app.secret_key="BaowaKhaidhanlid"
app.config["IMAGE_UPLOADS"]="C:\\Users\\khalid\\PycharmProjects\\exam-11\\static\\uploads"
app.config["CLIENT_IMAGES"]="C:\\Users\\khalid\\PycharmProjects\\exam-11\\static\\client"



@app.route('/download/<filename>')
def download(filename):
    return send_from_directory(app.config["CLIENT_IMAGES"],filename,as_attachment=True)









def allowed_folder(file_name):
    return "." in file_name and file_name.rsplit(".",1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/",methods=["POST","GET"])
def home():
    return render_template("index.html")



@app.route("/Resizing",methods=["POST","GET"])
def resize():

    if request.method=="POST":
        try:
            x=int(request.form.get("x"))
            y=int(request.form.get("y"))
        except ValueError:
            flash("Enter Number Please")
            return redirect(request.url)

        if "file" not in request.files:
            flash("No File Part")
            return redirect(request.url)
        file=request.files["file"]
        if file.filename.split(".")[1] not in ALLOWED_EXTENSIONS:
            flash("Only Images Please")
            return redirect(request.url)
        if file and allowed_folder(file.filename):
            filename = secure_filename(file.filename)
            re_img = f"static/client/{filename}"
            file.save(os.path.join(app.config["CLIENT_IMAGES"],filename))
            image=Image.open(re_img)
            resized=image.resize((x,y),Image.LANCZOS)
            resized.save(os.path.join(app.config["CLIENT_IMAGES"],filename))


            return render_template("resizing.html",img=re_img)





    return render_template("resizing.html")



@app.route("/bg_remover",methods=["POST","GET"])
def remover():

    if request.method=="POST":

        if "file" not in request.files:
            flash("No File Part")
            return redirect(request.url)



        file=request.files["file"]
        if file.filename == '':
            flash("No Selected File")
            return redirect(request.url)
        elif file.filename.split(".")[1] not in ALLOWED_EXTENSIONS:
            flash("Only Images please")
            return redirect(request.url)
        if file and allowed_folder(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config["IMAGE_UPLOADS"],filename))
            img=Image.open(f"static/uploads/{filename}")
            removed=remove(img)
            image=f"static/uploads/{filename}"

            no_bg=f"static/client/No_background_{filename.split('.')[0]}.png"
            removed.save(os.path.join(app.config["CLIENT_IMAGES"],f"No_background_{filename.split('.')[0]}.png"))


        return render_template("bg_remover.html", image=image,removed=no_bg)
    return render_template("bg_remover.html")


@app.route("/QRcode_generator",methods=["POST","GET"])
def qr_code():
    if request.method == "POST":
        color=request.form.get("colors")
        url=request.form.get("url")
        img_file = request.files["file"]
        version=request.form.get("version")
        img_name = f"static/client/My_qr.png"


        if  len(img_file.filename)!=0:

            file = img_file
            if file.filename.split(".")[1] not in ALLOWED_EXTENSIONS:
                flash("Only Images please")
                return redirect(request.url)
            if file and allowed_folder(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config["CLIENT_IMAGES"],f"image.{filename.split('.')[1]}"))
                im = Image.open(f"static/client/image.{filename.split('.')[1]}")
                fill_color = (255, 255, 255)

                im = im.convert("RGBA")
                if im.mode in ('RGBA', 'LA'):
                    background = Image.new(im.mode[:-1], im.size, fill_color)
                    background.paste(im, im.split()[-1])  # omit transparency
                    im = background
                im.convert("RGB").save(os.path.join(app.config["CLIENT_IMAGES"],"My_qr.png"))

                logo = Image.open(img_name)
                basew = 100
                wpercent = (basew / float(logo.size[0]))
                hsize = int((float(logo.size[1]) * float(wpercent)))
                logo = logo.resize((basew + 15, hsize + 15), Image.LANCZOS)

                qr_code = qrcode.QRCode(version=version, error_correction=qrcode.constants.ERROR_CORRECT_H)
                qr_code.add_data(url)
                qr_code.make()

                qrimg = qr_code.make_image(fill_color=color, back_color="white").convert("RGB")
                pos = ((qrimg.size[0] - logo.size[0]) // 2,
                       (qrimg.size[1] - logo.size[1]) // 2)
                qrimg.paste(logo, pos)

                qrimg.save(img_name, "PNG")
                L_img = Image.open(img_name)
                L_img = L_img.resize((400, 400), Image.LANCZOS)
                L_img.save(img_name)
                return render_template("qr_code.html", img=img_name)

        else:
            qr_code = qrcode.QRCode(version=int(version), error_correction=qrcode.constants.ERROR_CORRECT_H)
            qr_code.add_data(url)
            qr_code.make()
            qrimg = qr_code.make_image(fill_color=color, back_color="white").convert("RGB")

            qrimg.save(os.path.join(app.config["CLIENT_IMAGES"],"My_qr.png"))
            L_img = Image.open(img_name)
            L_img = L_img.resize((400, 400), Image.LANCZOS)
            L_img.save(img_name)
            return render_template("qr_code.html",img=img_name)





    return render_template("qr_code.html")



@app.route("/image_rotation",methods=["POST","GET"])
def image_rotation():
    if request.method=="POST":
        if "file" not in request.files:
            flash("No File Part")
            return redirect(request.url)
        file = request.files["file"]
        if file.filename.split(".")[1] not in ALLOWED_EXTENSIONS:
            flash("Only Images Please")
            return redirect(request.url)
        if file and allowed_folder(file.filename):
            filename = secure_filename(file.filename)
            rotation = f"static/client/{filename.split('.')[0]}.png"
            file.save(os.path.join(app.config["CLIENT_IMAGES"], f"{filename.split('.')[0]}.png"))
            img=Image.open(rotation).convert("RGB")
            npImage = np.array(img)
            h,w=img.size
            alpha = Image.new('L', img.size,0)
            draw = ImageDraw.Draw(alpha)
            draw.pieslice([0,0,h,w],0,360,fill=255)
            npAlpha=np.array(alpha)
            npImage=np.dstack((npImage,npAlpha))

            Image.fromarray(npImage).save(os.path.join(app.config["CLIENT_IMAGES"], f"{filename.split('.')[0]}.png"))


            return render_template("cropping.html",img=rotation)




    return render_template("cropping.html")











if __name__=="__main__":
    app.run(debug=True)



