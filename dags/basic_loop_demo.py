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


# Read value from JSON config and write to XCOM
def subroutine_read(self, **kwargs):
    logging.info('Initializing DAG with ' + str(kwargs['dag_run'].conf['conf_val']))
    task_instance = kwargs['task_instance']
    task_instance.xcom_push(key='conf_key', value=kwargs['dag_run'].conf['conf_val'])

    return None


# Read value from XCOM, increment and write back to XCOM
def subroutine_increment(self, **kwargs):
    task_instance = kwargs['task_instance']
    key_val = task_instance.xcom_pull(key='conf_key') + 1
    task_instance.xcom_push(key='conf_key', value=key_val)

    return None


# Test if value passes certain threshold
def subroutine_test(self, **kwargs):
    task_instance = kwargs['task_instance']
    key_val = task_instance.xcom_pull(key='conf_key')
    threshold_val = kwargs['dag_run'].conf['threshold']

    if key_val > threshold_val:
        return 'End'
    else:
        return 'Repeat'


# Repeat DAG with new Config if value does not pass threshold
def subroutine_repeat(self, **kwargs):
    task_instance = kwargs['task_instance']
    key_val = task_instance.xcom_pull(key='conf_key')
    t_val = kwargs['dag_run'].conf['threshold']
    logging.info('Value is ' + str(key_val) + ' so we repeat')

    # Connect to Airflow API to trigger new dag, we use run_id none to auto-generate a new ID
    c = Client(None, None)
    c.trigger_dag(dag_id='basic_loop', run_id=None, conf={"conf_val":key_val,"threshold":t_val})

    return None


# Terminate DAG if value passes threshold
def subroutine_end(self, **kwargs):
    task_instance = kwargs['task_instance']
    key_val = task_instance.xcom_pull(key='conf_key')
    logging.info('Value is ' + str(key_val) + ' so we end')
    return None


# DAG Specification
dag = DAG('basic_loop',
          default_args=default_args,
          schedule_interval=None)


# Task Specification
t1 = PythonOperator(dag=dag,
                    task_id='Read',
                    python_callable=subroutine_read,
                    op_args=['arguments_passed_to_callable'],
                    op_kwargs={'function_argument': 'which will be passed to function'})

t2 = PythonOperator(dag=dag,
                    task_id='Increment',
                    python_callable=subroutine_increment,
                    op_args=['arguments_passed_to_callable'],
                    op_kwargs={'keyword_argument': 'which will be passed to function'})

t3 = BranchPythonOperator(dag=dag,
                    task_id='Test',
                    python_callable=subroutine_test,
                    op_args=['arguments_passed_to_callable'],
                    op_kwargs={'keyword_argument': 'which will be passed to function'})

t4 = PythonOperator(dag=dag,
                    task_id='Repeat', #trigger dag op
                    python_callable=subroutine_repeat,
                    op_args=['arguments_passed_to_callable'],
                    op_kwargs={'keyword_argument': 'which will be passed to function'})

t5 = PythonOperator(dag=dag,
                    task_id='End', #terminal op
                    python_callable=subroutine_end,
                    op_args=['arguments_passed_to_callable'],
                    op_kwargs={'keyword_argument': 'which will be passed to function'})


# DAG Structure
t2.set_upstream(t1)
t3.set_upstream(t2)
t4.set_upstream(t3)
t5.set_upstream(t3)
