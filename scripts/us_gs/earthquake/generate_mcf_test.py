# Copyright 2022 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Tests for generate_mcf."""

import os
import unittest
from unittest import mock
import sys

MODULE_DIR = os.path.dirname(__file__)
TEST_DIR = os.path.join(MODULE_DIR, "test_data")
sys.path.insert(0, MODULE_DIR)

from generate_mcf import generate_mcf
from generate_mcf import read_cache

mock_latlng_to_places = {
    (11, -66): [],
    (41.4, -81.9): ['geoId/3956882', 'geoId/39'],
    (36.9944992, -118.3001633): ['geoId/06'],
    (31.2593, 131.471): ['country/JPN']
}


def mock_latlng2places(id_to_latlng):
    return {
        id: mock_latlng_to_places.get(latlng, [])
        for id, latlng in id_to_latlng.items()
    }


class USGSEarthquakeMCFTest(unittest.TestCase):

    @mock.patch('util.latlng_recon_service.latlng2places', mock_latlng2places)
    def test_generate_mcf_without_cache(self):
        input = os.path.join(TEST_DIR, 'input*.csv')
        output = os.path.join(TEST_DIR, 'output.mcf')
        expected_mcf = os.path.join(TEST_DIR, 'expected.mcf')
        # Clear cache if exists.
        cache = os.path.join(TEST_DIR, 'test.cache')
        if os.path.isfile(cache):
            os.remove(cache)

        generate_mcf(input, output, cache)

        with open(output, 'r') as file:
            got = file.read()
        with open(expected_mcf, 'r') as file:
            want = file.read()
        self.assertEqual(got, want)

        cache_got = read_cache(cache)
        self.assertEqual(cache_got, mock_latlng_to_places)

        os.remove(output)
        os.remove(cache)


if __name__ == "__main__":
    unittest.main()
