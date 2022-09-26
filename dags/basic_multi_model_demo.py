from airflow import DAG
from airflow.operators.python_operator import PythonOperator, BranchPythonOperator
from airflow.api.client.local_client import Client
from airflow.models import TaskInstance

from modules.basic_modules import simple_const
from datetime import datetime, timedelta

import logging
import sys


default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2015, 6, 1),
    "retries": 1,
    "retry_delay": timedelta(seconds=5)
}


def subroutine_opera(self, **kwargs):
    logging.info('Initializing OPERA with ' + str(kwargs['dag_run'].conf['conf_val']))
    task_instance = kwargs['task_instance']
    task_instance.xcom_push(key='conf_key', value=kwargs['dag_run'].conf['conf_val'])

    return None


def subroutine_motor(self, **kwargs):
    logging.info('Initializing MOTOR with ' + str(kwargs['dag_run'].conf['conf_val']))
    task_instance = kwargs['task_instance']
    key_val = task_instance.xcom_pull(key='conf_key') + 1
    task_instance.xcom_push(key='conf_key', value=key_val)

    return None


def subroutine_regionalisation(self, **kwargs):
    logging.info('Initializing Regionalisation with ' + str(kwargs['dag_run'].conf['conf_val']))
    task_instance = kwargs['task_instance']
    key_val = task_instance.xcom_pull(key='conf_key') + 1
    task_instance.xcom_push(key='conf_key', value=key_val)

    return None


# Repeat DAG with new Config if value does not pass threshold
def subroutine_loadflow(self, **kwargs):
    logging.info('Initializing Load Flow with ' + str(kwargs['dag_run'].conf['conf_val']))
    task_instance = kwargs['task_instance']
    key_val = task_instance.xcom_pull(key='conf_key') + 1
    task_instance.xcom_push(key='conf_key', value=key_val)

    return None


# DAG Specification
dag = DAG('basic_multi_model',
          default_args=default_args,
          schedule_interval=None)


# Task Specification
t1 = PythonOperator(dag=dag,
                    task_id='OPERA',
                    python_callable=subroutine_opera,
                    op_args=['arguments_passed_to_callable'],
                    op_kwargs={'function_argument': 'which will be passed to function'})

t2 = PythonOperator(dag=dag,
                    task_id='MOTOR',
                    python_callable=subroutine_motor,
                    op_args=['arguments_passed_to_callable'],
                    op_kwargs={'keyword_argument': 'which will be passed to function'})

t3 = PythonOperator(dag=dag,
                    task_id='Regionalisation',
                    python_callable=subroutine_regionalisation,
                    op_args=['arguments_passed_to_callable'],
                    op_kwargs={'keyword_argument': 'which will be passed to function'})

t4 = PythonOperator(dag=dag,
                    task_id='LoadFlowModel',
                    python_callable=subroutine_loadflow,
                    op_args=['arguments_passed_to_callable'],
                    op_kwargs={'keyword_argument': 'which will be passed to function'})


# DAG Structure
t2.set_upstream(t1)
t3.set_upstream(t2)
t4.set_upstream(t3)
