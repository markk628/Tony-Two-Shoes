from unittest import TestCase, main as unittest_main, mock
from flask import Flask
from app import app
from bson.objectid import ObjectId

sample_meme_id = ObjectId('5d55cffc4a3d4031f42827a3')
sample_shirt = {
    'title': '',
    'price': "$2",
    'img': 'https://i.chzbgr.com/full/9233901568/hB41CDDDE/u-first-start-talking-to-someone-and-u-act-all-proper-bc-u-aint-sure-when-u-can-start-being-weird'
    
}
sample_form_data = {
    'title': sample_shirt['title'],
    'price': sample_shirt['price'],
    'img': sample_shirt['img']
}