
import pandas as pd
import requests
import sqlalchemy
from sqlalchemy import create_engine
import pprint
import pymysql
sqlEngine = create_engine("mysql+pymysql://{user}:{pw}@209.97.133.232/{db}"
                          .format(user="russ",
                                  pw="skimmer69skimmer",
                                  db="linkedin",
                                  CHARSET='utf8mb4'), pool_pre_ping=True)

# """ API KEY """
# https: // api.hunter.io/v2/domain-search?domain = stripe.com & api_key = f68a4cb3f9c2ec8fac1bedd2ab9df424760404e3

contents = requests.get("https://api.hunter.io/v2/domain-search?domain=stripe.com&api_key=f68a4cb3f9c2ec8fac1bedd2ab9df424760404e3").json()
data = []
for email in contents['data']['emails']:
        for source in email['sources']:
                metadata = contents['data'].copy()
                del metadata['emails']
                metadata['data_domain'] = metadata['domain']
                del metadata['domain']
                record = email.copy()
                del record['value']
                del record['sources']
                del record['verification']
                record['email'] = email['value']
                record.update(source)
                record.update(metadata)
                data.append(record)
df = pd.DataFrame(data)
df.to_sql(name='hunter', con=sqlEngine, if_exists='append', index=False)
