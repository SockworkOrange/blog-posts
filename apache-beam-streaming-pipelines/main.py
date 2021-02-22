import argparse
import apache_beam as beam
from apache_beam import window
from apache_beam.options.pipeline_options import PipelineOptions, StandardOptions

from datetime import datetime
import json

def run(argv=None, save_main_session=True):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--subscription',
        dest='subscription',
        default='projects/ilan-uzan/subscriptions/test',
        help='Input Pub/Sub subscription')

    parser.add_argument(
        '--table_spec ',
        dest='table_spec',
        default='ilan-uzan:test.count_and_mean',
        help='Destination BigQuery table.')

    known_args, pipeline_args = parser.parse_known_args(argv)
    pipeline_options = PipelineOptions(pipeline_args)
    pipeline_options.view_as(StandardOptions).streaming = True

    def within_limit(x, limit):
        return x['duration'] <= limit

    class CountAndMeanFn(beam.CombineFn):
        def create_accumulator(self):
            return 0.0, 0

        def add_input(self, sum_count, input):
            (sum, count) = sum_count
            return sum + input['duration'], count + 1

        def merge_accumulators(self, accumulators):
            sums, counts = zip(*accumulators)
            return sum(sums), sum(counts)

        def extract_output(self, sum_count):
            (sum, count) = sum_count

            return {
                'processing_time': datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                'count': count,
                'mean': sum / count if count else float('NaN')
            }

    with beam.Pipeline(options=pipeline_options) as p:
        table_schema = {
            'fields': [
                {'name': 'processing_time', 'type': 'TIMESTAMP', 'mode': 'NULLABLE'}, 
                {'name': 'count', 'type': 'FLOAT', 'mode': 'NULLABLE'},
                {'name': 'mean', 'type': 'FLOAT', 'mode': 'NULLABLE'}
            ]
        }

        (p
            | 'Read from pubsub' >> beam.io.ReadFromPubSub(subscription=known_args.subscription)
            | 'To Json' >> beam.Map(lambda e: json.loads(e.decode('utf-8')))
            | 'Filter' >> beam.Filter(within_limit, 100)
            | 'Window' >> beam.WindowInto(window.FixedWindows(60))
            | 'Calculate Metrics' >> beam.CombineGlobally(CountAndMeanFn()).without_defaults()
            | 'Write to BigQuery' >> beam.io.WriteToBigQuery(
                        known_args.table_spec,
                        schema=table_schema,
                        method=beam.io.WriteToBigQuery.Method.FILE_LOADS,
                        triggering_frequency=1,
                        write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND,
                        create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED))

    
if __name__ == '__main__':
  run() 