import dvc.api

params = dvc.api.params_show()

lr = params['lr']
epochs = params['train']['epochs']
layers = params['train']['layers']