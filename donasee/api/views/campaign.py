from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from donasee.api.serializers.campaign import CampaignSerializer
from donasee.apps.campaign.models import Campaign


class CampaignListView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, format=None):
        return Response(CampaignSerializer(Campaign.objects.all(), many=True).data)

    def post(self, request, format=None):
        ser = CampaignSerializer(data=request.data)
        if ser.is_valid():
            ser.save()
            return Response(ser.data)
        print(ser.errors)
        return Response({'detail': ser.errors['non_field_errors'][0]}, status=status.HTTP_400_BAD_REQUEST)
