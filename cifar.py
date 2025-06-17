from typing import override

from torch.utils.data import Dataset


class CIFAR10(Dataset):
    def __init__(self, fp:str|) -> None:
        super(Dataset, self).__init__()

    def __len__(self) -> int:
        pass

    @override
    def __getitem__(self, index: int) -> Any:
        return super().__getitem__(index)
