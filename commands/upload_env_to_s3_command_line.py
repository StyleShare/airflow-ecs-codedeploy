import os

import boto3
import click

import sys
import threading


class ProgressPercentage(object):

    def __init__(self, filename):
        self._filename = filename
        self._size = float(os.path.getsize(filename))
        self._seen_so_far = 0
        self._lock = threading.Lock()

    def __call__(self, bytes_amount):
        # To simplify, assume this is hooked up to a single filename
        with self._lock:
            self._seen_so_far += bytes_amount
            percentage = (self._seen_so_far / self._size) * 100
            sys.stdout.write(
                "\r%s  %s / %s  (%.2f%%)\n" % (
                    self._filename, self._seen_so_far, self._size,
                    percentage))
            sys.stdout.flush()


@click.command()
@click.option('--bucket_name', '-b', type=str)
@click.option('--key_name', '-k', type=str, default="")
@click.option('--region',
              type=click.Choice(['ap-northeast-2', 'ap-northeast-1'], case_sensitive=False), default="ap-northeast-2")
@click.argument('filename', type=click.Path(), default=".env")
def upload_env_to_s3_command_line(bucket_name, key_name, region, filename):
    """env file을 s3로 업로드합니다.

    :param bucket_name: s3 bucket 이름
    :param key_name: s3 key 이름
    :param region: AWS Region
    :param filename: 타깃 파일 이름
    """

    def _upload_keys(s3_bucket=bucket_name, s3_key=key_name, file_name=filename):
        os.environ['AWS_ACCESS_KEY_ID'] = aws_access_key_id
        os.environ['AWS_SECRET_ACCESS_KEY'] = aws_secret_access_key
        os.environ['AWS_DEFAULT_REGION'] = region
        s3 = boto3.resource('s3')
        s3.meta.client.upload_file(file_name,
                                   s3_bucket, f"{s3_key}/{filename}",
                                   ExtraArgs={'ServerSideEncryption': 'aws:kms',
                                              'SSEKMSKeyId': 'alias/aws/s3'},
                                   Callback=ProgressPercentage(filename=file_name))

    aws_access_key_id = click.prompt('AWS ACCESS KEY ID를 입력해주세요!', type=str, hide_input=True)
    aws_secret_access_key = click.prompt('AWS SECRET ACCESS KEY를 입력해주세요!', type=str, hide_input=True)

    _upload_keys()
    click.echo(f"s3://{bucket_name}/{key_name}/{filename}에 파일을 성공적으로 저장했습니다.")
    should_remove_file = click.prompt(f"남아있는 {filename} 파일을 지워도 될까요?", type=click.BOOL)
    if should_remove_file:
        os.remove(filename)


if __name__ == '__main__':
    upload_env_to_s3_command_line()
