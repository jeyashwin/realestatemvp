from django.test import TestCase

from property import models


class PropertyModelTests(TestCase):

    def test_statelist_str(self):
        """Test the statelist string representation"""
        state = models.StateList.objects.create(stateFullName="Newyork", stateShortName="NY")

        self.assertEqual(str(state), state.stateFullName)