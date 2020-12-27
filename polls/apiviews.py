from django.core.exceptions import PermissionDenied
from django.views import generic
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import generics, status, viewsets
from django.contrib.auth import authenticate

from .models import Poll, Choice, Vote
from .serializers import PollSerializer, ChoiceSerializer, UserSerializer, VoteSerializer

# option 1
# class PollList(APIView):
#     def get(self, request):
#         polls = Poll.objects.all()[:20]
#         data = PollSerializer(polls, many=True).data
#         return Response(data)

# class PollDetail(APIView):
#     def get(self, request, pk):
#         poll = get_object_or_404(Poll, pk=pk)
#         data = PollSerializer(poll).data
#         return Response(data)


# # option 2
# class PollList(generics.ListCreateAPIView):
#     queryset = Poll.objects.all()
#     serializer_class = PollSerializer

# class PollDetail(generics.RetrieveDestroyAPIView):
#     queryset = Poll.objects.all()
#     serializer_class = PollSerializer

# option 3 using viewset

class PollViewSet(viewsets.ModelViewSet):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer

    # poll can be only deleted by the creator
    def destroy(self, request, *args, **kwargs):
        poll = Poll.objects.get(pk=self.kwargs['pk'])
        print(poll.created_by)
        print(request.user)
        if poll:
            if not request.user == poll.created_by:
                print("I am not allowed")
                raise PermissionDenied('You can only delete poll you craeted')
            return super().destroy(request, *args, **kwargs)        
# /choices/
# class ChoiceList(generics.ListCreateAPIView):
#     queryset = Choice.objects.all()
#     serializer_class = ChoiceSerializer

# /polls/<pk>/choices/
class ChoiceList(generics.ListCreateAPIView):
    def get_queryset(self):
        # print(self.kwargs["pk"])
        queryset = Choice.objects.filter(poll_id=self.kwargs['id'])
        return queryset
    serializer_class = ChoiceSerializer

    def post(self, request, *args, **kwargs):
        poll = Poll.objects.get(pk=self.kwargs['pk'])
        if not request.user == poll.created_by:
            raise PermissionDenied('you cannot create choice for poll')
        return super().post(request, *args, **kwargs)

# [POST] /vote/
# class CreateVote(generics.CreateAPIView):
#     serializer_class = VoteSerializer

# [POST] /polls/<pk>/choices/<choice_pk>/vote/
class CreateVote(APIView):
    # serializer_class = VoteSerializer
    
    def post(self, request, poll_pk, choice_pk):
        voted_by = request.data.get("voted_by")
        data = {"choice": choice_pk, "poll": poll_pk, "voted_by": voted_by}
        serializer = VoteSerializer(data=data)
        if serializer.is_valid():
            vote = serializer.save()
            return Response(serializer.data, status= status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

# [POST] /users/
class UserCreate(generics.CreateAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = UserSerializer

class LoginView(APIView):
    permission_classes = ()
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        print(username, password)
        user = authenticate(username=username, password=password)
        print(user)
        if user:
            return Response({
                "token": user.auth_token.key
            })
        else:
            return Response({
                "error": "Wrong Credential"
            }, status = status.HTTP_401_UNAUTHORIZED)