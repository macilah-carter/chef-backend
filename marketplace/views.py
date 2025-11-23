from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied, ValidationError
from .models import Chef, Menus, Booking
from .serializers import ChefSerializer, MenusSerializer, BookingSerializer


from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound

class ChefViewSet(ModelViewSet):
    queryset = Chef.objects.select_related('user').all()
    serializer_class = ChefSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['specialties', 'location', 'availability']

    def perform_create(self, serializer):
        if self.request.user.role != 'chef':
            raise PermissionDenied("Only chef users can create a chef profile.")

        if hasattr(self.request.user, 'chef_profile'):
            raise ValidationError("You already have a chef profile.")

        serializer.save(user=self.request.user)

    # ✨ ADD THIS
    @action(detail=False, methods=['get'], url_path='me')
    def me(self, request):
        """Return the chef profile of the logged-in user."""
        user = request.user

        # Check if this user has a chef profile
        try:
            chef = user.chef_profile  # reverse OneToOne lookup
        except Chef.DoesNotExist:
            raise NotFound("You do not have a chef profile.")

        serializer = self.get_serializer(chef)
        return Response(serializer.data, status=status.HTTP_200_OK)



class MenusViewSet(ModelViewSet):
    serializer_class = MenusSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['chef', 'price']

    def get_queryset(self):
        queryset = Menus.objects.select_related('chef__user').all()
        chef_id = self.kwargs.get('chef_pk')
        if chef_id:
            queryset = queryset.filter(chef__id=chef_id)
        return queryset

    def perform_create(self, serializer):
        chef_id = self.kwargs.get('chef_pk')
        if not chef_id:
            raise ValidationError("Chef ID is required to create a menu.")

        chef = Chef.objects.get(id=chef_id)

        # Make sure only the chef who owns the profile can add menus
        if chef.user != self.request.user:
            raise PermissionDenied("You can only add menus to your own chef profile.")

        serializer.save(chef=chef)


class BookingViewSet(ModelViewSet):
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['chef__id', 'client__id', 'status', 'event_date']

    def get_queryset(self):
        queryset = Booking.objects.select_related('chef__user', 'client').all()
        chef_id = self.kwargs.get('chef_pk')
        if chef_id:
            queryset = queryset.filter(chef__id=chef_id)
        return queryset

    def perform_create(self, serializer):
        chef_id = self.kwargs.get('chef_pk')
        if not chef_id:
            raise ValidationError("Chef ID is required to create a booking.")

        chef = Chef.objects.get(id=chef_id)

        # Prevent chefs from booking themselves
        if chef.user == self.request.user:
            raise PermissionDenied("You cannot book yourself.")

        serializer.save(client=self.request.user, chef=chef)
