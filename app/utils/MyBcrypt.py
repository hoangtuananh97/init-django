from django.contrib.auth.hashers import BCryptSHA256PasswordHasher


class MyBCryptSHA256PasswordHasher(BCryptSHA256PasswordHasher):
    BCryptSHA256PasswordHasher.rounds = 15
