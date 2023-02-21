from flask import Flask,render_template,request,redirect,flash
from flask_bootstrap import Bootstrap
import os
from werkzeug.utils import secure_filename
from os.path import join, dirname, realpath
from colorthief import ColorThief


UPLOAD_FOLDER = join(dirname(realpath(__file__)), 'static/uploads/..')
ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg', 'gif']

app=Flask(__name__)
bootstrap=Bootstrap(app)
app.secret_key="Hello world"
app.config["UPLOAD_FOLDER"]=UPLOAD_FOLDER


def allowed_folder(file_name):
    return "." in file_name and file_name.rsplit(".",1)[1].lower() in ALLOWED_EXTENSIONS



@app.route("/",methods=["POST","GET"])
def home():
    if request.method=="POST":
        if "file" not in request.files:
            flash("No File Part")
            return redirect(request.url)
        file=request.files["file"]


        if file.filename=='':
            flash("No Selected File")
            return redirect(request.url)
        elif file.filename.split(".")[1] not in ALLOWED_EXTENSIONS:
            flash("Only Images please")
            return redirect(request.url)
        if file and allowed_folder(file.filename):
            filename=secure_filename(file.filename)

            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            image = f"static/{filename}"
            color_thief=ColorThief(image)
            pallete=color_thief.get_palette(color_count=11)

            hex_color=[]
            for rgb in pallete:
                hex_color.append("#{:02x}{:02x}{:02x}".format(rgb[0],rgb[1],rgb[2]))






        return render_template("index.html",image=image,colors=hex_color)
    return render_template("index.html")





if __name__=="__main__":
    app.run(debug=False,host='0.0.0.0')



