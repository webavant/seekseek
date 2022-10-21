from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser

from .search_functions import *

from vlc import MediaPlayer
player = MediaPlayer()

class Play(APIView):
    """
    Instruct the server instance open an audio stream.
    """
    def get(self, request, format=None):
        """
        Accepts JSON:
        Parameters: url - audio stream or mp3 url
        Example:
        $ curl 'http://localhost:8000/server/play/?url=http://stream1.opb.org/radio.mp3'
        """
        url = request.query_params.get('url')
        platform = request.query_params.get('platform')
        if platform == 'youtube':
            import pafy
            url = pafy.new(url).getbestaudio().url
        player.set_mrl(url, ":no-video")
        player.play()
        return Response(status=status.HTTP_200_OK)

class Pause(APIView):
    def get(self, request, format=None):
        player.pause()
        return Response(status=status.HTTP_200_OK)

class Stop(APIView):
    """
    Instruct the server instance to stop the playing audio stream.
    """
    def get(self, request, format=None):
        """
        Example: 
        $ curl http://localhost:8000/server/stop/
        """
        player.stop()
        return Response(status=status.HTTP_200_OK)

class Status(APIView):
    def get(self, request, format=None):
        pos = player.get_position()
        return Response(data=pos,status=status.HTTP_200_OK)

class Search(APIView):
    def get(self, request, format=None):
        query = request.query_params.get('query')
        platform = request.query_params.get('platform')
        res = do_search(platform, query)
        return Response(data=res,status=status.HTTP_200_OK)

class Episodes(APIView):
    def get(self, request, format=None):
        url = request.query_params.get('url')
        res = get_episodes(url)
        return Response(data=res,status=status.HTTP_200_OK)
