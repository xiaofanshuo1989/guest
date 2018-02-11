from django.test import TestCase
from sign.models import Guest,Event
from django.contrib.auth.models import User

# Create your tests here.


class ModelTest(TestCase):
    def setUp(self):
        Event.objects.create(id=10, name='oppo oneplus 3',title= 33, status=True, address='shenzhen', start_time='2016-10-26 14:25:31')
        Guest.objects.create(id=10, event_id=10, realname='allen', phone='13415', mail='allen.zhen@qq.com', sign=False)


    def test_event_model(self):
        result = Event.objects.get(name='oppo oneplus 3')
        self.assertEqual(result.address, 'shenzhen')
        self.assertTrue(result.status)

    def test_guest_model(self):
        result = Guest.objects.get(realname='allen')
        self.assertEqual(result.phone, '13415')
        self.assertFalse(result.sign)


class IndexPageTest(TestCase):
    '''test index page'''

    def test_index_page_renders_index_template(self):
        '''test view '''
        response = self.client.get('/index/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

class LoginActionTest(TestCase):
    def setUp(self):
        User.objects.create_user('tim','4151@qq.com','qwertyuiop')

    def test_add_user(self):
        result = User.objects.get(username='tim')
        self.assertEqual(result.email, '4151@qq.com')

    def test_login_username_password_null(self):
        test_data = {'username':'','password':''}
        response = self.client.post('/login_action/', test_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"userName or password incorrect", response.content)

    def test_login_username_password_wrong(self):
        test_data = {'username':'abc','password':'123'}
        response = self.client.post('/login_action/', test_data)
        self.assertIn(b"userName or password incorrect", response.content)
        self.assertEqual(response.status_code, 200)

    def test_login_action_success(self):
        test_data = {'userName':'tim','password':'qwertyuiop'}
        response = self.client.post('/login_action/', test_data)
        print(response.content)
        self.assertEqual(response.status_code, 302)

class EventManageTest(TestCase):
    def setUp(self):
        User.objects.create_user('tim','4151@qq.com', 'qwertyuiop')
        Event.objects.create(id=10, name='oppo oneplus 3', title=33, status=True, address='shenzhen',start_time='2016-10-26 14:25:31')
        Guest.objects.create(id=10, event_id=10, realname='allen', phone='13415', mail='allen.zhen@qq.com', sign=False)
        #init login_user
        self.login_user = {'userName':'tim','password':'qwertyuiop'}

    def test_event_manage_success(self):
        response = self.client.post('/login_action/', self.login_user)
        response = self.client.post('/login_success/')
        self.assertIn(b'oppo oneplus 3',response.content)

    def test_event_search(self):
        response = self.client.post('/login_action/', self.login_user)
        response = self.client.post('/login_success/')
        response = self.client.get('/search_name/', {'name':'oppo'})

        self.assertIn(b'oppo oneplus 3', response.content)

