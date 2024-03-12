from torchvision import datasets
from torch.utils.data import Subset
from sklearn.model_selection import train_test_split
import numpy as np


def split_dataset_classwise(
    root, transform, train_size=0.7, test_size=0.2, val_size=0.1
):
    dataset = datasets.ImageFolder(root=root, transform=transform)

    train_indices = []
    test_indices = []
    val_indices = []

    for _, class_indices in dataset.class_to_idx.items():
        all_class_indices = np.where(np.array(dataset.targets) == class_indices)[0]
        train_and_test_indices, valid_class_indices = train_test_split(
            all_class_indices,
            test_size=val_size,
            random_state=2024,
            stratify=all_class_indices,
        )
        train_class_indices, test_class_indices = train_test_split(
            train_and_test_indices,
            test_size=test_size / (train_size + test_size),
            random_state=2024,
            stratify=train_and_test_indices,
        )

        train_indices.extend(train_class_indices)
        test_indices.extend(test_class_indices)
        val_indices.extend(valid_class_indices)

    # Create subset for each
    train_dataset = Subset(dataset, train_indices)
    test_dataset = Subset(dataset, test_indices)
    val_dataset = Subset(dataset, val_indices)

    return train_dataset, test_dataset, val_dataset
