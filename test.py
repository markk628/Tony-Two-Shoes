from unittest import TestCase, main as unittest_main, mock
from flask import Flask
from app import app
from bson.objectid import ObjectId

sample_meme_id = ObjectId('5d55cffc4a3d4031f42827a3')
sample_meme = {
    'title': '',
    'price': "$2",
    'img': 'https://i.chzbgr.com/full/9233901568/hB41CDDDE/u-first-start-talking-to-someone-and-u-act-all-proper-bc-u-aint-sure-when-u-can-start-being-weird'
    
}
sample_form_data = {
    'title': sample_meme['title'],
    'price': sample_meme['price'],
    'img': sample_meme['img']
}

class MemesTests(TestCase):
    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True

    '''tests if home page renders'''
    def test_index(self):
        result = self.client.get('/')
        self.assertEqual(result.status, '200 OK')
        self.assertIn(b'memes', result.data)

    '''tests if about page renders'''
    def test_about(self):
        result = self.client.get('/about')
        self.assertEqual(result.status, '200 OK')
        self.assertIn(b'memes', result.data)

    '''tests if default memes page renders'''
    def test_memes(self):
        result = self.client.get('/memes')
        self.assertEqual(result.status, '200 OK')
        self.assertIn(b'memes', result.data)

    '''tests if new meme page renders'''
    def test_new(self):
        result = self.client.get('/memes/new')
        self.assertEqual(result.status, '200 OK')
        self.assertIn(b'memes', result.data)
    
    '''uses mock data to see if individual meme page renders'''
    @mock.patch('pymongo.collection.Collection.find_one')
    def test_show_meme(self, mock_find):
        mock_find.return_value = sample_meme
        result = self.client.get(f'/memes/{sample_meme_id}')
        self.assertEqual(result.status, '200 OK')
        self.assertIn(b'memes', result.data)

    '''uses mock data to see if edit meme page renders'''
    @mock.patch('pymongo.collection.Collection.find_one')
    def test_edit_meme(self, mock_find):
        mock_find.return_value = sample_meme
        result = self.client.get(f'/memes/{sample_meme_id}/edit')
        self.assertEqual(result.status, '200 OK')
        self.assertIn(b'memes', result.data)
    
    '''uses mock data to see if meme has successfully been uploaded to database'''
    @mock.patch('pymongo.collection.Collection.insert_one')
    def test_submit_meme(self, mock_insert):
        result = self.client.post('/memes', data=sample_form_data)
        self.assertEqual(result.status, '302 FOUND')
        mock_insert.assert_called_with(sample_meme)

    '''uses mock data to see if meme has been deleted'''
    @mock.patch('pymongo.collection.Collection.delete_one')
    def test_delete_meme(self, mock_delete):
        form_data = {'_method': 'DELETE'}
        result = self.client.post(f'/memes/{sample_meme_id}/delete', data=form_data)
        self.assertEqual(result.status, '302 FOUND')
        mock_delete.assert_called_with({'_id': sample_meme_id})

if __name__ == '__main__':
    unittest_main()