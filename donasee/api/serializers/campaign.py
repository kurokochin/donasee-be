from django.contrib.auth.models import User
from rest_framework import serializers

from donasee.apps.accounts.models import UserProfile
from donasee.apps.campaign.models import Campaign, Donation


class DonationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donation
        fields = '__all__'


class CampaignSerializer(serializers.ModelSerializer):
    donations = DonationSerializer(many=True, required=False)

    class Meta:
        model = Campaign
        fields = '__all__'

    def validate(self, attrs):
        try:
            user = User.objects.get(id=attrs['user'].id)
            user_profile = UserProfile.objects.get(user=user)
            if user_profile.status == 'pending':
                raise serializers.ValidationError('User Profile hasn\'t been verified')
        except User.DoesNotExist:
            raise serializers.ValidationError('User doesn\'t exist')
        except UserProfile.DoesNotExist:
            raise serializers.ValidationError('User Profile doesn\' exist')

        if not attrs['title']:
            raise serializers.ValidationError('Invalid title provided')

        if not attrs['image']:
            raise serializers.ValidationError('Invalid image link provided')

        if not attrs['money_needed']:
            raise serializers.ValidationError('Invalid money needed provided')

        if not attrs['description']:
            raise serializers.ValidationError('Invalid description provided')

        return attrs
