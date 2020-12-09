import argparse
import apache_beam as beam
from apache_beam.io.textio import ReadFromTextWithFilename
from apache_beam.options.pipeline_options import PipelineOptions
import re
from nltk.corpus import stopwords


class WordExtractingDoFn(beam.DoFn):
    def __init__(self):
        self.stopwords = set(stopwords.words('english'))

    def __extract_author_from_filename(self, filename):
        pattern = re.compile(r'.*\/([\w\-]+)\/[\w\-]+\.txt')
        match = pattern.match(filename)

        if match is not None:
            return match.group(1)

        return None

    def process(self, element):
        filename, line = element
        for word in re.findall(r"[\w']+", line, re.UNICODE):
            if word not in self.stopwords:
                yield (self.__extract_author_from_filename(filename), word)


def run(argv=None, save_main_session=True):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--input',
        dest='input',
        default='gs://blog-data-resources/books_txt_files/**',
        help='Input file pattern to process.')
    parser.add_argument(
        '--table_spec ',
        dest='table_spec',
        default='ilan-uzan-297514:tests.author_wordcount',
        help='Destination BigQuery table.')
    known_args, pipeline_args = parser.parse_known_args(argv)

    pipeline_options = PipelineOptions(pipeline_args)
    with beam.Pipeline(options=pipeline_options) as p:
        table_schema = {
            'fields': [
                {'name': 'author', 'type': 'STRING', 'mode': 'NULLABLE'}, 
                {'name': 'word', 'type': 'STRING', 'mode': 'NULLABLE'},
                {'name': 'cnt', 'type': 'INTEGER', 'mode': 'NULLABLE'}
            ]
        }

        def to_json_row(element):
            key, cnt = element
            author, word = key

            return {"author": author, "word": word, "cnt": cnt}

        (p
         | 'Read files' >> ReadFromTextWithFilename(known_args.input)
         | 'Split lines' >> beam.ParDo(WordExtractingDoFn())
         | 'Pair with 1' >> beam.Map(lambda x: ((x[0], x[1]), 1))
         | 'Sum per author & word' >> beam.CombinePerKey(sum)
         | 'Format records to JSON' >> beam.Map(to_json_row)
         | 'Write to BigQuery' >> beam.io.WriteToBigQuery(
                                    known_args.table_spec,
                                    schema=table_schema,
                                    write_disposition=beam.io.BigQueryDisposition.WRITE_TRUNCATE,
                                    create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED)
                                 )


if __name__ == '__main__':
    run()
