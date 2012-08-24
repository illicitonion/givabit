import test_data
import test_utils

from charity import Charity
from charity_repository import CharityRepository
from errors import MissingValueException, MultipleValueException

class CharityRepositoryTest(test_utils.TestCase):
    def setUp(self):
        super(CharityRepositoryTest, self).setUp()
        self.all_charities = [test_data.c1, test_data.c2, test_data.c3, test_data.c4]
        self.repo = CharityRepository()
        for charity in self.all_charities:
            self.repo.add_or_update_charity(charity)

    def test_lists_charities(self):
        self.assertSequenceEqual(self.repo.list_charities(), self.all_charities)

    def test_gets_single_charity(self):
        self.assertEqual(self.repo.get_charity('Shelter'), test_data.c1)
        self.assertEqual(self.repo.get_charity('Oxfam'), test_data.c2)
        self.assertRaises(MissingValueException, lambda: self.repo.get_charity('Does not exist'))
        try:
            self.repo.get_charity('BHF')
        except MultipleValueException, e:
            self.assertSequenceEqual(e.values, [test_data.c3, test_data.c4])
