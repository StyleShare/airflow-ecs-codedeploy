import os

import boto3
import click


@click.command()
@click.option('--bucket_name', '-b', type=str)
@click.option('--key_name', '-k', type=str, default="")
@click.option('--region',
              type=click.Choice(['ap-northeast-2', 'ap-northeast-1'], case_sensitive=False), default="ap-northeast-2")
@click.argument('filename', type=click.Path(), default=".env")
def load_env_file_from_s3_command_line(bucket_name, key_name, region, filename):
    def _read_env_file_from_s3():
        os.environ['AWS_ACCESS_KEY_ID'] = aws_access_key_id
        os.environ['AWS_SECRET_ACCESS_KEY'] = aws_secret_access_key
        os.environ['AWS_DEFAULT_REGION'] = region
        s3 = boto3.client('s3')
        obj = s3.get_object(Bucket=bucket_name, Key=f"{key_name}/{filename}")
        return obj['Body'].read().decode('utf-8')

    aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID', None)
    if aws_access_key_id is None:
        aws_access_key_id = click.prompt('AWS ACCESS KEY ID를 입력해주세요!', type=str, hide_input=True)

    aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY', None)
    if aws_secret_access_key is None:
        aws_secret_access_key = click.prompt('AWS SECRET ACCESS KEY를 입력해주세요!', type=str, hide_input=True)

    env_file_body = _read_env_file_from_s3()
    click.echo(' '.join(env_file_body.splitlines()))


if __name__ == '__main__':
    load_env_file_from_s3_command_line()
