import pandas as pd
import requests
import numpy as np

## Based on: https://aws.amazon.com/blogs/machine-learning/use-the-built-in-amazon-sagemaker-random-cut-forest-algorithm-for-anomaly-detection/
## https://github.com/awslabs/amazon-sagemaker-examples/blob/master/introduction_to_amazon_algorithms/random_cut_forest/random_cut_forest.ipynb
## https://docs.aws.amazon.com/sagemaker/latest/dg/sagemaker-dg.pdf

# -------------------------------------------------- prepare data set -----------------------------------------------

data_filename = 'nyc_taxi.csv'
data_source = 'https://raw.githubusercontent.com/numenta/NAB/master/data/realKnownCause/nyc_taxi.csv'
taxi_data = pd.read_csv(data_source, delimiter=',')

shingle_size = 48

def shingle(data, shingle_size=shingle_size):
    import numpy as np
    num_data = len(data)
    shingled_data = np.zeros((num_data - shingle_size, shingle_size))

    for n in range(num_data - shingle_size):
        shingled_data[n] = data[n:(n + shingle_size)].reshape((1,shingle_size,))
    return shingled_data


def convert_and_upload_training_data(
    ndarray, bucket, prefix, filename='data.pbr'):
    import boto3
    import os
    from sagemaker.amazon.common import numpy_to_record_serializer

    # convert Numpy array to Protobuf RecordIO format
    serializer = numpy_to_record_serializer()
    data = shingle(ndarray)
    buffer = serializer( data.astype(np.int32))

    # upload to S3
    s3_object = os.path.join(prefix, 'train', filename)
    boto3.Session().resource('s3').Bucket(bucket).Object(s3_object).upload_fileobj(buffer)
    s3_path = 's3://{}/{}'.format(bucket, s3_object)
    return s3_path

bucket = 'aws-rcf-testbucket' # <-- use your own bucket, here
prefix = 'sagemaker/randomcutforest'
s3_train_data = convert_and_upload_training_data(
    taxi_data.value.as_matrix().reshape(-1,1),
    bucket,
    prefix)

# --------------------------------------- train random cut forrest -------------------------------------------------

import boto3
import sagemaker

containers = {
    'us-west-2': '174872318107.dkr.ecr.us-west-2.amazonaws.com/randomcutforest:latest'}
region_name = boto3.Session().region_name
container = containers[region_name]

session = sagemaker.Session()

role = 'aws-sagemaker-full-permission'

rcf = sagemaker.estimator.Estimator(
    container,
    role,
    output_path='s3://{}/{}/output'.format(bucket, prefix),
    train_instance_count=1,
    train_instance_type='ml.m4.xlarge',
    sagemaker_session=session)

rcf.set_hyperparameters(
    num_samples_per_tree=200,
    num_trees=50,
    feature_dim=48)

s3_train_input = sagemaker.session.s3_input(
    s3_train_data,
    distribution='ShardedByS3Key',
    content_type='application/x-recordio-protobuf')

rcf.fit({'train': s3_train_input})

# --------------------------------------- deploy trained model -------------------------------------------------


from sagemaker.predictor import csv_serializer, json_deserializer

rcf_inference = rcf.deploy(
    initial_instance_count=1,
    instance_type='ml.m4.xlarge',
)

rcf_inference.content_type = 'text/csv'
rcf_inference.serializer = csv_serializer
rcf_inference.deserializer = json_deserializer


# --------------------------------------- test model on same data -------------------------------------------------

data = shingle(taxi_data.value.as_matrix().reshape(-1,1).astype(np.int32))

results = rcf_inference.predict(data)

scores = [datum['score'] for datum in results['scores']]
if(len(scores) < taxi_data.shape[0]):
    tmp = np.ones((taxi_data.shape[0]))
    tmp = tmp*np.nan
    tmp[0:len(scores)] = scores
    scores = tmp

taxi_data['score'] = scores

score_mean = taxi_data.score.mean()
score_std = taxi_data.score.std()

score_cutoff = score_mean + 3*score_std
anomalies = taxi_data[taxi_data['score'] > score_cutoff]

import matplotlib.pyplot as plt

fig, ax1 = plt.subplots()
ax2 = ax1.twinx()

ax1.plot(taxi_data['value'], alpha=0.8)
ax1.set_ylabel('Taxi Ridership', color='C0')
ax1.tick_params('y', colors='C0')

ax2.plot(taxi_data['score'], color='C1')
ax2.plot(anomalies.index, anomalies.score, 'ko')
ax2.set_ylabel('Anomaly Score', color='C1')
ax2.tick_params('y', colors='C1')

fig.suptitle('Taxi Ridership in NYC')
plt.show()

# -------------------------------------- clean up: destroy deployment / endpoint--------------------------------------

sagemaker.Session().delete_endpoint(rcf_inference.endpoint)
