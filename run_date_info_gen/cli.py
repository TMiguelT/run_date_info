import click
import csv
from pathlib import Path
import json
import random
import datetime
import sys
import iso8601

multiqc_format = '%Y-%m-%d, %H:%M'


@click.command()
@click.argument('multiqc_dir', type=Path)
@click.option('--chronqc', is_flag=True)
@click.option('--change-date', is_flag=True)
@click.option('--date-range', nargs=2, help='If set, this is a range of ISO dates that will be randomly selected from',
              type=iso8601.parse_date)
def generate(multiqc_dir: Path, chronqc: bool, change_date: bool, date_range=None):
    date_start, date_end = date_range
    multiqc_data = multiqc_dir / 'multiqc_data.json'
    run_date_info = multiqc_dir / 'run_date_info.csv'

    # Load the metadata
    with multiqc_data.open() as fp:
        metadata = json.load(fp)
        samples = list(metadata['report_general_stats_data'][0].keys())

    # Calculate the new date for this sample
    if date_range is None:
        date = datetime.datetime.strptime(metadata['config_creation_date'], multiqc_format)
    else:
        options = []
        while date_start <= date_end:
            options.append(date_start)
            date_start += datetime.timedelta(days=1)
        date = random.choice(options)

    # If we're replacing the date, do it now
    if change_date:
        metadata['config_creation_date'] = date.strftime(multiqc_format)
        with multiqc_data.open('w') as out_fp:
            json.dump(metadata, out_fp)

    # If we're generating a run_date_info file, do it now
    if chronqc:
        with run_date_info.open('w') as out_fp:
            writer = csv.writer(out_fp)
            writer.writerow(('Sample', 'Run', 'Date'))
            for sample in samples:
                writer.writerow((sample, 'Run-1', date.strftime('%d/%m/%Y')))


if __name__ == '__main__':
    generate()
