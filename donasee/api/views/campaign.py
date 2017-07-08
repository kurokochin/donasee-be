from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from donasee.api.serializers.campaign import CampaignSerializer
from donasee.apps.campaign.models import Campaign


class CampaignListView(APIView):
    def get(self):
        return Response(CampaignSerializer(Campaign.objects.all(), many=True).data)

    def post(self, request, format=None):
        ser = CampaignSerializer(data=request.data)
        if ser.is_valid():
            ser.save()
            return Response(ser.data)
        return Response({'detail': 'Some fields are not valid'}, status=status.HTTP_400_BAD_REQUEST)
