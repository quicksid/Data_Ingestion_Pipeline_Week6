import logging
import os
import subprocess
import yaml
import datetime
import gc
import re


def read_config_file(filepath):
  with open(filepath, 'r') as stream:
    try:
      return yaml.safe_load(stream)
    except yaml.YAMLError as exc:
      logging.error(exc)

def replacer(string, char):
  pattern = re.escape(char) + '{2,}'
  string = re.sub(pattern, char, string)
  return string

def col_header_val(df, config):
  df_columns = df.columns
  yaml_columns = config

  #print("Original Columns: ", df_columns)
  df_columns = df_columns.str.lower()
  #print("Lower cased Columns: ", df_columns)
  df_columns = df_columns.str.strip('_')
  #print("Stripped by _ Columns: ", df_columns)
  df_columns = list(df_columns)

  for i in range(len(df_columns)):
    df_columns[i] = replacer(df_columns[i], '_')
  #print("Replaced repeating characters: ", df_columns)
    df_columns[i] = re.sub('[$%^&*@!]', '', df_columns[i])
    df_columns[i] = df_columns[i].strip('_')
  #print(len(df_columns))

  expected_col = yaml_columns
  expected_col = list(expected_col)

  if len(df_columns) == len(expected_col) and expected_col == df_columns:
    print("column name and column length validation passed")
    return 1
  else:
    print("column name and column length validation failed")
    mismatched_columns_file = set(df_columns).difference(expected_col)
    print("Columns not in YAML files", mismatched_columns_file)
    mismatched_YAML_file = set(expected_col).difference(df_columns)
    print("Columns not in uploaded file", mismatched_YAML_file)
    logging.info(f'df columns: {df_columns}')
    logging.info(f'expected columns: {expected_col}')
    return 0
