from givabit.backend.charity import Charity
from givabit.backend.errors import MissingValueException, MultipleValueException

from givabit.test_common import test_data
from givabit.test_common import test_utils

class CharityRepositoryTest(test_utils.TestCase):
    def setUp(self):
        super(CharityRepositoryTest, self).setUp()
        self.all_charities = [test_data.c1, test_data.c2, test_data.c3, test_data.c4]
        for charity in self.all_charities:
            self.charity_repo.add_or_update_charity(charity)

    def test_lists_charities(self):
        self.assertSequenceEqual(self.charity_repo.list_charities(), self.all_charities)

    def test_gets_single_charity(self):
        self.assertEqual(self.charity_repo.get_charity('Shelter'), test_data.c1)
        self.assertEqual(self.charity_repo.get_charity('Oxfam'), test_data.c2)
        with self.assertRaises(MissingValueException):
            self.charity_repo.get_charity('Does not exist')
        try:
            self.charity_repo.get_charity('BHF')
        except MultipleValueException, e:
            self.assertSequenceEqual(e.values, [test_data.c3, test_data.c4])

    def test_gets_charity_by_id(self):
        self.assertEquals(self.charity_repo.get_charity(id=test_data.c1.key().id()), test_data.c1)

    def test_getting_missing_charity_by_id_throws(self):
        missing_id = 0
        while missing_id in map(lambda charity: charity.key().id(), self.all_charities):
            missing_id += 1

        with self.assertRaises(MissingValueException):
            self.charity_repo.get_charity(id=missing_id)
