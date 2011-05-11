from boar.accounts.models import UserProfile
from django.test.testcases import TestCase

class UserProfileTestCase(TestCase):
    
    def test_create_from_name(self):
        u = UserProfile.objects.create_from_name('Joe Shmo')
        self.assertEqual(u.user.first_name, 'Joe')
        self.assertEqual(u.user.last_name, 'Shmo')
        self.assertEqual(u.user.username, 'joe.shmo')
        
        u = UserProfile.objects.create_from_name('Joe Shmo')
        self.assertEqual(u.user.username, 'joe.shmo.2')
        
        u = UserProfile.objects.create_from_name('Joe S!h-m%(&o Fo')
        self.assertEqual(u.user.first_name, 'Joe')
        self.assertEqual(u.user.last_name, 'S!h-m%(&o Fo')
        self.assertEqual(u.user.username, 'joe.shmo.fo')
        
        u = UserProfile.objects.create_from_name('Joe')
        self.assertEqual(u.user.first_name, 'Joe')
        self.assertEqual(u.user.last_name, '')
        self.assertEqual(u.user.username, 'joe')
        