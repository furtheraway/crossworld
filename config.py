# Copyright 2015 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
This file contains all of the configuration values for the application.
Update this file with the values for your specific Google Cloud project.
You can create and manage projects at https://console.developers.google.com
"""

# The secret key is used by Flask to encrypt session cookies.
SECRET_KEY = '\x05\x11\xb4\x02\xfc\xe04\x9c\x05\xc0\xbb|\xac1\xbe\xd3Q\x9e!\x125T\xfd\xeb'

# There are three different ways to store the data in the application.
# You can choose 'datastore', 'cloudsql', or 'mongodb'. Be sure to
# configure the respective settings for the one you choose below.
# You do not have to configure the other data backends. If unsure, choose
# 'datastore' as it does not require any additional configuration.
DATA_BACKEND = 'cloudsql'

# Google Cloud Project ID. This can be found on the 'Overview' page at
# https://console.developers.google.com
PROJECT_ID = 'crossworldsbu1'

# Cloud Datastore dataset id, this is the same as your project id.
DATASTORE_DATASET_ID = PROJECT_ID

# SQLAlchemy configuration
# Replace user, pass, host, and database with the respective values of your
# Cloud SQL instance.
SQLALCHEMY_DATABASE_URI = \
    'mysql+pymysql://yuan:cross@173.194.226.174/library'
    # 'mysql+pymysql://yuan:cross@2001:4860:4864:1:c3e8:626a:4e6:395e/library'

# Mongo configuration
# If using mongolab, the connection URI is available from the mongolab control
# panel. If self-hosting on compute engine, replace the values below.
MONGO_URI = \
    'mongodb://user:password@host:27017/database'


# OAuth2 configuration.
# This can be generated from the Google Developers Console at
# https://console.developers.google.com/project/_/apiui/credential.
# Note that you will need to add all URLs that your application uses as
# authorized redirect URIs. For example, typically you would add the following:
#
#  * http://localhost:8080/oauth2callback
#  * https://<your-app-id>.appspot.com/oauth2callback.
#
# If you receive a invalid redirect URI error review you settings to ensure
# that the current URI is allowed.
GOOGLE_OAUTH2_CLIENT_ID = \
    '284510608032-g6l90vf5u542heknfot6kvdp776qgcba.apps.googleusercontent.com'
GOOGLE_OAUTH2_CLIENT_SECRET = 'snbp1YLEIqW4HYc2OjzjdW0O'
