"""from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
	 拡張 ユーザーモデル

	class Meta(AbstractUser.Meta):
		db_table = 'custom_user'

		age = models.IntegerField('年齢', blank=True, null=True)"""


from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

class CustomUserManager(BaseUserManager):
    """ ユーザーネーム無しのユーザーモデルを定義 """
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """メールとパスワードでユーザーを作成して保存する"""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """メールとパスワードを使用して通常のユーザーを作成して保存する"""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """メールとパスワードでスーパーユーザーを作成して保存する"""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
    """拡張ユーザーモデル"""

    class Meta(AbstractUser.Meta):
        db_table = 'custom_user'

    # emailをオーバーライドして入力必須制限、ユニーク制約を付与
    last_name = models.CharField(
        '姓',
        max_length=150,
        blank=False,
        null=False,
        )
    first_name = models.CharField(
        '名',
        max_length=150,
        blank=False,
        null=False,
        )
    email = models.EmailField('メールアドレス', unique=True)
    # username = models.CharField(
    #     'ユーザー名',
    #     max_length=150,
    #     blank=True,
    #     null=True,
    #     help_text="半角アルファベット、半角数字、@/./+/-/_で150文字以下にしてください。",
    #     validators=[AbstractUser.username_validator],
    #     )
    #age = models.IntegerField('年齢', blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()
