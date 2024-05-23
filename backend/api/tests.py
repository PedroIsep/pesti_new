from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from .models import Note
from django.core.exceptions import ValidationError


class CreateUserViewTest_CreatedUserOK(APITestCase):
    def test_create_user(self):
        url = reverse('register')
        data = {
            'username': 'testuser',
            'password': 'testpassword123',
        }
        
        # Make a POST request to the CreateUserView
        response = self.client.post(url, data, format='json')
        
        # Assert that the response status is 201 Created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class CreateUserViewTest_CreatedUserNOK(APITestCase):
    def test_create_user(self):
        url = reverse('register')
        data = {
            'username': 'testuser',
            'password': 'testpassword123',
        }
        
        # Make a POST request to the CreateUserView
        response = self.client.post(url, data, format='json')
        
        # Assert that the response status is 200 OK
        self.assertNotEqual(response.status_code, status.HTTP_200_OK)
        
        

class CreateUserViewTest_PassOK(APITestCase):
    def test_create_user(self):
        url = reverse('register')
        data = {
            'username': 'testuser',
            'password': 'testpassword123',
        }
        
        # Make a POST request to the CreateUserView
        self.client.post(url, data, format='json')
        
        # Assert that the password was set correctly
        user = User.objects.get(username='testuser')
        self.assertTrue(user.check_password('testpassword123'))


class CreateUserViewTest_PassNOK(APITestCase):
    def test_create_user(self):
        url = reverse('register')
        data = {
            'username': 'testuser',
            'password': 'testpassword123',
        }
        
        # Make a POST request to the CreateUserView
        self.client.post(url, data, format='json')
        
        # Assert that the password was set correctly
        user = User.objects.get(username='testuser')
        self.assertFalse(user.check_password('testpassword12'))

class CreateUserViewTest_UserOK(APITestCase):
    def test_create_user(self):
        url = reverse('register')
        data = {
            'username': 'testuser',
            'password': 'testpassword123',
        }
        
        # Make a POST request to the CreateUserView
        self.client.post(url, data, format='json')
        
        # Assert that the password was set correctly
        user = User.objects.get(username='testuser')
        self.assertTrue(user, self)
        
                
        
class NoteModelTest_ContentOK(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        
    def test_create_note(self):
        note = Note.objects.create(
            content="This is a test note",
            imageURL="http://example.com/image.jpg",
            model="TestModel",
            author=self.user
        )
        
        # Retrieve the note from the database
        retrieved_note = Note.objects.get(id=note.id)
        
        # Assert that the note's fields are correct
        self.assertEqual(retrieved_note.content, "This is a test note")
       
       
       
class NoteModelTest_UrlOK(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        
    def test_create_note(self):
        note = Note.objects.create(
            content="This is a test note",
            imageURL="http://example.com/image.jpg",
            model="TestModel",
            author=self.user
        )
        
        # Retrieve the note from the database
        retrieved_note = Note.objects.get(id=note.id)
        
        # Assert that the note's fields are correct
        self.assertEqual(retrieved_note.imageURL, "http://example.com/image.jpg")
 
 
 
class NoteModelTest_ModelOK(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        
    def test_create_note(self):
        note = Note.objects.create(
            content="This is a test note",
            imageURL="http://example.com/image.jpg",
            model="TestModel",
            author=self.user
        )
        
        # Retrieve the note from the database
        retrieved_note = Note.objects.get(id=note.id)
        
        # Assert that the note's fields are correct
        self.assertEqual(retrieved_note.model, "TestModel")



class NoteModelTest_AuthorOK(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        
    def test_create_note(self):
        note = Note.objects.create(
            content="This is a test note",
            imageURL="http://example.com/image.jpg",
            model="TestModel",
            author=self.user
        )
        
        # Retrieve the note from the database
        retrieved_note = Note.objects.get(id=note.id)
        
        # Assert that the note's fields are correct
        self.assertEqual(retrieved_note.author, self.user)
        

class NoteModelTest_ContentNOK(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
    
    def test_note_str_method(self):
        note = Note.objects.create(
            content="This is a test note with a long content to test the string representation",
            imageURL="http://example.com/image.jpg",
            model="TestModel",
            author=self.user
        )
        
        # Assert that the __str__ method returns the first 50 characters of the content
        self.assertEqual(str(note.content[:50]), "This is a test note with a long content to test th")



class NoteModelTest_ModelNOK(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        
    def test_create_note(self):
        note = Note.objects.create(
            content="This is a test note",
            imageURL="http://example.com/image.jpg",
            model="TestModel",
            author=self.user
        )
        
        # Retrieve the note from the database
        retrieved_note = Note.objects.get(id=note.id)
        
        # Assert that the note's fields are correct
        self.assertNotEqual(retrieved_note.model, "TestModel1")
        


class NoteModelTest_AuthorNOK(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.user1 = User.objects.create_user(username='testuser1', password='testpassword1')
            
    def test_create_note(self):
        note = Note.objects.create(
            content="This is a test note",
            imageURL="http://example.com/image.jpg",
            model="TestModel",
            author=self.user
        )
        
        # Retrieve the note from the database
        retrieved_note = Note.objects.get(id=note.id)
        
        # Assert that the note's fields are correct
        self.assertNotEqual(retrieved_note.author, self.user1)