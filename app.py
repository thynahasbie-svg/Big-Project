from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

mapel_list = [
    {"nama_mapel": "Matematika Lanjutan", "catatan": "Vektor dan Matriks", "nilai": 90.0},
    {"nama_mapel": "Informatika", "catatan": "Python & Flask Web", "nilai": 92.0},
]

todos = ["Belajar Vektor", "Latihan soal di VS Code"]


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    return render_template("contact.html")


@app.route("/project")
def project():
    return render_template("project.html")


#HALAMAN WAKTU (Clock & Timer)
@app.route('/waktu')
def waktu():
    return render_template('waktu.html')


@app.route("/mapel", methods=["GET", "POST"])
def mapel():
    error = None
    if request.method == "POST":
        nama_mapel = request.form.get("nama_mapel", "").strip()
        catatan = request.form.get("catatan", "").strip()
        try:
            nilai = float(request.form.get("nilai", 0))
            if not nama_mapel or not catatan:
                error = "Nama mapel dan catatan wajib diisi."
            elif nilai < 0 or nilai > 100:
                error = "Nilai harus berada di rentang 0 sampai 100."
            else:
                mapel_list.append({
                    "nama_mapel": nama_mapel,
                    "catatan": catatan,
                    "nilai": nilai,
                })
                return redirect(url_for("mapel"))
        except ValueError:
            error = "Format nilai tidak valid."

    rata_rata = sum(item["nilai"] for item in mapel_list) / len(mapel_list) if mapel_list else 0.0
    return render_template("mapel.html", mapel_list=mapel_list, rata_rata=rata_rata, error=error)


@app.route("/mapel/hapus/<int:index>")
def hapus_mapel(index):
    if 0 <= index < len(mapel_list):
        mapel_list.pop(index)
    return redirect(url_for("mapel"))


@app.route("/todo", methods=["GET", "POST"])
def todo():
    if request.method == "POST":
        item = request.form.get("item", "").strip()
        if item:
            todos.append(item)
        return redirect(url_for("todo"))
    return render_template("todo.html", todos=todos, edit_index=None, edit_value="")


@app.route("/todo/edit/<int:index>", methods=["GET", "POST"])
def todo_edit(index):
    if index < 0 or index >= len(todos):
        return redirect(url_for("todo"))
    if request.method == "POST":
        item_baru = request.form.get("item", "").strip()
        if item_baru:
            todos[index] = item_baru
        return redirect(url_for("todo"))
    return render_template("todo.html", todos=todos, edit_index=index, edit_value=todos[index])


@app.route("/todo/hapus/<int:index>", methods=["POST"])
def todo_hapus(index):
    if 0 <= index < len(todos):
        todos.pop(index)
    return redirect(url_for("todo"))


if __name__ == "__main__":
    app.run(debug=True)