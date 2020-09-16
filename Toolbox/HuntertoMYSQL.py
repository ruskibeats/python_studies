
import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine

import pymysql

sqlEngine = create_engine("mysql+pymysql://{user}:{pw}@209.97.133.232/{db}"
                          .format(user="russ",
                                  pw="skimmer69skimmer",
                                  db="linkedin",
                                  CHARSET='utf8mb4'))

df.to_sql(name='hunter', con=sqlEngine, if_exists='append', index=False)
