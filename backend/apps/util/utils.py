import boto3
import logging
from pyfcm import FCMNotification
from boto3.exceptions import (
    ResourceLoadException,
    ResourceNotExistsError,
    RetriesExceededError,
)
from botocore.client import Config

from rest_framework.exceptions import NotFound

from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.conf import settings


def custom_get_object_or_404(Model, message='No', **kwargs):
    """ Returns 404 with custom message """
    try:
        return Model.objects.get(**kwargs)
    except Model.DoesNotExist:
        raise NotFound(detail=message)
    

def send_email(subject, recipient_email, from_email, text_template_path, html_template_path, merge_data):
    text_body = render_to_string(text_template_path, merge_data)
    html_body = render_to_string(html_template_path, merge_data)
    msg = EmailMultiAlternatives(
        subject=subject,
        body=text_body,
        from_email=from_email,
        to=recipient_email,
    )
    msg.attach_alternative(html_body, "text/html")
    msg.send()


def get_s3_url_for_key(key, session=None):
    try:
        if not session:
            session = boto3.Session(
                settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY)

        s3 = session.client('s3', config=Config(
            region_name=settings.AWS_REGION, signature_version='s3v4'))

        url = s3.generate_presigned_url(
            ClientMethod='get_object',
            Params={
                'Bucket': settings.AWS_S3_BUCKET_NAME,
                'Key': key
            }
        )
        return {
            "key": key,
            "url": url
        }
    except (ResourceNotExistsError, ResourceLoadException, RetriesExceededError):
        # TODO: logging here
        return


def get_s3_url(key):
    return get_s3_url_for_key(key).get('url', None)

def send_push_notification(registration_ids, title, message, deep_link=None):
    push_service = FCMNotification(api_key=settings.FCM_SERVER_KEY)
    
    data_message = {
        "title": title,
        "body": message,
    }

    if deep_link:
        data_message["link"] = deep_link

    result = push_service.notify_multiple_devices(
        registration_ids=registration_ids,
        data_message=data_message,
        message_title=title,
        message_body=message
    )
    
    return result

