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
                return serializers.ValidationError('User Profile hasn\'t been verified')
        except User.DoesNotExist:
            return serializers.ValidationError('User doesn\'t exist')
        except UserProfile.DoesNotExist:
            return serializers.ValidationError('User Profile doesn\' exist')

        try:
            if not attrs['title']:
                return serializers.ValidationError('Invalid title provided')
        except:
            return serializers.ValidationError('Invalid title provided')

        try:
            if not attrs['image']:
                return serializers.ValidationError('Invalid image link provided')
        except:
            return serializers.ValidationError('Invalid image link provided')

        try:
            if not attrs['money_needed']:
                return serializers.ValidationError('Invalid money needed provided')
        except:
            return serializers.ValidationError('Invalid money needed provided')

        try:
            if not attrs['description']:
                return serializers.ValidationError('Invalid description provided')
        except:
            return serializers.ValidationError('Invalid description provided')

        return attrs
