from django.contrib.auth.models import User
from rest_framework import serializers

from donasee.apps.accounts.models import UserProfile
from donasee.apps.campaign.models import Campaign, Donation


class CampaignSerializer(serializers.ModelSerializer):
    donations = DonationSerializer(many=True)

    class Meta:
        model = Campaign
        fields = '__all__'

    def validate(self, attrs):
        try:
            user = User.objects.get(id=attrs['user'])
            user_profile = UserProfile.objects.get(user=user)
            if user_profile.status == 'pending':
                return serializers.ValidationError('User Profile hasn\'t been verified')
        except User.DoesNotExist:
            return serializers.ValidationError('User doesn\'t exist')
        except UserProfile.DoesNotExist:
            return serializers.ValidationError('User Profile doesn\' exist')

        return super(CampaignSerializer, self).run_validation(data=attrs)


class DonationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donation
        fields = '__all__'
