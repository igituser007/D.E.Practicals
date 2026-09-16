Practical 06 - Setting Up Apache Airflow and Creating a DAG
=============================================================

OBJECTIVE
---------
Configure a Directed Acyclic Graph (DAG) in Apache Airflow to run daily,
executing sequential dependency tasks: a start notifier, an extraction
script, and a pipeline success logger.

SOFTWARE / LIBRARIES REQUIRED
------------------------------
- Python 3
- apache-airflow==2.9.3 (installed in an isolated virtual environment,
  airflow_venv, so it doesn't conflict with system Python packages)

FILE TO RUN
-----------
practical_06_dag.py  (place in your Airflow DAGs folder, e.g. ~/airflow/dags/)

SETUP + HOW THIS WAS ACTUALLY RUN
-----------------------------------
1. python3 -m venv airflow_venv
2. airflow_venv/bin/pip install apache-airflow==2.9.3
3. export AIRFLOW_HOME=<this folder>/airflow_home
4. airflow_venv/bin/airflow db migrate         (creates the metadata DB)
5. Copy practical_06_dag.py into $AIRFLOW_HOME/dags/
6. airflow_venv/bin/airflow tasks test university_etl_orchestration <task_id> 2026-01-01
   run once per task, in order:
     - start_pipeline
     - run_extraction_script
     - log_pipeline_success

`airflow tasks test` runs a single task instance directly, which is the
standard lightweight way to test a DAG's task logic without needing the
full scheduler + webserver running (those need long-lived background
processes, which don't fit a one-shot script run).

WHAT THE CODE DOES
-------------------
Defines one DAG (university_etl_orchestration) with 3 tasks that run in
sequence: start_pipeline (EmptyOperator) -> run_extraction_script
(BashOperator) -> log_pipeline_success (BashOperator). The DAG is set to
run daily (schedule_interval=timedelta(days=1)).

One small fix from the original: the extraction task originally called
`python3 /absolute/path/to/data_extraction.py`, which is a placeholder path
that doesn't exist. It was replaced with a simple echo command so the task
can actually run in this environment; point it back at your real
data_extraction.py path (e.g. the one from Practical 05) when running
this in a real Airflow install.

OUTPUT
------
- output/console_output.txt          : full raw log from all three
  `airflow tasks test` runs (actual, executed - this really ran).
- output/console_output_summary.txt  : the same log filtered down to just
  the key "Executing" / "Running command" / "Marking task as SUCCESS"
  lines, for quick reading.

All three tasks show "Marking task as SUCCESS" in the log.
