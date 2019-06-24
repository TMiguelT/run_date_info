import click
import csv
from pathlib import Path
import json
import random
import datetime
import sys


@click.command()
@click.argument('multiqc_dir', type=Path)
@click.option('--date-range', nargs=2, help='If set, this is a range of ISO dates that will be randomly selected from',
              type=datetime.date.fromisoformat)
def generate(multiqc_dir: Path, date_range=None):
    date_start, date_end = date_range

    with (multiqc_dir / 'multiqc_data.json').open() as fp:
        metadata = json.load(fp)

    if date_range is None:
        date = datetime.datetime.strptime(metadata['config_creation_date'], '%Y-%m-%d, %H:%M')
    else:
        options = []
        while date_start <= date_end:
            options.append(date_start)
            date_start += datetime.timedelta(days=1)
        date = random.choice(options)

    samples = list(metadata['report_general_stats_data'][0].keys())

    writer = csv.writer(sys.stdout)
    writer.writerow(('Sample', 'Run', 'Date'))
    for sample in samples:
        writer.writerow((sample, 'Run-1', date.strftime('%d/%m/%Y')))


if __name__ == '__main__':
    generate()
