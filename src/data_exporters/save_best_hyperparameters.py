from dvclive import Live
from typing import Dict


@data_exporter
def export_data(best_params: Dict, **kwargs):
    try:
        with Live(save_dvc_exp=True) as live:
            live.log_params({
                "Best hyperparameters": best_params,
            })
    except Exception as err:
        print(err)