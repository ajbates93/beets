# This file is part of beets.
# Copyright 2014, Thomas Scholtes.
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.

from _common import unittest
from helper import TestHelper

from beets.mediafile import MediaFile


class InfoTest(unittest.TestCase, TestHelper):

    def setUp(self):
        self.setup_beets()
        self.load_plugins('info')

    def tearDown(self):
        self.unload_plugins()
        self.teardown_beets()

    def run_command(self, *args):
        super(InfoTest, self).run_command('info', *args)

    def test_path(self):
        path = self.create_mediafile_fixture()

        mediafile = MediaFile(path)
        mediafile.albumartist = 'AAA'
        mediafile.disctitle = 'DDD'
        mediafile.genres = ['a', 'b', 'c']
        mediafile.composer = None
        mediafile.save()

        out = self.run_with_output(path)
        self.assertIn(path, out)
        self.assertIn('albumartist: AAA', out)
        self.assertIn('disctitle: DDD', out)
        self.assertIn('genres: a; b; c', out)
        self.assertNotIn('composer:', out)

    def test_item_query(self):
        items = self.add_item_fixtures(count=2)
        items[0].album = 'xxxx'
        items[0].write()
        items[0].album = 'yyyy'
        items[0].store()

        out = self.run_with_output('album:yyyy')
        self.assertIn(items[0].path, out)
        self.assertIn('album: xxxx', out)

        self.assertNotIn(items[1].path, out)

    def test_item_library_query(self):
        item, = self.add_item_fixtures()
        item.album = 'xxxx'
        item.store()

        out = self.run_with_output('--library', 'album:xxxx')
        self.assertIn(item.path, out)
        self.assertIn('album: xxxx', out)

    def test_collect_item_and_path(self):
        path = self.create_mediafile_fixture()
        mediafile = MediaFile(path)
        item, = self.add_item_fixtures()

        item.album = mediafile.album = 'AAA'
        item.tracktotal = mediafile.tracktotal = 5
        item.title = 'TTT'
        mediafile.title = 'SSS'

        item.write()
        item.store()
        mediafile.save()

        out = self.run_with_output('--summarize', 'album:AAA', path)
        self.assertIn('album: AAA', out)
        self.assertIn('tracktotal: 5', out)
        self.assertIn('title: [various]', out)


def suite():
    return unittest.TestLoader().loadTestsFromName(__name__)

if __name__ == '__main__':
    unittest.main(defaultTest='suite')
