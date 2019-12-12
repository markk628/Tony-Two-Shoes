from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
import os

host = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/meme')
client = MongoClient(host=f'{host}?retryWrites=false')
db = client.get_default_database()
memes = db.memes
comments = db.comments
price = db.price
memes.drop()
memes.insert_one({'title': 'Baby Yoda', 'price': '$1098320812', 'img': '/static/images/babyyoda.jpg'})
memes.insert_one({'title': 'Confused Cat', 'price': '$9319081213', 'img': '/static/images/confusedcat.jpg'})
memes.insert_one({'title': 'Dog', 'price': '$1239010210', 'img': '/static/images/dog.jpg'})
memes.insert_one({'title': 'Frog', 'price': '$19020180400', 'img': '/static/images/frog.jpg'})
memes.insert_one({'title': 'Juice WRLD', 'price': '$18927019040', 'img': '/static/images/juicewrld.jpg'})
memes.insert_one({'title': 'Plankton', 'price': '$28673912730', 'img': '/static/images/plankton.jpg'})


app = Flask(__name__)

@app.route('/')
def meme_index():
    return render_template('meme_index.html', memes=memes.find())

@app.route('/about')
def meme_about():
    return render_template('about.html')

@app.route('/memes')
def meme():
    return render_template('memes.html', memes=memes.find())

@app.route('/memes/new')
def meme_new():
    return render_template('meme_new.html', meme={}, title='New Meme')

@app.route('/memes', methods=['POST'])
def meme_submit():
    meme = {
        'title': request.form.get('title'),
        'price': request.form.get('price'),
        'img': request.form.get('img')
    }
    print(meme)
    meme_id = memes.insert_one(meme).inserted_id
    return redirect(url_for('meme_show', meme_id=meme_id))

@app.route('/memes/<meme_id>')
def meme_show(meme_id):
    meme = memes.find_one({'_id': ObjectId(meme_id)})
    meme_comments = comments.find({'meme_id': ObjectId(meme_id)})
    return render_template('meme_show.html', meme=meme, comments=meme_comments)

@app.route('/memes/<meme_id>', methods=['POST'])
def meme_update(meme_id):
    updated_meme = {
        'title': request.form.get('title'),
        'price': request.form.get('price'),
        'img': request.form.get('img')
    }
    memes.update_one(
        {'_id': ObjectId(meme_id)},
        {'$set': updated_meme})
    return redirect(url_for('meme_show', meme_id=meme_id))

@app.route('/memes/<meme_id>/edit')
def meme_edit(meme_id):
    meme = memes.find_one({'_id': ObjectId(meme_id)})
    return render_template('meme_edit.html', meme=meme, title='Edit Meme')

@app.route('/memes/<meme_id>/delete', methods=['POST'])
def meme_delete(meme_id):
    memes.delete_one({'_id': ObjectId(meme_id)})
    return redirect(url_for('meme_index'))

@app.route('/memes/<meme_id>/comments', methods=['POST'])
def comments_new(meme_id):
    comment = {
        'title': request.form.get('title'),
        'content': request.form.get('content'),
        'meme_id': ObjectId(request.form.get('meme_id'))
    }
    print(comment)
    comments.insert_one(comment)
    return redirect(url_for('meme_show', meme_id=request.form.get('meme_id')))

@app.route('/memes/<meme_id>/comments/<comment_id>', methods=['POST'])
def comment_update(meme_id, comment_id):
    updated_comment = {
        'title': request.form.get('title'),
        'content': request.form.get('content'),
        'meme_id': ObjectId(request.form.get('meme_id'))
    }
    comments.update_one(
        {'_id': ObjectId(comment_id)},
        {'$set': updated_comment})
    return redirect(url_for('meme_show', comment_id=comment_id, meme_id=meme_id))

@app.route('/memes/<meme_id>/comments/<comment_id>/edit')
def comment_edit(meme_id, comment_id):
    meme = memes.find_one({'_id': ObjectId(meme_id)})
    comment = comments.find_one({'_id': ObjectId(comment_id)})
    return render_template('comment_edit.html', comment=comment, meme=meme, meme_id=meme_id, title='Edit Comment')

@app.route('/memes/<meme_id>/comments/<comment_id>/delete', methods=['POST'])
def comments_delete(meme_id, comment_id):
    comment = comments.find_one({'_id': ObjectId(comment_id)})
    comments.delete_one({'_id': ObjectId(comment_id)})
    return redirect(url_for('meme_show', meme_id=comment.get('meme_id')))


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT', 5000))