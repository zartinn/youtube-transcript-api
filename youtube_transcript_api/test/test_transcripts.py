from unittest import TestCase
from unittest.mock import Mock
from mock import patch

import os
import json

import requests

import httpretty

from .._transcripts import (
    TranscriptListFetcher
)


def load_asset(filename):
    filepath = '{dirname}/assets/{filename}'.format(
        dirname=os.path.dirname(__file__), filename=filename)

    with open(filepath, mode="rb") as file:
        return file.read()


class TestYouTubeTranscriptApi(TestCase):
    def setUp(self):
        httpretty.enable()
        httpretty.register_uri(
            httpretty.GET,
            'https://www.youtube.com/watch',
            body=load_asset('youtube.html.static')
        )
        httpretty.register_uri(
            httpretty.GET,
            'https://www.youtube.com/api/timedtext',
            body=load_asset('transcript.xml.static')
        )

    def tearDown(self):
        httpretty.reset()
        httpretty.disable()

    def test_extract_metadata_json(self):
        # Load HTML responses
        valid_html = load_asset('youtube_transcripts_disabled2.html.static')  # replace with the actual file name
        # invalid_html = load_asset('invalid_html_file.html')  # replace with the actual file name
        valid_html = valid_html.decode('utf-8')

        # Test with a valid HTML and video_id
        video_id = 'valid_video_id'
        http_client = Mock()
        fetcher = TranscriptListFetcher(http_client)
        result = fetcher._extract_metadata_json(valid_html, video_id)

        # test that result has specific keys
        self.assertIn('videoId', result)
        self.assertIn('title', result)
        self.assertIn('lengthSeconds', result)
        self.assertIn('shortDescription', result)
        self.assertIn('author', result)
        self.assertIn('viewCount', result)
        self.assertIn('uploadDate', result)
