#!/usr/bin/env python3
import pandas as pd
import os

default_kwargs = {
    'sep': ';',
    'quotechar': '"',
}
def process_caracs_pre_2019(caracs: pd.DataFrame) -> pd.DataFrame:
    caracs[['lat','long']] /= 100_000
    return caracs

sources = {
    '2020': {
        'usagers': {
            'url':'https://www.data.gouv.fr/fr/datasets/r/78c45763-d170-4d51-a881-e3147802d7ee',
            'opts': {**default_kwargs}
        },
        'caracteristiques': {
            'url':'https://www.data.gouv.fr/fr/datasets/r/07a88205-83c1-4123-a993-cba5331e8ae0',
            'opts': {
                **default_kwargs,
                'decimal': ','
            }
        }
    },
    '2019': {
        'usagers': {
            'url':'https://www.data.gouv.fr/fr/datasets/r/36b1b7b3-84b4-4901-9163-59ae8a9e3028',
            'opts': {**default_kwargs}
        },
        'caracteristiques': {
            'url':'https://www.data.gouv.fr/fr/datasets/r/e22ba475-45a3-46ac-a0f7-9ca9ed1e283a',
            'opts': {
                **default_kwargs,
                'decimal': ','
            }
        }
    },
    '2018': {
        'usagers': {
            'url':'https://www.data.gouv.fr/fr/datasets/r/72b251e1-d5e1-4c46-a1c2-c65f1b26549a',
            'opts': {}
        },
        'caracteristiques': {
            'url':'https://www.data.gouv.fr/fr/datasets/r/6eee0852-cbd7-447e-bd70-37c433029405',
            'opts': {
                'encoding':'iso-8859-1'
            },
            'process': process_caracs_pre_2019
        }
    },
    '2017': {
        'usagers': {
            'url':'https://www.data.gouv.fr/fr/datasets/r/07bfe612-0ad9-48ef-92d3-f5466f8465fe',
            'opts': {}
        },
        'caracteristiques': {
            'url':'https://www.data.gouv.fr/fr/datasets/r/9a7d408b-dd72-4959-ae7d-c854ec505354',
            'opts': {
                'encoding':'iso-8859-1'
            },
            'process': process_caracs_pre_2019
        }
    },
    '2016': {
        'usagers': {
            'url':'https://www.data.gouv.fr/fr/datasets/r/e4c6f4fe-7c68-4a1d-9bb6-b0f1f5d45526',
            'opts': {}
        },
        'caracteristiques': {
            'url':'https://www.data.gouv.fr/fr/datasets/r/96aadc9f-0b55-4e9a-a70e-c627ed97e6f7',
            'opts': {
                'encoding':'iso-8859-1'
            },
            'process': process_caracs_pre_2019
        }
    },
}

for year, src in sources.items():
    print(f"Collecting data for {year}")
    os.makedirs(year, exist_ok=True)

    print("Reading user data...")
    usagers = pd.read_csv(src['usagers']['url'], **src['usagers']['opts'])
    print("Reading accident caracteristics data...")
    caracs = pd.read_csv(src['caracteristiques']['url'], **src['caracteristiques']['opts'])

    if 'process' in src['usagers']:
        usagers = src['usagers']['process'](usagers)

    if 'process' in src['caracteristiques']:
        caracs = src['caracteristiques']['process'](caracs)

    # TODO process data, cleanup, join...
    # ...

    print("Writing file(s)...")
    usagers.to_csv(f"{year}/usagers.csv", index=False)
    caracs.to_csv(f"{year}/caracteristiques.csv", index=False)

print()
print("Done.")
