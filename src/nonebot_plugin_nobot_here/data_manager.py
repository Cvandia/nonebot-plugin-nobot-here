"""
Description: data manager
"""

import json

from dataclasses import dataclass
from dataclasses import field
from pathlib import Path

from .config import plugin_config


_path = Path(plugin_config.nobot_data_path)


@dataclass
class DataManager:
    """
    数据管理器
    """

    data_path: Path
    data: dict[str, list[str]] = field(default_factory=dict)

    def load_data(self):
        """加载数据"""
        with open(self.data_path, "r", encoding="utf-8") as f:
            self.data = json.load(f)

    def save_data(self):
        """保存数据"""
        if not self.data_path.parent.exists():
            self.data_path.parent.mkdir(parents=True)
        with open(self.data_path, "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=4)

    def get_data(self, key: str):
        """获取数据"""
        return self.data.get(key)

    def set_data(self, key: str, value):
        """设置数据"""
        self.data[key] = value

    def del_data(self, key: str):
        """删除数据"""
        self.data.pop(key)

    def clear_data(self):
        """清空群聊数据"""
        for key in list(self.data.keys()):
            self.del_data(key)


data_manager = DataManager(_path, {})
