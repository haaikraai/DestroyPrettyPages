import torch
from torch.utils.data import DataLoader

import torch.utils.data
import torch.utils.dlpack
import torch.utils.tensorboard



from DestroyPrettyPage import DestroyPrettyPage

dpp = DestroyPrettyPage('https://course.fast.ai/')

dir(dpp)
dpp.page