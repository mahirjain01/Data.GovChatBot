import pandas as pd
from datagovindia import DataGovIndia
import logging

class DataDownloader:
    def __init__(self, api_key=None):
        self.datagovin = DataGovIndia(api_key)
        self.datagovin.sync_metadata()

    def search_data(self, query, search_fields=None, sort_by=None, ascending=True):
        try:
            return self.datagovin.search(query, search_fields=search_fields, sort_by=sort_by, ascending=ascending)
        except Exception as e:
            logging.error(f"Error during search: {str(e)}")
            raise

    def get_resource_info(self, resource_id):
        try:
            return self.datagovin.get_resource_info(resource_id)
        except Exception as e:
            logging.error(f"Error getting resource info: {str(e)}")
            raise

    def get_data(self, resource_id, sort_by=None, ascending=True, offset=0, batch_size=2000,
                 limit=None, filters=None, fields=None, njobs=None):
        try:
            return self.datagovin.get_data(resource_id, sort_by=sort_by, ascending=ascending,
                                           offset=offset, batch_size=batch_size, limit=limit,
                                           filters=filters, fields=fields, njobs=njobs)
        except Exception as e:
            logging.error(f"Error getting data: {str(e)}")
            raise

    def download_data(self, resource_id, output_format="csv", output_filepath=None):
        try:
            data = self.get_data(resource_id)
            if output_filepath:
                if output_format == "csv":
                    data.to_csv(output_filepath, index=False)
                elif output_format == "json":
                    data.to_json(output_filepath, orient="records")
                else:
                    raise ValueError("Invalid output format. Supported formats: csv, json")
            return data
        except Exception as e:
            logging.error(f"Error during download: {str(e)}")
            raise

