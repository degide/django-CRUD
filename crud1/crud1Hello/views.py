from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Account
from .serializers import AccountSerializer
import uuid
from .utils.jwtUtils import create_token, decode_token


# Views

@api_view(['GET'])
def all_accounts(request):
    accounts = Account.objects.all()
    serializer = AccountSerializer(accounts, many=True)
    return Response({
        "success": True,
        "data": serializer.data,
        "message": "Account created"
    })


@api_view(['POST'])
def create_account(request):
    req_body_dict = request.data
    try:
        with_same_email = Account.objects.get(email=req_body_dict["email"])
        return Response({
            "success": False,
            "message": "Email already taken"
        })
    except:
        new_account = Account(
            unique_id=uuid.uuid1(),
            first_name=req_body_dict["fname"],
            last_name=req_body_dict["lname"],
            email=req_body_dict["email"],
            phone=req_body_dict["phone"]
        )
        new_account.save()
        return Response({
            "success": True,
            "data": new_account.to_dict(),
            "message": "Account created"
        })


@api_view(["DELETE"])
def delete_account(request):
    try:
        account = Account.objects.get(unique_id=request.data["unique_id"])
        deleted_account = account.delete()
        print(account)
        return Response({
            "success": True,
            "data": deleted_account,
            "message": "Account deleted"
        })
    except:
        return Response({
            "success": False,
            "message": "Something is Wrong Or Account Doesn't exist"
        })


@api_view(['PUT'])
def update_account(request):
    try:
        req_body_dict = request.data
        account = Account.objects.get(unique_id=request.data["unique_id"])
        account.email = req_body_dict["email"]
        account.phone = req_body_dict["phone"]
        account.first_name = req_body_dict["fname"]
        account.last_name = req_body_dict["lname"]
        account.save()
        return Response({
            "success": True,
            "data": account.to_dict(),
            "message": "Account updated"
        })
    except:
        return Response({
            "success": False,
            "message": "Something is Wrong Or Account Doesn't exist"
        })


@api_view(['GET'])
def account_by_unique_id(request):
    try:
        account = Account.objects.get(unique_id=request.query_params["unique_id"])
        return Response({
            "success": True,
            "data": AccountSerializer(account).data,
            "message": "Request successful"
        })
    except:
        return Response({
            "success": False,
            "message": "Something is Wrong Or Account Doesn't exist"
        })


@api_view(['POST'])
def account_login(request):
    try:
        account = Account.objects.get(email=request.data["email"], phone=request.data["phone"])
        return Response({
            "success": True,
            "data": {
                "token": create_token({"unique_id": AccountSerializer(account).data["unique_id"]}),
                "account": AccountSerializer(account).data
            },
            "message": "Login successful"
        })
    except:
        return Response({
            "success": False,
            "message": "Invalid Email or Phone"
        })


@api_view(['POST'])
def verify_token(request):
    try:
        decoded = decode_token(request.data["token"])
    except:
        return Response({
            "success": False,
            "message": "Unauthorized!"
        })
    if decoded["unique_id"]:
        try:
            account = Account.objects.get(unique_id=decoded["unique_id"])
            return Response({
                "success": True,
                "data": AccountSerializer(account).data,
                "message": "Token Is Valid"
            })
        except:
            return Response({
                "success": False,
                "message": "Something is Wrong Or Account Doesn't exist"
            })
    else:
        return Response({
            "success": False,
            "message": "Unauthorized!"
        })