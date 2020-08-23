# unicef-dssg

## Installation instructions
To install the required packages run:
`pipenv install`

If a package is not present in the pipenv run:
`pipenv install [insert package name here]`

To initialize to pipenv run:
`pipenv shell`

## Notes
To install `earthengine-api` run the following:
`pip install ee`

After this run `pipenv shell`

## Installing ipykernel instructions
To access all versions of packages in a kernel run:
python -m ipykernel install --user --name unicef-dssg --display-name "Python unicef-dssg kernel"

### Data import
To import google earthengine data after completing the above run:
`python src/scripts/run_ee_data_download.py`
