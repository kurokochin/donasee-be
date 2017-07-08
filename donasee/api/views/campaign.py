from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from donasee.api.serializers.campaign import CampaignSerializer, DonationSerializer
from donasee.api.serializers.user import UserProfileSerializer
from donasee.apps.accounts.models import UserProfile
from donasee.apps.campaign.models import Campaign


class CampaignListView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, format=None):
        campaigns = CampaignSerializer(Campaign.objects.all(), many=True).data
        datas = []
        for campaign in campaigns:
            user_profile = UserProfileSerializer(
                instance=UserProfile.objects.get(user=User.objects.get(id=campaign['user']))).data
            data = campaign
            data['community_name'] = user_profile['community_name']
            datas.append(data)
        return Response(datas)

    def post(self, request, format=None):
        ser = CampaignSerializer(data=request.data)
        if ser.is_valid():
            ser.save()
            data = ser.data
            data['community_name'] = UserProfileSerializer(
                instance=UserProfile.objects.get(user=User.objects.get(id=ser.data['user']))).data['community_name']
            return Response(data)
        return Response({'detail': ser.errors['non_field_errors'][0]}, status=status.HTTP_400_BAD_REQUEST)


class DonationList(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, form=None):
        ser = DonationSerializer(request.data)
        if ser.is_valid():
            return Response(ser.data)
        return Response({'detail': ser.errors}, status=status.HTTP_400_BAD_REQUEST)
