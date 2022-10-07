from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser

from vlc import MediaPlayer
player = MediaPlayer()

class Play(APIView):
    """
    Instruct the server instance open an audio stream.
    """
    def post(self, request, format=None):
        """
        Accepts JSON:
        Parameters: url - audio stream or mp3 url
        Example:
        $ curl -X POST http://localhost:8000/server/play/ \
            -d '{"url":"http://stream1.opb.org/radio.mp3"}'
        """
        url = JSONParser().parse(request).get('url')
        player.set_mrl(url)
        player.play()
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
