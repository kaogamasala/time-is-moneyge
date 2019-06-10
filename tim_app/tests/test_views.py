from django.test import TestCase, Client
from tim_app.models import Time_is_moneyge
from django.urls import reverse
from django.shortcuts import render, redirect
from accounts.models import CustomUser
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from tim_app.forms import MorningForm

# class TestLoginView(TestCase):

# 	"""ユーザー情報をself.userにセット"""
# 	def setUp(self):
# 		print("# {} is running!".format(self.id()))
# 		self.user = get_user_model().objects.create_user(
# 			last_name='admin', first_name='admin',  email='example@ex.co.jp', password='django000000')

# # 	"""'/accounts/signup/'にgetリクエストしてユーザー登録画面に遷移するかを検証"""
# # 	def test_get_success(self):
# # 		# テストクライアントでgetリクエストをシミュレート
# # 		response = self.client.get('/accounts/signup/')
# # 		# レスポンスを検証
# # 		self.assertEqual(response.status_code, 200)
# # 		# エラーメッセージが出ないことを検証
# # 		self.assertFalse(response.context['form'].errors)
# # 		self.assertTemplateUsed(response, 'registration/signup.html')

# # 	"""ログイン済みのユーザーが/accounts/signup/へgetリクエストすると"""
# # 	def test_get_by_unauthenticated_user(self):
# # 		# テストクライアントでログインをシミュレート
# # 		logged_in = self.client.login(email=self.user.email, password='django000000')
# # 		# ログイン成功したか検証
# # 		self.assertTrue(logged_in)
# # 		# ログイン済みのCookieを保持したクライアントでgetリクエスト実行
# # 		response = self.client.get(reverse('tim_app:timeismoneyge'))
# # 		self.assertEqual(response.status_code, 200)
# # 		# レスポンスを検証
# # 		self.assertTemplateUsed(response, 'tim_app/main.html')

# # 	""" テストクライアント作成の検証 """
# # 	def test_post_success(self):
# # 		response = self.client.post('/accounts/signup/', {
# # 		'last_name': 'test',
# # 		'first_name': 'test',
# # 		'email': 'testemail@test.co.jp',
# # 		'password': 'pass20190501',
# # 		'password2': 'pass20190501',
# # 		})
# # 		print("レスポンス",response)
# # 		self.assertEqual(response.status_code, 200)
# # 		# self.assertRedirects(response, '/accounts/profile/')
# # 		# self.assertTrue(get_user_model().objects.filter(email='testemail@test.co.jp').exists())
    

# # class TestTimeIsMoneygeListView(TestCase):
# # 	def setUp(self):
# # 		print("# {} is running!".format(self.id()))
# # 		self.user = get_user_model().objects.create_user(
# # 			last_name='admin', first_name='admin',  email='example@ex.co.jp', password='django000000')

# # 	def test_get(self):
# # 		logged_in = self.client.login(email=self.user.email, password='django000000')
# # 		response = self.client.get(reverse('tim_app:timeismoneyge_list',  kwargs={'id':self.user.id}))
# # 		self.assertEqual(response.status_code, 200)

  
# # class TestMorningView(TestCase):
# # 	def test_valid(self):
# # 		params = dict(morning_word="おはよう", )


# class YourTestCase(TestCase):
#     def test_profile(self, user_id):
#         user = CustomUser.objects.create(username='testuser')
#         user.set_password('12345')
#         user.save()
#         client = Client()
#         client.login(username='testuser', password='12345')
#         request = client.get("/account/profile/{}/".format(user.id), follow=True)
#         self.assertEqual(request.status_code, 200)

# # class TestCustomUser(TestCase):

# # 	def setUp(self):
# # 		print("# {} is running!".format(self.id()))

# # 	def test_post_login(self):	
# # 		"""
# # 		post_login()を実行するとlogin_countが+1されて保存されることを検証
# # 		"""
# # 		# テストで利用するレコードを作成
# # 		user = get_user_model().objects.create_user('user', password='pass')
# # 		print(user)
# # 		# 事前状態の検証
# # 		self.assertEqual(user.login_count, 0)

# # 		# テスト対象メソッドを呼び出す
# # 		user.post_login()

# # 		# 事後状態の検証
# # 		self.assertEqual(user.login_count, 1)
# # 		self.assertEqual(get_user_model().objects.get(pk=user.id).login_count, 1)

class Time_is_moneygeModelTests(TestCase):

	# fixtures = ['tim_app']

	#何も登録しなければ保存されたレコードの数は0個
	def test_is_empty(self):
		saved_timeismoneyges = Time_is_moneyge.objects.all()
		self.assertEqual(saved_timeismoneyges.count(), 0)

	# def test_is_not_empy(self):
	# 	time_is_moneyge = Time_is_moneyge()
	# 	save = time_is_moneyge.save() 
	# 	saved_timeismoneyges = Time_is_moneyge.objects.all()
	# 	self.assertEqual(saved_timeismoneyges.count(), 1)
