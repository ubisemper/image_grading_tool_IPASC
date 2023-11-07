def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'jpg', 'jpeg', 'png', 'gif'}


def allowed_file_zip(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'zip'}