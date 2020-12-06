import os
from typing import List, Tuple

import click

default_local_env = [
    ('AIRFLOW__CORE__EXECUTOR', 'CeleryExecutor'),
    ('AIRFLOW__CORE__SQL_ALCHEMY_CONN', 'postgresql+psycopg2://airflow:airflow@postgres/airflow'),
    ('AIRFLOW__FERNET_KEY', '46BKJoQYlPPOexq0OhDZnIlNepKFf87WFwLbfzqDDho'),
    ('AIRFLOW__CORE__LOAD_EXAMPLES', False),
    ('AIRFLOW__CELERY__BROKER_URL', 'redis://:redispass@redis:6379/0'),
    ('AIRFLOW__CELERY__RESULT_BACKEND', 'db+postgresql://airflow:airflow@postgres:5432/airflow')
]


@click.command()
@click.option('--entry', nargs=2, type=click.Tuple([str, str]), multiple=True, default=default_local_env)
@click.argument('filename', type=click.Path(), default=".env")
def write_env_file_command_line(entry, filename) -> None:
    """dotenv 파일을 생성합니다.

    :param entry: key-value 페어 entry
    :param filename: 타깃 파일 이름
    """

    def _write_env_file(key_value_pairs: List[Tuple[str, str]], filepath: str = filename):
        with open(file=filepath, mode='w') as f:
            for k, v in key_value_pairs:
                f.write(f"{k}={v}{os.linesep}")

    # TODO: add additional entries prompt
    # click.echo('현재 Env 목록입니다!')
    # for k, v in list(entry):
    #     print(f"{k}={v}")
    #
    # should_add_entry = True
    # while should_add_entry:
    #     print(list(entry))
    #     next_pair = click.prompt('추가할 Key, Value를 입력해주세요 (e.g., HELLO WORLD -> HELLO=WORLD)',
    #                              type=(str, str))
    #     entry = entry + next_pair
    #     should_add_entry = click.prompt('추가할 Key-Value 페어가 있을까요?', type=click.BOOL)

    _write_env_file(key_value_pairs=list(entry))


if __name__ == '__main__':
    write_env_file_command_line()
