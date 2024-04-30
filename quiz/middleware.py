import datetime
from django_ratelimit.core import get_usage, is_ratelimited
from graphql import GraphQLError

from django.http import HttpResponse
from functools import wraps
import os
import csv
from datetime import datetime
from django.conf import settings
import boto3
from botocore.exceptions import ClientError

def static_auth_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        username = request.GET.get('u')  # Example: Extract username from query parameters
        password = request.GET.get('p')  # Example: Extract password from query parameters
        
        # Perform static authentication check
        if username == 'Kappapply' and password == 'graphql@kapp':
            # Authentication successful, allow access to the view
            return view_func(request, *args, **kwargs)
        else:
            # Authentication failed, return HTTP 401 Unauthorized response
            return HttpResponse('Unauthorized', status=401)
    return wrapper

class GraphQLRateLimitMiddleware:
    def resolve(self, next, root, info, **args):
        # Define your rate limit settings
        rate = '10/m'
        key = 'ip'

        # Check if the request is ratelimited ratelimited for 10 requests per minute

        request = info.context
        if is_ratelimited(request, method='GET', rate=rate, key=key, increment=True):
            # Retrieve current usage and limit information
            usage = get_usage(request, method='GET', rate=rate, key=key)
            raise GraphQLError(f"Rate limit exceeded: {usage['count']} of {usage['limit']}")

        # Continue to the next resolver if not ratelimited
        return next(root, info, **args)


# class LogEntryMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         # Before the view (and later middleware) are called
#         response = self.get_response(request)
#         # After the view is called
#         return response

#     def process_view(self, request, view_func, view_args, view_kwargs):
#         ip = self.get_client_ip(request)
#         if request.user.is_authenticated:
#         # If the user is authenticated, get the user's details from Userkap
#             user = request.user
#             user_id = user.id
#         # You can now access any attribute of the Userkap model
#             email = user.email
#             username = user.username
#         # ... other fields as needed
#         else:
#             user = None
#             user_id = 1  # or 1, if you want to use a default value
#         action = "Visited"
#         description = f"Visited {request.path}"

#         # Check for recent activity from the same IP address
#          # last 1 hour
#         recent_activity = LogEntry1.objects.filter(
#             ip_address=ip
#         ).order_by('-created_at').first()

#         if recent_activity:
#             # Update existing record if found
#             recent_activity.description += f"; {description}"
#             if user:
#                 recent_activity.user = user  # Update user if authenticated
#             recent_activity.save()
#         else:
#             # Create a new record
#             LogEntry1.objects.create(
#                 # user=user,
#                 action=action,
#                 description=description,
#                 ip_address=ip,
#                 user_id = user_id 
#             )

#         return None
class LogEntryMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        self.log_to_s3(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        return None

    def log_to_s3(self, request):
        print("heloo")
        ip = self.get_client_ip(request)
        user = request.user if request.user.is_authenticated else None
        action = "Visited"
        description = f"Visited {request.path}"
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Create log data
        log_data = [timestamp, user.username if user else 'Anonymous', ip, action, description]
        print("he;llo before")
        # Connect to AWS S3
        s3 = boto3.client('s3', aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                          aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)

        # Define S3 path
        s3_folder_path = 'log/log'  # Folder path on S3
        s3_file_path = os.path.join(s3_folder_path, f"{datetime.now().strftime('%Y-%m-%d')}.csv")

        try:
            # Create S3 bucket if it does not exist
            s3.create_bucket(Bucket=settings.AWS_STORAGE_BUCKET_NAME)

            # Upload log file to S3
            with open('/tmp/log_entry.csv', 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(log_data)

            with open('/tmp/log_entry.csv', 'rb') as data:
                s3.upload_fileobj(data, settings.AWS_STORAGE_BUCKET_NAME, s3_file_path)

        except ClientError as e:
            # Handle bucket creation error
            if e.response['Error']['Code'] == 'BucketAlreadyOwnedByYou':
                # Bucket already exists and is owned by you
                pass
            else:
                # Unexpected error occurred
                print(f"Error: {e}")
                raise

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    @staticmethod
    def get_client_ip(request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip