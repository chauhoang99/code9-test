import json
from shapely.geometry import Polygon
import geopandas as gpd
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings
from rest_framework import permissions, generics

from .serializers import *
from .models import *

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class SignupViews(generics.CreateAPIView):
    '''
    username
    email
    password
    '''

    model = User
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserSerializer


class LoginViews(generics.GenericAPIView):
    '''
    username
    password
    '''

    authentication_classes = [BasicAuthentication]
    permission_classes = [AllowAny]
    serializer_class = LogInSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.authenticate()
        if user:
            payload = jwt_payload_handler(user)
            token = jwt_encode_handler(payload)
            return_data = {'token': token}
            return Response(return_data)
        else:
            raise exceptions.ValidationError({'authentication': 'Username / password mismatched.'})


class ShapeViews(generics.GenericAPIView):
    permissions = [IsAuthenticated,]
    serializer_class = ShapeSerializer

    def post(self, request):
        '''
        coords: list of all coordiates (list of x and y, i.e. [x, y]) of a shape on an Euclidean plane
        '''
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        new_shape = Shape(
            coords=json.dumps(validated_data.get('coords'))
        )
        new_shape.save()
        return Response({'id': new_shape.pk})

    def get(self, request):
        pk = request.GET.get('id')
        if not pk:
            raise exceptions.ValidationError({'id': 'This param is mandatory'})
        shape = Shape.objects.filter(pk=pk)
        if not shape:
            raise exceptions.ValidationError({'id': 'Id is not available in database'})
        coords = json.loads(shape[0].coords)
        res = {'coords': coords}
        if request.GET.get('getArea'):
            area = self.get_area(coords)
            res['area'] = area
        if request.GET.get('getPerimeter'):
            perimeter = self.get_perimeter(coords)
            res['perimeter'] = perimeter
        return Response(res)

    def get_area(self, coords):
        polygon = Polygon(coords)
        p = gpd.GeoSeries(polygon)
        return p.area[0]

    def get_perimeter(self, coords):
        polygon = Polygon(coords)
        p = gpd.GeoSeries(polygon)
        return p.length[0]

    def put(self, request):
        pk = request.query_params.get('id')
        if not pk:
            raise exceptions.ValidationError({'id': 'This param is mandatory'})
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        shape = Shape.objects.filter(pk=pk)
        if not shape:
            raise exceptions.ValidationError({'id': 'Id is not available in database'})
        else:
            shape.update(coords=validated_data.get('coords'))
        return Response({'id': shape[0].pk})

    def delete(self, request):
        pk = request.query_params.get('id')
        if not pk:
            raise exceptions.ValidationError({'id': 'This param is mandatory'})
        shape = Shape.objects.filter(pk=pk)
        if not shape:
            raise exceptions.ValidationError({'id': 'Id is not available in database'})
        else:
            shape.delete()
        return Response({'id': pk, 'deleted': True})
